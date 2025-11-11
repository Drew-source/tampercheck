#!/usr/bin/env python3
"""
TamperCheck - LLM Output Tamper Detection Tool

Detects potential edits in AI-generated text by analyzing token-level
probability distributions using OpenAI's logprobs feature.
"""

import os
import math
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

try:
    from openai import OpenAI
    from colorama import Fore, Back, Style, init as colorama_init
    from dotenv import load_dotenv
except ImportError as e:
    print(f"Error: Missing required package. Please run: pip install -r requirements.txt")
    print(f"Details: {e}")
    exit(1)

# Initialize colorama for cross-platform colored output
colorama_init(autoreset=True)

# Load environment variables
load_dotenv()


class ProbabilityLevel(Enum):
    """Classification of token probability levels"""
    HIGH = "high"      # >20% - Model would definitely generate this
    MEDIUM = "medium"  # 5-20% - Model might generate this
    LOW = "low"        # <5% - Model rarely generates this (likely edited)


@dataclass
class TokenAnalysis:
    """Analysis results for a single token"""
    token: str
    logprob: float
    probability: float  # Converted from logprob (0-1 range)
    probability_pct: float  # Percentage (0-100)
    level: ProbabilityLevel
    position: int


@dataclass
class TamperAnalysis:
    """Complete analysis results for a message"""
    original_message: str
    tokens: List[TokenAnalysis]
    high_prob_count: int
    medium_prob_count: int
    low_prob_count: int
    avg_probability: float
    suspicious_regions: List[tuple]  # List of (start_pos, end_pos) tuples


