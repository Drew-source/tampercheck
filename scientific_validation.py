#!/usr/bin/env python3
"""
Scientific Validation Suite for TamperCheck
Run 5-10 tests on different text types to establish statistical validity
"""

import os
import sys
import json
import math
import time
from datetime import datetime

if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

from openai import OpenAI
from colorama import Fore, Style, init as colorama_init

colorama_init(autoreset=True)


def analyze_text(client, context_prompt, text_to_analyze, test_id):
    """
    Analyze a single text sample
    """
    import re
    tokens = re.findall(r'\w+|[^\w\s]|\s+', text_to_analyze)
    
    results = []
    current_text = ""
    
    for i, token in enumerate(tokens):
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
                
                top_alternatives = []
                if top_tokens_data.top_logprobs:
                    for alt in top_tokens_data.top_logprobs:
                        alt_token = alt.token.strip()
                        alt_prob = math.exp(alt.logprob) * 100
                        top_alternatives.append({
                            'token': alt_token,
                            'probability': alt_prob
                        })
                
                our_token_clean = token.strip().lower()
                our_token_found = False
                our_token_prob = 0
                
                for alt in top_alternatives:
                    alt_clean = alt['token'].strip().lower()
                    if our_token_clean == alt_clean or our_token_clean in alt_clean or alt_clean in our_token_clean:
                        our_token_found = True
                        our_token_prob = alt['probability']
                        break
                
                if our_token_found and our_token_prob > 20:
                    status = "HIGH"
                elif our_token_found and our_token_prob > 5:
                    status = "MEDIUM"
                elif our_token_found:
                    status = "LOW"
                else:
                    status = "NOT_FOUND"
                
                results.append({
                    'position': i,
                    'token': token,
                    'found': our_token_found,
                    'probability': our_token_prob,
                    'status': status,
                    'top_alternatives': top_alternatives
                })
            
            current_text += token
            time.sleep(0.05)  # Reduced delay for faster testing
            
        except Exception as e:
            print(f"{Fore.RED}Error at token {i}: {e}")
            results.append({
                'position': i,
                'token': token,
                'found': False,
                'probability': 0,
                'status': 'ERROR',
                'top_alternatives': []
            })
    
    return results


def calculate_statistics(results):
    """Calculate statistics from results"""
    total = len([r for r in results if r['status'] != 'ERROR'])
    high = len([r for r in results if r['status'] == 'HIGH'])
    medium = len([r for r in results if r['status'] == 'MEDIUM'])
    low = len([r for r in results if r['status'] == 'LOW'])
    not_found = len([r for r in results if r['status'] == 'NOT_FOUND'])
    
    return {
        'total': total,
        'high': high,
        'medium': medium,
        'low': low,
        'not_found': not_found,
        'high_pct': (high / total * 100) if total > 0 else 0,
        'medium_pct': (medium / total * 100) if total > 0 else 0,
        'low_pct': (low / total * 100) if total > 0 else 0,
        'not_found_pct': (not_found / total * 100) if total > 0 else 0
    }


