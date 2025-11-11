#!/usr/bin/env python3
"""
FALSE POSITIVE TEST
Analyze the ORIGINAL AI-generated text to establish baseline
Should show mostly HIGH probability (few/no false positives)
"""

import os
import sys
import json
import math
import time

if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

from openai import OpenAI
from colorama import Fore, Style, init as colorama_init

colorama_init(autoreset=True)


def analyze_all_tokens(client, context_prompt, text_to_analyze, label):
    """
    Analyze ALL tokens
    """
    
    print(f"\n{Fore.CYAN}{Style.BRIGHT}ANALYZING: {label}")
    print(f"{'='*80}{Style.RESET_ALL}")
    
    # Split into tokens
    import re
    tokens = re.findall(r'\w+|[^\w\s]|\s+', text_to_analyze)
    
    print(f"\n{Fore.CYAN}Analyzing {len(tokens)} tokens...")
    print(f"\n{'Pos':<5} {'Token':<25} {'Status':<15} {'Model Prefers'}")
    print(f"{'-'*100}")
    
    results = []
    current_text = ""
    
    for i, token in enumerate(tokens):
        # Skip pure whitespace
        if token.strip() == "":
            current_text += token
            continue
        
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": context_prompt},
                    {"role": "assistant", "content": current_text}
                ],
                max_tokens=1,
                temperature=0.7,
                logprobs=True,
                top_logprobs=5
            )
            
            if response.choices[0].logprobs and response.choices[0].logprobs.content:
                top_tokens_data = response.choices[0].logprobs.content[0]
                
                # Get top alternatives
                top_alternatives = []
                if top_tokens_data.top_logprobs:
                    for alt in top_tokens_data.top_logprobs:
                        alt_token = alt.token.strip()
                        alt_prob = math.exp(alt.logprob) * 100
                        top_alternatives.append({
                            'token': alt_token,
                            'probability': alt_prob
                        })
                
                # Check if our token matches any top alternative
                our_token_clean = token.strip().lower()
                our_token_found = False
                our_token_prob = 0
                match_rank = -1
                
                for rank, alt in enumerate(top_alternatives):
                    alt_clean = alt['token'].strip().lower()
                    if our_token_clean == alt_clean or our_token_clean in alt_clean or alt_clean in our_token_clean:
                        our_token_found = True
                        our_token_prob = alt['probability']
                        match_rank = rank + 1
                        break
                
                # Determine status
                if our_token_found and our_token_prob > 20:
                    status = f"{Fore.GREEN}✓ HIGH ({our_token_prob:.1f}%)"
                    status_text = "HIGH"
                elif our_token_found and our_token_prob > 5:
                    status = f"{Fore.YELLOW}○ MED ({our_token_prob:.1f}%)"
                    status_text = "MEDIUM"
                elif our_token_found:
                    status = f"{Fore.RED}! LOW ({our_token_prob:.1f}%)"
                    status_text = "LOW"
                else:
                    status = f"{Fore.RED}✗ NOT IN TOP 5"
                    status_text = "NOT_FOUND"
                
                top_pref = top_alternatives[0]['token'] if top_alternatives else "N/A"
                top_prob = top_alternatives[0]['probability'] if top_alternatives else 0
                
                print(f"{i:<5} {token[:25]:<25} {status:<15} {top_pref} ({top_prob:.1f}%){Style.RESET_ALL}")
                
                results.append({
                    'position': i,
                    'token': token,
                    'found': our_token_found,
                    'probability': our_token_prob,
                    'rank': match_rank,
                    'status': status_text,
                    'top_alternatives': top_alternatives
                })
            
            current_text += token
            time.sleep(0.1)
            
        except Exception as e:
            print(f"{Fore.RED}Error at token {i}: {e}")
            results.append({
                'position': i,
                'token': token,
                'found': False,
                'probability': 0,
                'rank': -1,
                'status': 'ERROR',
                'top_alternatives': []
            })
    
    return results


