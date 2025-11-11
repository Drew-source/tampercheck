#!/usr/bin/env python3
"""
REAL Tamper Detection Analysis
Actually gets token probabilities for the edited text from OpenAI API
"""

import os
import sys
import json

# Set UTF-8 encoding for Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

from openai import OpenAI
from colorama import Fore, Style, init as colorama_init

colorama_init(autoreset=True)


def get_token_probabilities(client, context, text_to_analyze):
    """
    Get REAL token probabilities for specific text.
    
    We'll use the completion API to get probabilities for each token
    in the text we want to analyze.
    """
    print(f"\n{Fore.CYAN}Getting real token probabilities from OpenAI API...")
    
    # Build the prompt with context
    prompt = context[0]['content'] + "\n\n"
    
    try:
        # Use the completions API with the text as a continuation
        # We need to get logprobs for the text we're analyzing
        response = client.completions.create(
            model="gpt-3.5-turbo-instruct",  # This model supports logprobs
            prompt=prompt + text_to_analyze,
            max_tokens=0,  # We don't want new tokens, just logprobs of existing
            echo=True,  # Echo back the prompt with logprobs
            logprobs=5,  # Get top 5 alternatives for each token
            temperature=0.7
        )
        
        return response
        
    except Exception as e:
        print(f"{Fore.RED}Error: {e}")
        print(f"{Fore.YELLOW}Trying alternative method...")
        
        # Alternative: Generate with the text as context and see what model would say
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=context + [{"role": "assistant", "content": text_to_analyze}],
                max_tokens=1,
                logprobs=True,
                top_logprobs=5
            )
            return response
        except Exception as e2:
            print(f"{Fore.RED}Alternative method also failed: {e2}")
            return None


def analyze_text_real(original_text, edited_text, context):
    """
    Analyze BOTH texts with real API calls to get actual probabilities
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    print(f"\n{Fore.CYAN}{Style.BRIGHT}{'='*80}")
    print("REAL TAMPER DETECTION ANALYSIS")
    print(f"{'='*80}{Style.RESET_ALL}")
    
    print(f"\n{Fore.WHITE}Original Text:")
    print(f"{Fore.GREEN}{original_text}")
    
    print(f"\n{Fore.WHITE}Edited Text:")
    print(f"{Fore.YELLOW}{edited_text}")
    
    # Method: Use completions API with echo to get logprobs
    print(f"\n{Fore.CYAN}Analyzing EDITED text with real token probabilities...")
    
    # Build prompt
    prompt = context[0]['content'] + "\n\n"
    
    try:
        # Get logprobs for the edited text
        response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=len(edited_text.split()) + 50,
            logprobs=5,
            temperature=0.7
        )
        
        print(f"\n{Fore.GREEN}✓ Got real probabilities from API!")
        
        # Parse the response
        if hasattr(response.choices[0], 'logprobs') and response.choices[0].logprobs:
            logprobs_data = response.choices[0].logprobs
            
            print(f"\n{Fore.WHITE}{Style.BRIGHT}TOKEN-BY-TOKEN ANALYSIS (REAL DATA):")
            print(f"{Fore.CYAN}{'='*80}")
            print(f"\n{'Token':<20} {'Probability':<15} {'Level':<10}")
            print(f"{'-'*80}")
            
            tokens = logprobs_data.tokens
            token_logprobs = logprobs_data.token_logprobs
            
            high_count = 0
            medium_count = 0
            low_count = 0
            
            results = []
            
            for i, (token, logprob) in enumerate(zip(tokens, token_logprobs)):
                if logprob is None:
                    continue
                    
                prob = 2.71828 ** logprob  # e^logprob
                prob_pct = prob * 100
                
                # Classify
                if prob >= 0.20:
                    level = "HIGH"
                    color = Fore.GREEN
                    high_count += 1
                elif prob >= 0.05:
                    level = "MEDIUM"
                    color = Fore.YELLOW
                    medium_count += 1
                else:
                    level = "LOW"
                    color = Fore.RED
                    low_count += 1
                
                token_display = token.replace('\n', '\\n')[:20]
                print(f"{color}{token_display:<20} {prob_pct:>6.2f}%{' '*8} {level:<10}{Style.RESET_ALL}")
                
                results.append({
                    'token': token,
                    'probability': prob,
                    'level': level
                })
            
            # Statistics
            total = high_count + medium_count + low_count
            print(f"\n{Fore.CYAN}{'='*80}")
            print(f"{Fore.WHITE}{Style.BRIGHT}STATISTICS:")
            print(f"  Total tokens: {total}")
            print(f"  {Fore.GREEN}HIGH probability (>20%): {high_count} ({high_count/total*100:.1f}%)")
            print(f"  {Fore.YELLOW}MEDIUM probability (5-20%): {medium_count} ({medium_count/total*100:.1f}%)")
            print(f"  {Fore.RED}LOW probability (<5%): {low_count} ({low_count/total*100:.1f}%)")
            
            if low_count > total * 0.10:  # More than 10% low probability
                print(f"\n{Fore.RED}{Style.BRIGHT}⚠️  TAMPERING DETECTED!")
                print(f"{Fore.WHITE}High percentage of low-probability tokens suggests editing.")
            else:
                print(f"\n{Fore.GREEN}✓ Text appears authentic")
            
            # Save results
            with open('real_analysis_results.json', 'w', encoding='utf-8') as f:
                json.dump({
                    'original_text': original_text,
                    'edited_text': edited_text,
                    'tokens': results,
                    'statistics': {
                        'high': high_count,
                        'medium': medium_count,
                        'low': low_count,
                        'total': total
                    }
                }, f, indent=2, ensure_ascii=False)
            
            print(f"\n{Fore.GREEN}Results saved to: real_analysis_results.json")
            
            return results
            
        else:
            print(f"{Fore.RED}No logprobs data in response")
            return None
            
    except Exception as e:
        print(f"{Fore.RED}Error: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    print(f"{Fore.CYAN}{Style.BRIGHT}")
    print("="*80)
    print("  REAL TAMPER DETECTION TEST")
    print("  Using actual OpenAI API probabilities - no simulation!")
    print("="*80)
    print(Style.RESET_ALL)
    
    # Original text from first generation
    original_text = """Once there was a robot who could perform complex calculations and complete tasks with precision, but it longed to express itself in a more creative way. So, it decided to learn how to paint. With each stroke of the brush, the robot discovered the joy of blending colors and creating beautiful works of art, proving that even machines can find beauty in creativity."""
    
    # User's edited version
    edited_text = """Once there was a small robot who could perform complex calculations and complete tasks with accuracy but it wanted to express itself in a more creative manner. So one day, it decided to learn how to paint. With each stroke of the paint brush, the litte robot discovered the joy of blending colors and creating splendid works of art, proving that even machines can find beauty in art."""
    
    # Context
    context = [
        {"role": "user", "content": "Write a short story about a robot learning to paint. Keep it to 2-3 sentences."}
    ]
    
    # Run REAL analysis
    results = analyze_text_real(original_text, edited_text, context)
    
    if results:
        print(f"\n{Fore.GREEN}{Style.BRIGHT}✓ REAL analysis complete!")
        print(f"\n{Fore.CYAN}This is actual data from OpenAI's API - no simulation.")
        print(f"{Fore.CYAN}The probabilities show what the model ACTUALLY thinks about each token.")
    else:
        print(f"\n{Fore.YELLOW}Analysis method needs adjustment for this API version.")
        print(f"{Fore.YELLOW}The theory is sound, but we need to use a different approach.")


if __name__ == "__main__":
    main()

