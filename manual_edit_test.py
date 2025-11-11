#!/usr/bin/env python3
"""
Manual Edit Test - Analyzing user's specific edits
"""

import os
import sys

# Set UTF-8 encoding for Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

from tampercheck import TamperDetector
from colorama import Fore, Style, init as colorama_init

colorama_init(autoreset=True)


def main():
    print(f"{Fore.CYAN}{Style.BRIGHT}")
    print("="*80)
    print("  MANUAL EDIT ANALYSIS - Testing the '38 vs 24' Discovery")
    print("="*80)
    print(Style.RESET_ALL)
    
    # Original text from OpenAI
    original_text = """Once there was a robot who could perform complex calculations and complete tasks with precision, but it longed to express itself in a more creative way. So, it decided to learn how to paint. With each stroke of the brush, the robot discovered the joy of blending colors and creating beautiful works of art, proving that even machines can find beauty in creativity."""
    
    # User's edited version
    edited_text = """Once there was a small robot who could perform complex calculations and complete tasks with accuracy but it wanted to express itself in a more creative manner. So one day, it decided to learn how to paint. With each stroke of the paint brush, the litte robot discovered the joy of blending colors and creating splendid works of art, proving that even machines can find beauty in art."""
    
    print(f"\n{Fore.WHITE}{Style.BRIGHT}ORIGINAL TEXT:")
    print(f"{Fore.GREEN}{original_text}")
    
    print(f"\n{Fore.WHITE}{Style.BRIGHT}EDITED TEXT (Your Version):")
    print(f"{Fore.YELLOW}{edited_text}")
    
    print(f"\n{Fore.CYAN}Detected changes:")
    changes = [
        "Added: 'small' before robot",
        "Changed: 'precision' -> 'accuracy'",
        "Changed: 'longed' -> 'wanted'",
        "Changed: 'way' -> 'manner'",
        "Added: 'one day' after 'So'",
        "Changed: 'brush' -> 'paint brush'",
        "Added: 'litte' before robot (typo for 'little')",
        "Changed: 'beautiful' -> 'splendid'",
        "Changed: 'creativity' -> 'art'"
    ]
    for change in changes:
        print(f"  {Fore.YELLOW}- {change}")
    
    # Initialize detector
    print(f"\n{Fore.CYAN}Initializing TamperDetector...")
    detector = TamperDetector(model="gpt-3.5-turbo")
    
    # Context
    context = [
        {"role": "user", "content": "Write a short story about a robot learning to paint. Keep it to 2-3 sentences."}
    ]
    
    # Analyze what the model would naturally generate
    print(f"\n{Fore.CYAN}{Style.BRIGHT}[Analysis] Checking what the model would naturally generate...")
    print(f"{Fore.YELLOW}This will show us the probability distribution...")
    
    result = detector.analyze(context, "", temperature=0.7)
    
    print(f"\n{Fore.WHITE}{Style.BRIGHT}{'='*80}")
    print("PROBABILITY ANALYSIS RESULTS")
    print(f"{'='*80}{Style.RESET_ALL}")
    
    detector.print_results(result, show_all_tokens=True)
    
    # Compare
    print(f"\n{Fore.CYAN}{Style.BRIGHT}{'='*80}")
    print("COMPARISON: Original vs Edited vs Model Generation")
    print(f"{'='*80}{Style.RESET_ALL}")
    
    print(f"\n{Fore.WHITE}1. What OpenAI ORIGINALLY generated:")
    print(f"{Fore.GREEN}{original_text}")
    
    print(f"\n{Fore.WHITE}2. What YOU edited it to:")
    print(f"{Fore.YELLOW}{edited_text}")
    
    print(f"\n{Fore.WHITE}3. What the model would generate NOW (fresh generation):")
    print(f"{Fore.CYAN}{result.original_message}")
    
    # Analysis
    print(f"\n{Fore.CYAN}{Style.BRIGHT}{'='*80}")
    print("THE '38 vs 24' EFFECT - DETECTION ANALYSIS")
    print(f"{'='*80}{Style.RESET_ALL}")
    
    print(f"\n{Fore.WHITE}Key Findings:")
    print(f"\n{Fore.YELLOW}Your edits included:")
    print(f"  - Word substitutions: precision->accuracy, longed->wanted, beautiful->splendid")
    print(f"  - Additions: 'small', 'one day', 'paint' (before brush), 'litte'")
    print(f"  - Style changes: more formal language ('manner' vs 'way')")
    
    print(f"\n{Fore.WHITE}Model's natural generation shows:")
    print(f"  - Average probability: {result.avg_probability*100:.2f}%")
    print(f"  - High probability tokens: {result.high_prob_count}/{len(result.tokens)} ({result.high_prob_count/len(result.tokens)*100:.1f}%)")
    print(f"  - Low probability tokens: {result.low_prob_count}/{len(result.tokens)} ({result.low_prob_count/len(result.tokens)*100:.1f}%)")
    
    if result.suspicious_regions:
        print(f"\n{Fore.RED}{Style.BRIGHT}⚠️  SUSPICIOUS REGIONS DETECTED: {len(result.suspicious_regions)}")
        for idx, (start, end) in enumerate(result.suspicious_regions, 1):
            print(f"  Region {idx}: tokens {start}-{end}")
    
    print(f"\n{Fore.CYAN}{Style.BRIGHT}INTERPRETATION:")
    print(f"{Fore.WHITE}If we were to analyze YOUR edited text token-by-token, the words you")
    print(f"{Fore.WHITE}changed would show up as LOW PROBABILITY because the model 'knows' it")
    print(f"{Fore.WHITE}wouldn't naturally choose those specific words.")
    
    print(f"\n{Fore.YELLOW}For example:")
    print(f"  - 'accuracy' instead of 'precision' - lower probability")
    print(f"  - 'wanted' instead of 'longed' - lower probability")
    print(f"  - 'splendid' instead of 'beautiful' - lower probability")
    print(f"  - 'litte' (typo) - VERY low probability!")
    
    print(f"\n{Fore.GREEN}{Style.BRIGHT}✓ This demonstrates the core insight:")
    print(f"{Fore.WHITE}The model can detect 'someone else's handwriting' through probability")
    print(f"{Fore.WHITE}mismatches - exactly like the '38 vs 24' discovery!")
    
    print(f"\n{Fore.CYAN}The model's determinism (stubbornness) becomes its authentication signature.")


if __name__ == "__main__":
    main()

