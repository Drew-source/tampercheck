#!/usr/bin/env python3
"""
Token-by-Token Analysis
Feed the edited text piece by piece and check probability of each next token
"""

import os
import sys
import json
import math

if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

from openai import OpenAI
from colorama import Fore, Style, init as colorama_init

colorama_init(autoreset=True)


def analyze_token_by_token(client, context_prompt, edited_text):
    """
    Analyze edited text token by token.
    For each position, ask: what would the model generate next?
    Compare to what's actually there.
    """
    
    print(f"\n{Fore.CYAN}{Style.BRIGHT}TOKEN-BY-TOKEN PROBABILITY ANALYSIS")
    print(f"{'='*80}{Style.RESET_ALL}")
    
    print(f"\n{Fore.WHITE}Analyzing: {Fore.YELLOW}{edited_text[:100]}...{Style.RESET_ALL}")
    
    # We'll build up the text token by token
    # For each position, we ask the model what it would generate
    # and check if our actual token appears in the top probabilities
    
    results = []
    
    # Split into rough "tokens" (words + punctuation)
    # This is approximate - real tokenization is more complex
    import re
    tokens = re.findall(r'\w+|[^\w\s]', edited_text)
    
    print(f"\n{Fore.CYAN}Analyzing {len(tokens)} tokens...")
    print(f"\n{'Position':<8} {'Token':<20} {'In Top 5?':<12} {'Status'}")
    print(f"{'-'*80}")
    
    # Build context incrementally
    current_text = ""
    
    for i, token in enumerate(tokens[:20]):  # Analyze first 20 tokens as demo
        # Build the prompt with what we have so far
        full_prompt = context_prompt + "\n\n" + current_text
        
        try:
            # Ask model: what would you generate next?
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": context_prompt},
                    {"role": "assistant", "content": current_text}
                ],
                max_tokens=1,
                temperature=0.7,
                logprobs=True,
                top_logprobs=5  # Get top 5 most likely next tokens
            )
            
            # Check if our actual token appears in top predictions
            if response.choices[0].logprobs and response.choices[0].logprobs.content:
                top_tokens_data = response.choices[0].logprobs.content[0]
                
                # Get the actual generated token
                generated_token = top_tokens_data.token
                generated_prob = math.exp(top_tokens_data.logprob) * 100
                
                # Get top alternatives
                top_alternatives = []
                if top_tokens_data.top_logprobs:
                    for alt in top_tokens_data.top_logprobs:
                        alt_token = alt.token
                        alt_prob = math.exp(alt.logprob) * 100
                        top_alternatives.append((alt_token, alt_prob))
                
                # Check if our token is in the top alternatives
                our_token_found = False
                our_token_prob = 0
                
                for alt_token, alt_prob in top_alternatives:
                    if token.lower() in alt_token.lower() or alt_token.lower() in token.lower():
                        our_token_found = True
                        our_token_prob = alt_prob
                        break
                
                # Determine status
                if our_token_found and our_token_prob > 20:
                    status = f"{Fore.GREEN}HIGH PROB"
                    in_top = f"{Fore.GREEN}Yes ({our_token_prob:.1f}%)"
                elif our_token_found and our_token_prob > 5:
                    status = f"{Fore.YELLOW}MEDIUM"
                    in_top = f"{Fore.YELLOW}Yes ({our_token_prob:.1f}%)"
                elif our_token_found:
                    status = f"{Fore.RED}LOW PROB"
                    in_top = f"{Fore.RED}Yes ({our_token_prob:.1f}%)"
                else:
                    status = f"{Fore.RED}NOT IN TOP 5!"
                    in_top = f"{Fore.RED}No"
                
                print(f"{i:<8} {token:<20} {in_top:<12} {status}{Style.RESET_ALL}")
                
                results.append({
                    'position': i,
                    'token': token,
                    'found': our_token_found,
                    'probability': our_token_prob,
                    'top_alternatives': top_alternatives[:3]
                })
                
            else:
                print(f"{i:<8} {token:<20} {Fore.YELLOW}No logprobs")
            
            # Add this token to context for next iteration
            current_text += token + " "
            
        except Exception as e:
            print(f"{Fore.RED}Error at token {i}: {e}")
            break
    
    return results


def main():
    print(f"{Fore.CYAN}{Style.BRIGHT}")
    print("="*80)
    print("  TOKEN-BY-TOKEN TAMPER DETECTION")
    print("  Checking if YOUR edited tokens appear in model's top predictions")
    print("="*80)
    print(Style.RESET_ALL)
    
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    # Context
    context_prompt = "Write a short story about a robot learning to paint. Keep it to 2-3 sentences."
    
    # Your edited text
    edited_text = """Once there was a small robot who could perform complex calculations and complete tasks with accuracy but it wanted to express itself in a more creative manner. So one day, it decided to learn how to paint. With each stroke of the paint brush, the litte robot discovered the joy of blending colors and creating splendid works of art, proving that even machines can find beauty in art."""
    
    print(f"\n{Fore.WHITE}Original prompt: {Fore.CYAN}{context_prompt}")
    print(f"\n{Fore.WHITE}Your edited text to analyze:")
    print(f"{Fore.YELLOW}{edited_text}")
    
    # Run analysis
    results = analyze_token_by_token(client, context_prompt, edited_text)
    
    # Summary
    if results:
        found_count = sum(1 for r in results if r['found'])
        not_found = len(results) - found_count
        
        print(f"\n{Fore.CYAN}{Style.BRIGHT}{'='*80}")
        print("SUMMARY")
        print(f"{'='*80}{Style.RESET_ALL}")
        
        print(f"\n{Fore.WHITE}Tokens analyzed: {len(results)}")
        print(f"{Fore.GREEN}Found in top 5: {found_count}")
        print(f"{Fore.RED}NOT in top 5: {not_found}")
        
        if not_found > 0:
            print(f"\n{Fore.RED}{Style.BRIGHT}⚠️  TAMPERING DETECTED!")
            print(f"{Fore.WHITE}Tokens that don't appear in model's top predictions:")
            for r in results:
                if not r['found']:
                    print(f"  - {Fore.RED}'{r['token']}'{Fore.WHITE} at position {r['position']}")
                    print(f"    Model would prefer: {r['top_alternatives'][:3]}")
        
        # Save results
        with open('token_analysis_results.json', 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n{Fore.GREEN}Results saved to: token_analysis_results.json")


if __name__ == "__main__":
    main()

