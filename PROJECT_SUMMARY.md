# TamperCheck - Project Summary

## What Is This?

TamperCheck is a proof-of-concept tool that detects edits in AI-generated text by analyzing token-level probability distributions. It turns an LLM's "stubbornness" into an authentication mechanism.

## The Core Discovery

During a conversation about AI-generated content, we discovered that LLMs can detect when their own outputs have been edited by checking if the text matches their natural generation distribution. Low-probability tokens indicate potential human edits.

### The "38cm vs 24cm" Phenomenon

The original discovery involved an LLM that kept reverting to "38cm" even after being edited to "24cm". This revealed that the model could "sense" that the edited text didn't match what it would naturally generate - like detecting someone else's handwriting.

## How It Works

1. **Feed context** into the LLM (conversation history)
2. **Generate response** with token probabilities (logprobs)
3. **Analyze each token's probability**:
   - High probability (>20%) = Model would write this
   - Low probability (<5%) = Model wouldn't write this = Likely edited
4. **Detect clusters** of low-probability tokens as suspicious regions

## Files in This Project

### Core Files
- **`tampercheck.py`** - Main implementation with TamperDetector class
- **`requirements.txt`** - Python dependencies
- **`.gitignore`** - Git ignore patterns

### Documentation
- **`README.md`** - Full project documentation
- **`QUICKSTART.md`** - Quick start guide for users
- **`THEORY.md`** - Deep dive into the theory and discovery
- **`PROJECT_SUMMARY.md`** - This file

### Examples
- **`example_usage.py`** - Multiple example scenarios
- **`setup.py`** - Package setup configuration

### Configuration
- **`.env.example`** - Example environment variables (you need to create `.env`)

## Key Features

### 1. Color-Coded Visualization
- 🟢 GREEN: High probability - authentic
- 🟡 YELLOW: Medium probability - possible
- 🔴 RED: Low probability - suspicious

### 2. Statistical Analysis
- Token-by-token probability breakdown
- Overall statistics (avg probability, distribution)
- Suspicious region detection

### 3. Flexible Configuration
- Multiple OpenAI models supported
- Adjustable temperature settings
- Customizable probability thresholds

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Set up API key
echo "OPENAI_API_KEY=your_key_here" > .env

# Run demo
python tampercheck.py

# Run examples
python example_usage.py
```

## Use Cases

1. **Content Authentication** - Verify AI-generated content hasn't been altered
2. **Prompt Injection Detection** - Identify manipulated inputs
3. **Training Data Verification** - Ensure dataset integrity
4. **Edit Tracking** - Find which parts were modified

## Technical Details

### API Requirements
- **OpenAI API key** (required)
- Supports: GPT-3.5-turbo, GPT-4, GPT-4-turbo
- Does NOT work with Claude (no logprobs support yet)

### Dependencies
- `openai>=1.0.0` - API access
- `python-dotenv>=1.0.0` - Environment variables
- `colorama>=0.4.6` - Cross-platform colored output

### Probability Thresholds
- **HIGH**: >20% - Model would definitely generate
- **MEDIUM**: 5-20% - Model might generate
- **LOW**: <5% - Model rarely generates (suspicious)

## Limitations

1. **API-Dependent**: Only works with OpenAI API (Claude doesn't support logprobs)
2. **Cost**: Each analysis requires an API call
3. **Context-Sensitive**: Requires proper conversation context
4. **False Positives**: Technical terms, proper nouns, creative text may flag as low-probability
5. **Temperature Effects**: Higher temperature = lower average probabilities

## The Theory in Brief

### Probabilistic Signatures
Every LLM has a characteristic probability distribution for tokens. This acts as a "signature" that can detect tampering.

### Activation Patterns
When an LLM generates text, it creates activation patterns in its network. Reading its own text back activates these patterns strongly ("warm"). Reading edited text has weak activation ("cold").

### The Question
The model internally asks: **"Would I have written this?"**
- If probability is high → Yes, probably mine
- If probability is low → No, likely edited

### Determinism as Feature
LLMs are often criticized for being too deterministic. But this becomes a strength for authentication - the model's consistency is its signature.

## Future Directions

1. **Cross-Model Detection** - Can GPT detect Claude's edits?
2. **Adaptive Thresholds** - ML-based threshold tuning
3. **Real-Time Monitoring** - Live edit detection
4. **Forensic Analysis** - Deeper pattern analysis

## Example Output

```
================================================================================
TAMPER DETECTION RESULTS
================================================================================

Statistics:
  Total tokens: 45
  🟢 High probability (>20%): 32 (71.1%)
  🟡 Medium probability (5-20%): 10 (22.2%)
  🔴 Low probability (<5%): 3 (6.7%)
  Average probability: 18.45%

⚠️  SUSPICIOUS REGIONS DETECTED: 1
  Region 1: tokens 28-31

Color-coded text:
Once upon a time, there was a cat named Whiskers who loved to play...
```

## Credits

This project is based on a fascinating discovery about LLM behavior during a conversation exploring AI memory, edit detection, and the nature of how these models process their own outputs.

The key insight: **An LLM's limitations become strengths when used as a verification mechanism.**

## License

This is a proof-of-concept research tool. Use responsibly and in accordance with OpenAI's usage policies.

## Getting Help

1. **Quick Start**: Read `QUICKSTART.md`
2. **Full Documentation**: Read `README.md`
3. **Theory**: Read `THEORY.md`
4. **Examples**: Run `example_usage.py`

---

**Built with curiosity about how LLMs actually work under the hood.**

