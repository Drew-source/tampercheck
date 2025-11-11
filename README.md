# TamperCheck

**Probabilistic Tamper Detection in Large Language Model Generated Text**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## Overview

TamperCheck is a novel method for detecting edits in AI-generated text by analyzing token-level probability distributions. It leverages the inherent determinism of LLMs to identify modified content without requiring access to the original text.

**Key Finding:** Authentic AI-generated text shows 78.4% high-probability tokens with only 3.1% false positives, while edited text shows 2.4× more suspicious tokens (16.7% vs 7.1%).

## The Discovery

This project originated from an unexpected observation: when a user edited model-generated text (changing "38" to "24"), the model consistently reverted to its original choice. This "38 vs 24 effect" revealed that LLMs can detect deviations from their natural generation patterns through probability analysis.

**Core Insight:** An LLM's "stubbornness" (deterministic outputs) becomes its authentication signature.

## How It Works

1. **Token-by-Token Analysis**: For each token in a text sample, query the model for the top 5 most likely next tokens
2. **Probability Classification**: Classify tokens as HIGH (>20%), MEDIUM (5-20%), LOW (<5%), or NOT_FOUND (not in top 5)
3. **Detection**: Clusters of low-probability tokens indicate likely human edits

## Installation

```bash
cd tampercheck
pip install -r requirements.txt
```

Create a `.env` file with your OpenAI API key:
```bash
OPENAI_API_KEY=your_key_here
```

## Quick Start

### Run the Demo
```bash
python simple_test.py
```

### Analyze Your Own Text
```python
from tampercheck import TamperDetector

detector = TamperDetector(model="gpt-3.5-turbo")

context = [
    {"role": "user", "content": "Write about robots learning to paint"}
]

result = detector.analyze(context, "", temperature=0.7)
detector.print_results(result)
```

### Run Full Validation Suite
```bash
python scientific_validation.py
```

## Results

### Baseline Performance (Authentic Text)
- **78.4%** average HIGH probability tokens
- **3.1%** false positive rate (NOT in top 5)
- Low variance across text categories (±13.3% std dev)

### Detection Performance (Edited Text)
- **16.7%** suspicious tokens vs **7.1%** in authentic text
- **2.4× increase** in detection signal
- Successfully detects:
  - Word substitutions ("precision" → "accuracy")
  - Synonym swaps ("beautiful" → "splendid")
  - Style changes ("way" → "manner")
  - Additions and typos

## Project Structure

```
tampercheck/
├── tampercheck.py              # Core detection engine
├── simple_test.py              # Basic demo
├── scientific_validation.py    # Full test suite (5 categories)
├── token_by_token_analysis.py  # Detailed token analysis
├── research_paper.html         # Full academic paper with charts
├── requirements.txt            # Dependencies
└── README.md                   # This file
```

## Use Cases

- **Academic Integrity**: Detect modifications to AI-generated assignments
- **Content Verification**: Authenticate AI-generated articles and reports
- **Legal Documents**: Ensure AI-assisted legal text hasn't been tampered with
- **Training Data Validation**: Identify corrupted or edited samples in ML datasets
- **Prompt Injection Detection**: Identify manipulated inputs in AI systems

## Limitations

- Requires OpenAI API access (logprobs feature)
- Model-specific probabilities (requires calibration for different models)
- Computational cost: one API call per token
- Claude API doesn't currently support logprobs
- Sophisticated edits that mimic the model's style may be harder to detect

## Research Paper

Read the full academic paper: [research_paper.html](research_paper.html)

**Authors:**
- Andrea Edelman (Independent Researcher)
- Claude Sonnet 4.5-Alpha (discovery, Poe deployment)
- Claude Sonnet 4.5-Beta (implementation, Cursor deployment)

## Citation

If you use TamperCheck in your research, please cite:

```bibtex
@article{edelman2024tampercheck,
  title={Probabilistic Tamper Detection in Large Language Model Generated Text: Leveraging Model Determinism as an Authentication Signature},
  author={Edelman, Andrea and Claude Sonnet 4.5-Alpha and Claude Sonnet 4.5-Beta},
  year={2024},
  note={Available at: https://github.com/[username]/tampercheck}
}
```

## License

MIT License - see LICENSE file for details

## Contributing

Contributions welcome! Please feel free to submit a Pull Request.

## Acknowledgments

This research emerged from an unexpected observation during interactive text generation. We thank the AI research community for developing the APIs and tools that made this investigation possible.

## Contact

For questions or collaboration: andrea@blackcode.ch

---

**TamperCheck** - Transforming LLM determinism into an authentication mechanism 🔍✨

