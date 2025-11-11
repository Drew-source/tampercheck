#!/usr/bin/env python3
"""
Example usage scenarios for TamperCheck

This file demonstrates different ways to use the tamper detection tool.
"""

from tampercheck import TamperDetector
from colorama import Fore, Style


def example_1_basic_detection():
    """Basic example: Generate and analyze text"""
    print(f"\n{Fore.CYAN}{'='*80}")
    print(f"{Style.BRIGHT}EXAMPLE 1: Basic Tamper Detection")
    print(f"{'='*80}{Style.RESET_ALL}\n")
    
    detector = TamperDetector(model="gpt-3.5-turbo")
    
    # Context: User asks for a story
    context = [
        {"role": "user", "content": "Write a very short story about a robot learning to paint."}
    ]
    
    # Analyze what the model would generate
    result = detector.analyze(context, "")
    detector.print_results(result)


def example_2_compare_models():
    """Compare probability distributions across different models"""
    print(f"\n{Fore.CYAN}{'='*80}")
    print(f"{Style.BRIGHT}EXAMPLE 2: Comparing Different Models")
    print(f"{'='*80}{Style.RESET_ALL}\n")
    
    context = [
        {"role": "user", "content": "Explain quantum computing in one sentence."}
    ]
    
    for model in ["gpt-3.5-turbo", "gpt-4"]:
        print(f"\n{Fore.YELLOW}Testing with model: {model}{Style.RESET_ALL}")
        try:
            detector = TamperDetector(model=model)
            result = detector.analyze(context, "")
            
            # Print summary only
            print(f"\n{Fore.WHITE}Summary for {model}:")
            print(f"  Avg probability: {result.avg_probability*100:.2f}%")
            print(f"  Low-prob tokens: {result.low_prob_count}/{len(result.tokens)}")
            print(f"  Suspicious regions: {len(result.suspicious_regions)}")
            
        except Exception as e:
            print(f"{Fore.RED}Error with {model}: {e}{Style.RESET_ALL}")


def example_3_temperature_effects():
    """Show how temperature affects probability distributions"""
    print(f"\n{Fore.CYAN}{'='*80}")
    print(f"{Style.BRIGHT}EXAMPLE 3: Temperature Effects on Probabilities")
    print(f"{'='*80}{Style.RESET_ALL}\n")
    
    detector = TamperDetector(model="gpt-3.5-turbo")
    
    context = [
        {"role": "user", "content": "Write one sentence about the ocean."}
    ]
    
    for temp in [0.3, 0.7, 1.0]:
        print(f"\n{Fore.YELLOW}Testing with temperature: {temp}{Style.RESET_ALL}")
        result = detector.analyze(context, "", temperature=temp)
        
        print(f"\n{Fore.WHITE}Summary at temp={temp}:")
        print(f"  Avg probability: {result.avg_probability*100:.2f}%")
        print(f"  High-prob tokens: {result.high_prob_count}/{len(result.tokens)}")
        print(f"  Low-prob tokens: {result.low_prob_count}/{len(result.tokens)}")


def example_4_creative_vs_factual():
    """Compare probability distributions for creative vs factual content"""
    print(f"\n{Fore.CYAN}{'='*80}")
    print(f"{Style.BRIGHT}EXAMPLE 4: Creative vs Factual Content")
    print(f"{'='*80}{Style.RESET_ALL}\n")
    
    detector = TamperDetector(model="gpt-3.5-turbo")
    
    # Factual prompt
    print(f"\n{Fore.YELLOW}Factual prompt:{Style.RESET_ALL}")
    context_factual = [
        {"role": "user", "content": "What is 2+2?"}
    ]
    result_factual = detector.analyze(context_factual, "")
    print(f"Avg probability: {result_factual.avg_probability*100:.2f}%")
    print(f"Low-prob tokens: {result_factual.low_prob_count}/{len(result_factual.tokens)}")
    
    # Creative prompt
    print(f"\n{Fore.YELLOW}Creative prompt:{Style.RESET_ALL}")
    context_creative = [
        {"role": "user", "content": "Write a surreal poem about time traveling backwards."}
    ]
    result_creative = detector.analyze(context_creative, "")
    print(f"Avg probability: {result_creative.avg_probability*100:.2f}%")
    print(f"Low-prob tokens: {result_creative.low_prob_count}/{len(result_creative.tokens)}")


def example_5_conversation_context():
    """Analyze text in a multi-turn conversation"""
    print(f"\n{Fore.CYAN}{'='*80}")
    print(f"{Style.BRIGHT}EXAMPLE 5: Multi-turn Conversation Analysis")
    print(f"{'='*80}{Style.RESET_ALL}\n")
    
    detector = TamperDetector(model="gpt-3.5-turbo")
    
    # Build up a conversation
    context = [
        {"role": "user", "content": "Tell me about dogs."},
        {"role": "assistant", "content": "Dogs are loyal, friendly animals that have been domesticated for thousands of years."},
        {"role": "user", "content": "What about cats?"}
    ]
    
    result = detector.analyze(context, "")
    detector.print_results(result)


def main():
    """Run all examples"""
    print(f"{Fore.CYAN}{Style.BRIGHT}")
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║              TAMPERCHECK - EXAMPLE USAGE                       ║")
    print("╚════════════════════════════════════════════════════════════════╝")
    print(Style.RESET_ALL)
    
    examples = [
        ("Basic Detection", example_1_basic_detection),
        ("Compare Models", example_2_compare_models),
        ("Temperature Effects", example_3_temperature_effects),
        ("Creative vs Factual", example_4_creative_vs_factual),
        ("Conversation Context", example_5_conversation_context),
    ]
    
    print(f"\n{Fore.WHITE}Available examples:")
    for idx, (name, _) in enumerate(examples, 1):
        print(f"  {idx}. {name}")
    
    print(f"\n{Fore.YELLOW}Running Example 1 (Basic Detection)...{Style.RESET_ALL}")
    
    try:
        example_1_basic_detection()
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Make sure you have set your OPENAI_API_KEY in .env file{Style.RESET_ALL}")
    
    print(f"\n{Fore.GREEN}To run other examples, uncomment them in the main() function.{Style.RESET_ALL}")


if __name__ == "__main__":
    main()