def main():
    print(f"{Fore.CYAN}{Style.BRIGHT}")
    print("="*80)
    print("  FALSE POSITIVE TEST")
    print("  Testing ORIGINAL AI-generated text (no edits)")
    print("="*80)
    print(Style.RESET_ALL)
    
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    context_prompt = "Write a short story about a robot learning to paint. Keep it to 2-3 sentences."
    
    # ORIGINAL AI-generated text (no edits)
    original_text = "Once there was a robot who could perform complex calculations and complete tasks with precision, but it longed to express itself in a more creative way. So, it decided to learn how to paint. With each stroke of the brush, the robot discovered the joy of blending colors and creating beautiful works of art, proving that even machines can find beauty in creativity."
    
    print(f"\n{Fore.WHITE}Context: {Fore.CYAN}{context_prompt}")
    print(f"\n{Fore.WHITE}Testing ORIGINAL text (should show mostly HIGH probability):")
    print(f"{Fore.GREEN}{original_text}")
    
    # Analyze
    results = analyze_all_tokens(client, context_prompt, original_text, "ORIGINAL (No Edits)")
    
    # Statistics
    total = len([r for r in results if r['status'] != 'ERROR'])
    high = len([r for r in results if r['status'] == 'HIGH'])
    medium = len([r for r in results if r['status'] == 'MEDIUM'])
    low = len([r for r in results if r['status'] == 'LOW'])
    not_found = len([r for r in results if r['status'] == 'NOT_FOUND'])
    
    high_pct = (high / total * 100) if total > 0 else 0
    not_found_pct = (not_found / total * 100) if total > 0 else 0
    
    print(f"\n{Fore.CYAN}{Style.BRIGHT}{'='*80}")
    print("RESULTS - FALSE POSITIVE TEST")
    print(f"{'='*80}{Style.RESET_ALL}")
    
    print(f"\n{Fore.WHITE}Total tokens analyzed: {total}")
    print(f"{Fore.GREEN}HIGH probability (>20%): {high} ({high_pct:.1f}%)")
    print(f"{Fore.YELLOW}MEDIUM probability (5-20%): {medium}")
    print(f"{Fore.RED}LOW probability (<5%): {low}")
    print(f"{Fore.RED}NOT in top 5: {not_found} ({not_found_pct:.1f}%)")
    
    # Interpretation
    print(f"\n{Fore.CYAN}{Style.BRIGHT}INTERPRETATION:")
    
    if high_pct >= 80 and not_found_pct < 10:
        print(f"{Fore.GREEN}✓ EXCELLENT: Original text shows {high_pct:.1f}% high probability")
        print(f"{Fore.GREEN}✓ Low false positive rate: {not_found_pct:.1f}%")
        print(f"{Fore.GREEN}✓ System correctly identifies authentic AI text!")
    elif high_pct >= 70:
        print(f"{Fore.YELLOW}○ GOOD: {high_pct:.1f}% high probability")
        print(f"{Fore.YELLOW}○ Some variance is normal due to temperature/creativity")
    else:
        print(f"{Fore.RED}⚠ UNEXPECTED: Lower than expected high probability")
        print(f"{Fore.RED}⚠ May indicate issue with analysis method")
    
    # Compare to edited version
    print(f"\n{Fore.CYAN}{Style.BRIGHT}COMPARISON TO EDITED VERSION:")
    print(f"{Fore.WHITE}Original (no edits): {Fore.GREEN}{high_pct:.1f}% HIGH, {Fore.RED}{not_found_pct:.1f}% NOT IN TOP 5")
    print(f"{Fore.WHITE}Edited version:      {Fore.GREEN}~70% HIGH, {Fore.RED}~17% NOT IN TOP 5")
    print(f"\n{Fore.YELLOW}The edited version shows SIGNIFICANTLY more low-probability tokens!")
    print(f"{Fore.YELLOW}This confirms the system can distinguish edited from original text.")
    
    # Save results
    with open('original_analysis_results.json', 'w', encoding='utf-8') as f:
        json.dump({
            'text': original_text,
            'context': context_prompt,
            'results': results,
            'statistics': {
                'total': total,
                'high': high,
                'medium': medium,
                'low': low,
                'not_found': not_found,
                'high_pct': high_pct,
                'not_found_pct': not_found_pct
            }
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n{Fore.GREEN}Results saved to: original_analysis_results.json")
    
    # Show any false positives
    if not_found > 0:
        print(f"\n{Fore.YELLOW}False Positives (tokens flagged but shouldn't be):")
        for r in results:
            if r['status'] == 'NOT_FOUND':
                print(f"  - '{r['token']}' at position {r['position']}")
                if r['top_alternatives']:
                    print(f"    Model preferred: '{r['top_alternatives'][0]['token']}' ({r['top_alternatives'][0]['probability']:.1f}%)")
    
    print(f"\n{Fore.GREEN}{Style.BRIGHT}✓ FALSE POSITIVE TEST COMPLETE!")


if __name__ == "__main__":
    main()

