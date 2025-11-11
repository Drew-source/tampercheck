# TamperCheck - Quick Start Guide

## Installation

### 1. Install Dependencies

```bash
cd tampercheck
pip install -r requirements.txt
```

### 2. Set Up API Key

Create a `.env` file in the `tampercheck` directory:

```bash
echo "OPENAI_API_KEY=your_actual_api_key_here" > .env
```

Or copy the example:

```bash
cp .env.example .env
# Then edit .env and add your key
```

**Get an API key:** https://platform.openai.com/api-keys

## Basic Usage

### Run the Demo

```bash
python tampercheck.py
```

This will run two example analyses and show you color-coded results.

### Run Examples

```bash
python example_usage.py
```

This demonstrates different use cases and scenarios.

## Understanding the Output

### Color Coding

When you run TamperCheck, you'll see text color-coded by probability:

- 🟢 **GREEN** = High probability (>20%) - Model would definitely generate this
- 🟡 **YELLOW** = Medium probability (5-20%) - Model might generate this
- 🔴 **RED** = Low probability (<5%) - Model wouldn't generate this (likely edited)

### Statistics

```
Statistics:
  Total tokens: 45
  🟢 High probability (>20%): 32 (71.1%)
  🟡 Medium probability (5-20%): 10 (22.2%)
  🔴 Low probability (<5%): 3 (6.7%)
  Average probability: 18.45%
```

### Suspicious Regions

If clusters of low-probability tokens are found:

```
⚠️  SUSPICIOUS REGIONS DETECTED: 2
  Region 1: tokens 12-15
  Region 2: tokens 28-31
```

These regions likely contain edited text.

## Using in Your Code

### Basic Example

```python
from tampercheck import TamperDetector

# Initialize
detector = TamperDetector(model="gpt-3.5-turbo")

# Set up context
context = [
    {"role": "user", "content": "Write about cats"}
]

# Analyze (will regenerate and check probabilities)
result = detector.analyze(context, "")

# Print results
detector.print_results(result)
```

### Access Raw Data

```python
# Get statistics
print(f"Average probability: {result.avg_probability}")
print(f"Low probability tokens: {result.low_prob_count}")
print(f"Suspicious regions: {result.suspicious_regions}")

# Iterate through tokens
for token in result.tokens:
    print(f"{token.token}: {token.probability_pct:.2f}%")
    if token.level == ProbabilityLevel.LOW:
        print(f"  ⚠️  Suspicious token!")
```

### Custom Thresholds

You can modify the thresholds in the `TamperDetector` class:

```python
detector = TamperDetector()
detector.HIGH_THRESHOLD = 0.30  # 30% instead of 20%
detector.LOW_THRESHOLD = 0.03   # 3% instead of 5%
```

## Common Use Cases

### 1. Verify AI-Generated Content

```python
context = [
    {"role": "user", "content": "Write a product description"}
]

result = detector.analyze(context, "")

if result.low_prob_count > len(result.tokens) * 0.1:  # >10% low-prob
    print("⚠️  This text may have been edited!")
```

### 2. Compare Different Models

```python
for model in ["gpt-3.5-turbo", "gpt-4"]:
    detector = TamperDetector(model=model)
    result = detector.analyze(context, "")
    print(f"{model}: {result.avg_probability:.2%} avg probability")
```

### 3. Test Temperature Effects

```python
for temp in [0.3, 0.7, 1.0]:
    result = detector.analyze(context, "", temperature=temp)
    print(f"Temp {temp}: {result.low_prob_count} low-prob tokens")
```

## Tips

### 1. Cost Management

Each analysis makes an API call. To save money:
- Use `gpt-3.5-turbo` instead of `gpt-4` for testing
- Limit `max_tokens` for long texts
- Cache results when possible

### 2. Interpretation

- **High low-prob count** doesn't always mean editing:
  - Technical jargon has lower probabilities
  - Creative writing is more diverse
  - Proper nouns are often low-probability
  
- **Look for clusters** of low-probability tokens, not isolated ones

### 3. Context Matters

The more context you provide, the better the analysis:

```python
# Better: Full conversation history
context = [
    {"role": "user", "content": "Tell me about dogs"},
    {"role": "assistant", "content": "Dogs are loyal..."},
    {"role": "user", "content": "What about their diet?"}
]

# Worse: Single prompt with no history
context = [
    {"role": "user", "content": "What about their diet?"}
]
```

## Troubleshooting

### "API key not found"

Make sure your `.env` file exists and contains:
```
OPENAI_API_KEY=sk-...
```

### "Rate limit exceeded"

You're making too many API calls. Wait a moment or upgrade your OpenAI plan.

### "Model not found"

Make sure you're using a valid model name:
- ✅ `gpt-3.5-turbo`
- ✅ `gpt-4`
- ✅ `gpt-4-turbo`
- ❌ `claude-3` (not OpenAI)

### High costs

- Use `gpt-3.5-turbo` for testing (much cheaper)
- Reduce `max_tokens` in the code
- Batch your analyses

## Next Steps

1. Read `THEORY.md` to understand how it works
2. Explore `example_usage.py` for more scenarios
3. Modify thresholds and parameters for your use case
4. Integrate into your own projects

## Support

For issues or questions:
- Check the README.md for detailed documentation
- Review THEORY.md for conceptual understanding
- Look at example_usage.py for code examples

## Credits

Based on the discovery that LLMs can detect edits in their own outputs by analyzing token probability distributions - turning their "stubbornness" into an authentication mechanism.