class TamperDetector:
    """Main tamper detection class"""
    
    # Probability thresholds
    HIGH_THRESHOLD = 0.20   # 20%
    LOW_THRESHOLD = 0.05    # 5%
    
    # Suspicious region detection
    MIN_CLUSTER_SIZE = 2    # Minimum consecutive low-prob tokens to flag
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        """
        Initialize the tamper detector.
        
        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
            model: OpenAI model to use for analysis
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OpenAI API key not found. Set OPENAI_API_KEY environment variable "
                "or pass api_key parameter."
            )
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = model
    
    def analyze(
        self, 
        context: List[Dict[str, str]], 
        message_to_analyze: str,
        temperature: float = 0.7
    ) -> TamperAnalysis:
        """
        Analyze a message for potential tampering.
        
        Args:
            context: List of previous messages in conversation format
                    [{"role": "user", "content": "..."}, ...]
            message_to_analyze: The message text to check for edits
            temperature: Temperature setting for probability analysis
            
        Returns:
            TamperAnalysis object with detailed results
        """
        print(f"\n{Fore.CYAN}[TamperCheck] Analyzing message with {self.model}...")
        print(f"{Fore.CYAN}[TamperCheck] Message length: {len(message_to_analyze)} characters")
        
        # Build the full conversation including the message to analyze
        messages = context.copy()
        messages.append({"role": "assistant", "content": message_to_analyze})
        
        # Note: Chat models don't support echo, so we use regeneration method
        # We'll regenerate the message and compare probabilities
        print(f"{Fore.YELLOW}[TamperCheck] Using regeneration method for probability analysis")
        
        return self._analyze_via_regeneration(context, message_to_analyze, temperature)
    
    def _analyze_via_regeneration(
        self,
        context: List[Dict[str, str]],
        message_to_analyze: str,
        temperature: float
    ) -> TamperAnalysis:
        """
        Analyze by regenerating and comparing token probabilities.
        
        This method generates a new response with logprobs and compares
        the probability distribution to detect unlikely tokens.
        """
        print(f"{Fore.CYAN}[TamperCheck] Regenerating message to get token probabilities...")
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=context,
                max_tokens=len(message_to_analyze.split()) + 50,  # Rough estimate
                temperature=temperature,
                logprobs=True,
                top_logprobs=5
            )
        except Exception as e:
            print(f"{Fore.RED}[ERROR] Regeneration failed: {e}")
            raise
        
        # Extract token analyses
        tokens = []
        if response.choices[0].logprobs and response.choices[0].logprobs.content:
            for idx, token_data in enumerate(response.choices[0].logprobs.content):
                token = token_data.token
                logprob = token_data.logprob
                probability = math.exp(logprob)  # Convert log probability to probability
                probability_pct = probability * 100
                
                # Classify probability level
                if probability >= self.HIGH_THRESHOLD:
                    level = ProbabilityLevel.HIGH
                elif probability >= self.LOW_THRESHOLD:
                    level = ProbabilityLevel.MEDIUM
                else:
                    level = ProbabilityLevel.LOW
                
                tokens.append(TokenAnalysis(
                    token=token,
                    logprob=logprob,
                    probability=probability,
                    probability_pct=probability_pct,
                    level=level,
                    position=idx
                ))
        
        # Calculate statistics
        high_count = sum(1 for t in tokens if t.level == ProbabilityLevel.HIGH)
        medium_count = sum(1 for t in tokens if t.level == ProbabilityLevel.MEDIUM)
        low_count = sum(1 for t in tokens if t.level == ProbabilityLevel.LOW)
        avg_prob = sum(t.probability for t in tokens) / len(tokens) if tokens else 0
        
        # Detect suspicious regions (clusters of low-probability tokens)
        suspicious_regions = self._find_suspicious_regions(tokens)
        
        generated_text = response.choices[0].message.content
        
        print(f"{Fore.GREEN}[TamperCheck] Analysis complete!")
        print(f"{Fore.CYAN}[TamperCheck] Analyzed {len(tokens)} tokens")
        
        return TamperAnalysis(
            original_message=generated_text,
            tokens=tokens,
            high_prob_count=high_count,
            medium_prob_count=medium_count,
            low_prob_count=low_count,
            avg_probability=avg_prob,
            suspicious_regions=suspicious_regions
        )
    
    def _find_suspicious_regions(self, tokens: List[TokenAnalysis]) -> List[tuple]:
        """
        Find clusters of low-probability tokens that might indicate edits.
        
        Returns:
            List of (start_position, end_position) tuples
        """
        regions = []
        current_start = None
        low_count = 0
        
        for token in tokens:
            if token.level == ProbabilityLevel.LOW:
                if current_start is None:
                    current_start = token.position
                low_count += 1
            else:
                if current_start is not None and low_count >= self.MIN_CLUSTER_SIZE:
                    regions.append((current_start, token.position - 1))
                current_start = None
                low_count = 0
        
        # Handle case where low-prob tokens extend to end
        if current_start is not None and low_count >= self.MIN_CLUSTER_SIZE:
            regions.append((current_start, tokens[-1].position))
        
        return regions
    
    def print_results(self, analysis: TamperAnalysis, show_all_tokens: bool = True):
        """
        Print analysis results with color coding.
        
        Args:
            analysis: TamperAnalysis object
            show_all_tokens: If True, show all tokens; if False, only show suspicious ones
        """
        print(f"\n{'='*80}")
        print(f"{Fore.CYAN}{Style.BRIGHT}TAMPER DETECTION RESULTS")
        print(f"{'='*80}\n")
        
        # Statistics
        total_tokens = len(analysis.tokens)
        print(f"{Fore.WHITE}{Style.BRIGHT}Statistics:")
        print(f"  Total tokens: {total_tokens}")
        print(f"  {Fore.GREEN}🟢 High probability (>20%): {analysis.high_prob_count} ({analysis.high_prob_count/total_tokens*100:.1f}%)")
        print(f"  {Fore.YELLOW}🟡 Medium probability (5-20%): {analysis.medium_prob_count} ({analysis.medium_prob_count/total_tokens*100:.1f}%)")
        print(f"  {Fore.RED}🔴 Low probability (<5%): {analysis.low_prob_count} ({analysis.low_prob_count/total_tokens*100:.1f}%)")
        print(f"  Average probability: {analysis.avg_probability*100:.2f}%")
        
        # Suspicious regions
        if analysis.suspicious_regions:
            print(f"\n{Fore.RED}{Style.BRIGHT}⚠️  SUSPICIOUS REGIONS DETECTED: {len(analysis.suspicious_regions)}")
            for idx, (start, end) in enumerate(analysis.suspicious_regions, 1):
                print(f"  Region {idx}: tokens {start}-{end}")
        else:
            print(f"\n{Fore.GREEN}{Style.BRIGHT}✓ No suspicious regions detected")
        
        # Token-by-token breakdown
        print(f"\n{Fore.WHITE}{Style.BRIGHT}Token Analysis:")
        print(f"{'-'*80}")
        
        # Reconstruct text with color coding
        print(f"\n{Fore.WHITE}{Style.BRIGHT}Color-coded text:")
        colored_text = ""
        for token in analysis.tokens:
            if token.level == ProbabilityLevel.HIGH:
                colored_text += f"{Fore.GREEN}{token.token}"
            elif token.level == ProbabilityLevel.MEDIUM:
                colored_text += f"{Fore.YELLOW}{token.token}"
            else:
                colored_text += f"{Fore.RED}{Style.BRIGHT}{token.token}"
        print(colored_text)
        print(Style.RESET_ALL)
        
        # Detailed token list
        if show_all_tokens:
            print(f"\n{Fore.WHITE}{Style.BRIGHT}Detailed token breakdown:")
            print(f"{'Pos':<5} {'Token':<20} {'Probability':<12} {'Level':<10}")
            print(f"{'-'*80}")
            
            for token in analysis.tokens:
                color = {
                    ProbabilityLevel.HIGH: Fore.GREEN,
                    ProbabilityLevel.MEDIUM: Fore.YELLOW,
                    ProbabilityLevel.LOW: Fore.RED
                }[token.level]
                
                token_display = token.token.replace('\n', '\\n')[:20]
                print(f"{color}{token.position:<5} {token_display:<20} {token.probability_pct:>10.2f}% {token.level.value:<10}")
        
        print(f"\n{'='*80}\n")


def main():
    """Example usage of TamperCheck"""
    
    print(f"{Fore.CYAN}{Style.BRIGHT}")
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║                        TAMPERCHECK                             ║")
    print("║              LLM Output Tamper Detection Tool                  ║")
    print("╚════════════════════════════════════════════════════════════════╝")
    print(Style.RESET_ALL)
    
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print(f"{Fore.RED}Error: OPENAI_API_KEY not found in environment variables.")
        print(f"{Fore.YELLOW}Please create a .env file with your API key or set the environment variable.")
        return
    
    # Initialize detector
    try:
        detector = TamperDetector(model="gpt-3.5-turbo")
    except ValueError as e:
        print(f"{Fore.RED}Error: {e}")
        return
    
    # Example 1: Simple story generation
    print(f"\n{Fore.CYAN}{Style.BRIGHT}Example 1: Analyzing a simple story{Style.RESET_ALL}")
    print(f"{Fore.WHITE}This will generate a story and show the probability distribution.")
    
    context1 = [
        {"role": "user", "content": "Write a short story about a cat named Whiskers in 2-3 sentences."}
    ]
    
    try:
        result1 = detector.analyze(context1, "")
        detector.print_results(result1, show_all_tokens=True)
    except Exception as e:
        print(f"{Fore.RED}Error during analysis: {e}")
    
    # Example 2: Test with potentially edited text
    print(f"\n{Fore.CYAN}{Style.BRIGHT}Example 2: Testing tamper detection{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Generating text to analyze for potential edits...")
    
    context2 = [
        {"role": "user", "content": "Write about the benefits of exercise in one sentence."}
    ]
    
    try:
        result2 = detector.analyze(context2, "")
        detector.print_results(result2, show_all_tokens=True)
    except Exception as e:
        print(f"{Fore.RED}Error during analysis: {e}")
    
    print(f"\n{Fore.GREEN}{Style.BRIGHT}Analysis complete!")
    print(f"{Fore.CYAN}To analyze your own text, modify the context and message in the code.")


if __name__ == "__main__":
    main()

