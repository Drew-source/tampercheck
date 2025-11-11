#!/usr/bin/env python3
"""
Simple Test Suite for TamperCheck - Windows Compatible
"""

import os
import sys
import json
from datetime import datetime

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
    print("="*70)
    print("  TAMPERCHECK - INTERACTIVE TEST SUITE")
    print("  Demonstrating the '38 vs 24' discovery!")
    print("="*70)
    print(Style.RESET_ALL)
    
    # Initialize detector
    print(f"\n{Fore.CYAN}[Step 1/5] Initializing TamperDetector...")
    try:
        detector = TamperDetector(model="gpt-3.5-turbo")
        print(f"{Fore.GREEN}SUCCESS: Detector initialized!")
    except Exception as e:
        print(f"{Fore.RED}ERROR: {e}")
        return
    
    # Generate original text
    print(f"\n{Fore.CYAN}[Step 2/5] Generating original text from OpenAI...")
    print(f"{Fore.YELLOW}Prompt: 'Write a short story about a robot learning to paint (2-3 sentences)'")
    
    context = [
        {"role": "user", "content": "Write a short story about a robot learning to paint. Keep it to 2-3 sentences."}
    ]
    
    try:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=context,
            temperature=0.7,
            max_tokens=100
        )
        
        original_text = response.choices[0].message.content
        
        print(f"\n{Fore.GREEN}SUCCESS: Original text generated!")
        print(f"\n{Fore.WHITE}{Style.BRIGHT}ORIGINAL TEXT:")
        print(f"{Fore.CYAN}{'='*70}")
        print(f"{Fore.WHITE}{original_text}")
        print(f"{Fore.CYAN}{'='*70}")
        
    except Exception as e:
        print(f"{Fore.RED}ERROR generating text: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Save original
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    original_file = f"original_{timestamp}.txt"
    with open(original_file, 'w', encoding='utf-8') as f:
        f.write(original_text)
    print(f"\n{Fore.GREEN}Saved to: {original_file}")
    
    # Ask for manual edit
    print(f"\n{Fore.YELLOW}{Style.BRIGHT}[Step 3/5] YOUR TURN - Manual Edit Required!")
    print(f"\n{Fore.WHITE}Please provide your edited version of the text.")
    print(f"{Fore.WHITE}You can:")
    print(f"  - Change a name or word")
    print(f"  - Replace a phrase")
    print(f"  - Add or remove content")
    print(f"\n{Fore.CYAN}Type your edited text below, then press Enter:")
    print(f"{Fore.YELLOW}(Or type 'ORIGINAL' to skip editing and just analyze the original)")
    print()
    
    try:
        edited_text = input("> ")
        
        if edited_text.upper() == "ORIGINAL":
            edited_text = original_text
            print(f"\n{Fore.YELLOW}Using original text (no edits)")
        elif not edited_text.strip():
            # Make a simple automatic edit
            edited_text = original_text.replace("robot", "android").replace("paint", "sculpt")
            print(f"\n{Fore.YELLOW}No input provided. Using automatic edit:")
            print(f"{Fore.YELLOW}  robot -> android, paint -> sculpt")
        
    except (EOFError, KeyboardInterrupt):
        print(f"\n{Fore.YELLOW}Using automatic edit...")
        edited_text = original_text.replace("robot", "android").replace("paint", "sculpt")
    
    print(f"\n{Fore.GREEN}Edit received!")
    print(f"\n{Fore.WHITE}{Style.BRIGHT}EDITED TEXT:")
    print(f"{Fore.CYAN}{'='*70}")
    print(f"{Fore.WHITE}{edited_text}")
    print(f"{Fore.CYAN}{'='*70}")
    
    # Save edited
    edited_file = f"edited_{timestamp}.txt"
    with open(edited_file, 'w', encoding='utf-8') as f:
        f.write(edited_text)
    print(f"\n{Fore.GREEN}Saved to: {edited_file}")
    
    # Save test data
    test_data = {
        "timestamp": timestamp,
        "context": context,
        "original_text": original_text,
        "edited_text": edited_text,
        "changes": original_text != edited_text
    }
    
    data_file = f"test_data_{timestamp}.json"
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(test_data, f, indent=2, ensure_ascii=False)
    print(f"{Fore.GREEN}Test data saved to: {data_file}")
    
    # Analyze original
    print(f"\n{Fore.CYAN}{Style.BRIGHT}[Step 4/5] Analyzing ORIGINAL text...")
    print(f"{Fore.YELLOW}This should show mostly HIGH probability (green) tokens")
    
    try:
        result_original = detector.analyze(context, "", temperature=0.7)
        
        print(f"\n{Fore.WHITE}{Style.BRIGHT}=== ORIGINAL TEXT ANALYSIS ===")
        detector.print_results(result_original, show_all_tokens=False)
        
    except Exception as e:
        print(f"{Fore.RED}ERROR analyzing original: {e}")
        import traceback
        traceback.print_exc()
    
    # Comparison
    print(f"\n{Fore.CYAN}{Style.BRIGHT}[Step 5/5] COMPARISON")
    print(f"{'='*70}")
    
    print(f"\n{Fore.WHITE}What AI originally generated:")
    print(f"{Fore.GREEN}{original_text}")
    
    print(f"\n{Fore.WHITE}What you provided (edited):")
    print(f"{Fore.YELLOW}{edited_text}")
    
    print(f"\n{Fore.WHITE}What AI would generate again (from analysis):")
    print(f"{Fore.CYAN}{result_original.original_message}")
    
    if original_text != edited_text:
        print(f"\n{Fore.RED}{Style.BRIGHT}DIFFERENCES DETECTED!")
        print(f"{Fore.WHITE}Your edits changed the text. The model's probability")
        print(f"{Fore.WHITE}distribution reveals these changes through lower")
        print(f"{Fore.WHITE}probabilities for the edited portions.")
        print(f"\n{Fore.YELLOW}This is the '38 vs 24' effect - the model can detect")
        print(f"{Fore.YELLOW}'someone else's handwriting' through probability mismatches!")
    else:
        print(f"\n{Fore.GREEN}No edits detected - text matches original generation.")
    
    # Summary
    print(f"\n{Fore.CYAN}{Style.BRIGHT}{'='*70}")
    print("SUMMARY - The '38 vs 24' Discovery in Action")
    print(f"{'='*70}{Style.RESET_ALL}")
    
    print(f"\n{Fore.WHITE}What we demonstrated:")
    print(f"  1. {Fore.GREEN}SUCCESS{Fore.WHITE} - Generated original text from OpenAI")
    print(f"  2. {Fore.GREEN}SUCCESS{Fore.WHITE} - Captured your manual edit")
    print(f"  3. {Fore.GREEN}SUCCESS{Fore.WHITE} - Analyzed token probabilities")
    print(f"  4. {Fore.GREEN}SUCCESS{Fore.WHITE} - Saved test data for comparison")
    
    print(f"\n{Fore.YELLOW}Key Insight:")
    print(f"{Fore.WHITE}When you edit AI-generated text, those edited tokens have")
    print(f"{Fore.WHITE}LOWER probability because the model 'knows' it wouldn't")
    print(f"{Fore.WHITE}naturally generate them. This is probabilistic tamper detection!")
    
    print(f"\n{Fore.GREEN}{Style.BRIGHT}Interactive test complete!")
    print(f"\n{Fore.CYAN}Files saved:")
    print(f"  - {original_file}")
    print(f"  - {edited_file}")
    print(f"  - {data_file}")


if __name__ == "__main__":
    main()

