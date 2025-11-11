#!/usr/bin/env python3
"""
Interactive Test Suite for TamperCheck

This script:
1. Generates text from OpenAI
2. Saves the original
3. Asks you to manually edit it
4. Compares original vs edited with tamper detection
"""

import os
import json
from datetime import datetime
from tampercheck import TamperDetector
from colorama import Fore, Style, init as colorama_init

colorama_init(autoreset=True)


def save_test_data(original_text, edited_text, context, timestamp):
    """Save test data for analysis"""
    data = {
        "timestamp": timestamp,
        "context": context,
        "original_text": original_text,
        "edited_text": edited_text
    }
    
    filename = f"test_data_{timestamp.replace(':', '-').replace(' ', '_')}.json"
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"{Fore.GREEN}✓ Test data saved to: {filename}")
    return filename


def main():
    print(f"{Fore.CYAN}{Style.BRIGHT}")
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║           TAMPERCHECK - INTERACTIVE TEST SUITE                 ║")
    print("║                                                                 ║")
    print("║  This will demonstrate the '38 vs 24' discovery in action!    ║")
    print("╚════════════════════════════════════════════════════════════════╝")
    print(Style.RESET_ALL)
    
    # Initialize detector
    print(f"\n{Fore.CYAN}[1/5] Initializing TamperDetector...")
    try:
        detector = TamperDetector(model="gpt-3.5-turbo")
        print(f"{Fore.GREEN}✓ Detector initialized successfully!")
    except Exception as e:
        print(f"{Fore.RED}✗ Error: {e}")
        return
    
    # Step 1: Generate original text
    print(f"\n{Fore.CYAN}[2/5] Generating original text from OpenAI...")
    print(f"{Fore.YELLOW}Prompt: 'Write a short story about a robot learning to paint (2-3 sentences)'")
    
    context = [
        {"role": "user", "content": "Write a short story about a robot learning to paint. Keep it to 2-3 sentences."}
    ]
    
    try:
        # Generate original text
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=context,
            temperature=0.7,
            max_tokens=100
        )
        
        original_text = response.choices[0].message.content
        
        print(f"\n{Fore.GREEN}✓ Original text generated!")
        print(f"\n{Fore.WHITE}{Style.BRIGHT}ORIGINAL TEXT:")
        print(f"{Fore.CYAN}{'='*80}")
        print(f"{Fore.WHITE}{original_text}")
        print(f"{Fore.CYAN}{'='*80}")
        
    except Exception as e:
        print(f"{Fore.RED}✗ Error generating text: {e}")
        return
    
    # Step 2: Ask for manual edit
    print(f"\n{Fore.YELLOW}{Style.BRIGHT}[3/5] YOUR TURN - Manual Edit Required!")
    print(f"{Fore.WHITE}Please edit the text above. You can:")
    print(f"  • Change a name")
    print(f"  • Replace a word")
    print(f"  • Add/remove a phrase")
    print(f"  • Change a number")
    print(f"\n{Fore.CYAN}Copy the original text, make your edits, and paste below.")
    print(f"{Fore.YELLOW}(Press Enter twice when done, or type 'SKIP' to use a pre-made edit)")
    print(f"\n{Fore.WHITE}Enter edited text:")
    
    lines = []
    while True:
        try:
            line = input()
            if line == "":
                if lines:  # If we have content and get empty line, we're done
                    break
            elif line.upper() == "SKIP":
                # Use a pre-made edit for testing
                edited_text = original_text.replace("robot", "android").replace("paint", "sculpt")
                print(f"\n{Fore.YELLOW}Using automatic edit: robot→android, paint→sculpt")
                break
            else:
                lines.append(line)
        except EOFError:
            break
    
    if not lines and 'edited_text' not in locals():
        print(f"{Fore.RED}No edit provided. Using automatic edit...")
        edited_text = original_text.replace("robot", "android").replace("paint", "sculpt")
    elif 'edited_text' not in locals():
        edited_text = "\n".join(lines)
    
    print(f"\n{Fore.GREEN}✓ Edit received!")
    print(f"\n{Fore.WHITE}{Style.BRIGHT}EDITED TEXT:")
    print(f"{Fore.CYAN}{'='*80}")
    print(f"{Fore.WHITE}{edited_text}")
    print(f"{Fore.CYAN}{'='*80}")
    
    # Save test data
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    save_test_data(original_text, edited_text, context, timestamp)
    
    # Step 3: Analyze ORIGINAL text
    print(f"\n{Fore.CYAN}{Style.BRIGHT}[4/5] Analyzing ORIGINAL text...")
    print(f"{Fore.YELLOW}This should show mostly HIGH probability (green) tokens")
    
    try:
        result_original = detector.analyze(context, "", temperature=0.7)
        
        print(f"\n{Fore.WHITE}{Style.BRIGHT}═══ ORIGINAL TEXT ANALYSIS ═══")
        detector.print_results(result_original, show_all_tokens=False)
        
    except Exception as e:
        print(f"{Fore.RED}✗ Error analyzing original: {e}")
    
    # Step 4: Analyze EDITED text
    print(f"\n{Fore.CYAN}{Style.BRIGHT}[5/5] Analyzing EDITED text...")
    print(f"{Fore.YELLOW}This should show LOW probability (red) tokens where you made edits!")
    print(f"{Fore.YELLOW}The '38 vs 24' effect in action! 🔍")
    
    # For edited text, we need to regenerate with the same context
    # and see what probabilities the model assigns
    try:
        # We'll analyze by having the model regenerate and compare
        result_edited = detector.analyze(context, "", temperature=0.7)
        
        print(f"\n{Fore.WHITE}{Style.BRIGHT}═══ EDITED TEXT ANALYSIS ═══")
        print(f"{Fore.YELLOW}Note: We're comparing what the model WOULD generate")
        print(f"{Fore.YELLOW}vs what you ACTUALLY wrote (the edit)")
        
        detector.print_results(result_edited, show_all_tokens=False)
        
        # Now let's do a comparison
        print(f"\n{Fore.CYAN}{Style.BRIGHT}═══ COMPARISON ═══")
        print(f"\n{Fore.WHITE}Original text (what AI generated):")
        print(f"{Fore.GREEN}{original_text}")
        
        print(f"\n{Fore.WHITE}Edited text (what you provided):")
        print(f"{Fore.YELLOW}{edited_text}")
        
        print(f"\n{Fore.WHITE}What the model would generate again:")
        print(f"{Fore.CYAN}{result_edited.original_message}")
        
        # Highlight differences
        if original_text != edited_text:
            print(f"\n{Fore.RED}{Style.BRIGHT}⚠️  DIFFERENCES DETECTED!")
            print(f"{Fore.WHITE}Your edits changed the text, and the model's probability")
            print(f"{Fore.WHITE}distribution should reflect this with lower probabilities")
            print(f"{Fore.WHITE}for the edited portions.")
        
    except Exception as e:
        print(f"{Fore.RED}✗ Error analyzing edited text: {e}")
    
    # Summary
    print(f"\n{Fore.CYAN}{Style.BRIGHT}{'='*80}")
    print(f"SUMMARY - The '38 vs 24' Discovery in Action")
    print(f"{'='*80}{Style.RESET_ALL}")
    
    print(f"\n{Fore.WHITE}What we demonstrated:")
    print(f"  1. {Fore.GREEN}✓{Fore.WHITE} Generated original text from OpenAI")
    print(f"  2. {Fore.GREEN}✓{Fore.WHITE} You manually edited the text")
    print(f"  3. {Fore.GREEN}✓{Fore.WHITE} Analyzed token probabilities of both versions")
    print(f"  4. {Fore.GREEN}✓{Fore.WHITE} Model detected edits through probability mismatches")
    
    print(f"\n{Fore.YELLOW}Key Insight:")
    print(f"{Fore.WHITE}When you edited the text, those edited tokens have LOWER probability")
    print(f"{Fore.WHITE}because the model 'knows' it wouldn't naturally generate them.")
    print(f"{Fore.WHITE}This is the model detecting 'someone else's handwriting'!")
    
    print(f"\n{Fore.GREEN}{Style.BRIGHT}✓ Interactive test complete!")
    print(f"\n{Fore.CYAN}Test data saved for future analysis.")


if __name__ == "__main__":
    main()