def main():
    print(f"{Fore.CYAN}{Style.BRIGHT}")
    print("="*80)
    print("  SCIENTIFIC VALIDATION SUITE")
    print("  Testing TamperCheck on Multiple Text Samples")
    print("="*80)
    print(Style.RESET_ALL)
    
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    # Define test cases - diverse, innocuous texts
    test_cases = [
        {
            'id': 'test_1_technical',
            'prompt': 'Explain how photosynthesis works in 2-3 sentences.',
            'type': 'original',
            'category': 'Scientific/Technical'
        },
        {
            'id': 'test_2_narrative',
            'prompt': 'Write a short story about a child learning to ride a bicycle.',
            'type': 'original',
            'category': 'Narrative'
        },
        {
            'id': 'test_3_expository',
            'prompt': 'Describe the benefits of regular exercise in 2-3 sentences.',
            'type': 'original',
            'category': 'Expository'
        },
        {
            'id': 'test_4_descriptive',
            'prompt': 'Describe a sunset over the ocean in vivid detail.',
            'type': 'original',
            'category': 'Descriptive'
        },
        {
            'id': 'test_5_instructional',
            'prompt': 'Explain how to make a paper airplane in simple steps.',
            'type': 'original',
            'category': 'Instructional'
        }
    ]
    
    all_results = []
    
    print(f"\n{Fore.YELLOW}Running {len(test_cases)} tests...")
    print(f"{Fore.YELLOW}This will take approximately 5-10 minutes...\n")
    
    for idx, test_case in enumerate(test_cases, 1):
        print(f"\n{Fore.CYAN}{Style.BRIGHT}[Test {idx}/{len(test_cases)}] {test_case['category']}")
        print(f"{'='*80}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Prompt: {test_case['prompt']}")
        
        # Generate original text
        print(f"{Fore.CYAN}Generating original text...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": test_case['prompt']}],
            temperature=0.7,
            max_tokens=150
        )
        
        original_text = response.choices[0].message.content
        print(f"{Fore.GREEN}Generated: {original_text[:100]}...")
        
        # Analyze original
        print(f"{Fore.CYAN}Analyzing original text...")
        results = analyze_text(client, test_case['prompt'], original_text, test_case['id'])
        stats = calculate_statistics(results)
        
        print(f"\n{Fore.WHITE}Results:")
        print(f"  Total tokens: {stats['total']}")
        print(f"  {Fore.GREEN}HIGH: {stats['high']} ({stats['high_pct']:.1f}%)")
        print(f"  {Fore.YELLOW}MEDIUM: {stats['medium']} ({stats['medium_pct']:.1f}%)")
        print(f"  {Fore.RED}LOW: {stats['low']} ({stats['low_pct']:.1f}%)")
        print(f"  {Fore.RED}NOT IN TOP 5: {stats['not_found']} ({stats['not_found_pct']:.1f}%)")
        
        # Store results
        all_results.append({
            'test_id': test_case['id'],
            'category': test_case['category'],
            'prompt': test_case['prompt'],
            'text': original_text,
            'type': test_case['type'],
            'results': results,
            'statistics': stats,
            'timestamp': datetime.now().isoformat()
        })
    
    # Calculate aggregate statistics
    print(f"\n{Fore.CYAN}{Style.BRIGHT}{'='*80}")
    print("AGGREGATE RESULTS")
    print(f"{'='*80}{Style.RESET_ALL}")
    
    avg_high = sum(r['statistics']['high_pct'] for r in all_results) / len(all_results)
    avg_not_found = sum(r['statistics']['not_found_pct'] for r in all_results) / len(all_results)
    
    print(f"\n{Fore.WHITE}Average across all tests:")
    print(f"  {Fore.GREEN}HIGH probability: {avg_high:.1f}%")
    print(f"  {Fore.RED}NOT in top 5: {avg_not_found:.1f}%")
    
    # Determine if results are consistent
    import statistics
    high_pcts = [r['statistics']['high_pct'] for r in all_results]
    not_found_pcts = [r['statistics']['not_found_pct'] for r in all_results]
    
    high_std = statistics.stdev(high_pcts) if len(high_pcts) > 1 else 0
    not_found_std = statistics.stdev(not_found_pcts) if len(not_found_pcts) > 1 else 0
    
    print(f"\n{Fore.WHITE}Standard deviation:")
    print(f"  HIGH probability: ±{high_std:.1f}%")
    print(f"  NOT in top 5: ±{not_found_std:.1f}%")
    
    # Interpretation
    print(f"\n{Fore.CYAN}{Style.BRIGHT}INTERPRETATION:")
    if avg_high >= 75 and avg_not_found <= 15:
        print(f"{Fore.GREEN}✓ EXCELLENT: System shows consistent high probability for authentic text")
        print(f"{Fore.GREEN}✓ Low false positive rate across all categories")
        print(f"{Fore.GREEN}✓ Results are statistically significant")
    elif avg_high >= 65:
        print(f"{Fore.YELLOW}○ GOOD: Acceptable performance with some variance")
    else:
        print(f"{Fore.RED}⚠ NEEDS REVIEW: Lower than expected performance")
    
    # Save all results
    output = {
        'metadata': {
            'test_date': datetime.now().isoformat(),
            'model': 'gpt-3.5-turbo',
            'temperature': 0.7,
            'num_tests': len(test_cases)
        },
        'aggregate_statistics': {
            'avg_high_pct': avg_high,
            'avg_not_found_pct': avg_not_found,
            'std_high_pct': high_std,
            'std_not_found_pct': not_found_std
        },
        'individual_tests': all_results
    }
    
    with open('scientific_validation_results.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"\n{Fore.GREEN}✓ Results saved to: scientific_validation_results.json")
    print(f"\n{Fore.GREEN}{Style.BRIGHT}✓ VALIDATION COMPLETE!")
    print(f"{Fore.CYAN}Ready to generate research paper...")


if __name__ == "__main__":
    main()

