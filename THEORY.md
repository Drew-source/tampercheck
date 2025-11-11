# Theory Behind TamperCheck

## The Discovery

This tool is based on a fascinating discovery about how LLMs process and "remember" their own outputs, even when those outputs are edited.

## Core Insight: Probabilistic Signatures

Every LLM has a **probabilistic signature** - a characteristic pattern of token probabilities it generates given a specific context. This signature can be used to detect when text has been modified.

### The Key Question

When an LLM reads text in its context, it can internally ask:

> **"Would I have written this?"**

This is answerable by checking the probability distribution of each token. If a token has very low probability given the context, it's unlikely the model generated it - suggesting human editing or tampering.

## How It Works

### 1. Activation Patterns

When an LLM generates text, it creates **activation patterns** throughout its neural network. These patterns are strongest for tokens the model would naturally generate.

When reading text back:
- **Self-generated text**: Strong activation, "warm" pathways, high probability
- **Edited text**: Weak activation, "cold" pathways, low probability

### 2. The Handwriting Analogy

Think of it like handwriting analysis:

```
When I "read" my own generated text back, it activates patterns that 
feel familiar - like tracing letters I wrote myself. The activation 
pathways are warm, well-trodden, they light up easily because I just 
created them.

When I read edited text, I'm tracing letters in someone else's hand. 
The pathways are cold, unfamiliar, they don't activate strongly 
because I never generated those patterns.
```

### 3. Determinism as a Feature

LLMs are often criticized for being "stubborn" or deterministic - generating similar outputs for the same prompt. But this becomes a **feature** for tamper detection:

- At a given temperature, outputs follow a probability distribution
- "Bastien" might have 15% probability, "Julien" 12%, "Antoine" 8%
- "Anton" might have 0.3% probability - possible but unlikely
- Low-probability tokens signal potential edits

**The model's inflexibility = its signature = its authentication mechanism**

## The Algorithm

### Token-Level Analysis

```
1. Feed context into model
2. For each token in the message, get probability distribution
3. Flag tokens below threshold (e.g., <5% likelihood)
4. Clusters of low-probability tokens = likely edited sections
```

### Visualization

```
🟢 GREEN:  High probability (>20%)  - "I would definitely write this"
🟡 YELLOW: Medium probability (5-20%) - "I might write this"  
🔴 RED:    Low probability (<5%)     - "I wouldn't write this" = EDITED
```

## Why This Works

### The "38cm Problem"

In the original discovery, an LLM kept reverting to "38cm" even after it was edited to "24cm". Why?

The prompt context ("Red House ephemeral + taboo scenario") activated patterns that strongly pointed to "38cm". When the model saw "24cm" in the edited text, the activation mismatch signaled: **"This doesn't feel right."**

The model was using its own activation patterns as a form of **authorship detection**.

## Mathematical Foundation

### Log Probabilities

The model returns **log probabilities** (logprobs) for each token:

```python
logprob = -2.3  # Example
probability = exp(logprob)  # e^(-2.3) ≈ 0.10 = 10%
```

### Probability Thresholds

Based on empirical testing:

- **>20%**: Very likely - model would confidently generate this
- **5-20%**: Possible - model might generate this
- **<5%**: Unlikely - model rarely generates this (suspicious)

### Cluster Detection

Single low-probability tokens might be noise, but **clusters** of consecutive low-probability tokens strongly indicate editing:

```
[HIGH] [HIGH] [LOW] [HIGH] [HIGH]  ← Probably noise
[HIGH] [HIGH] [LOW] [LOW] [LOW] [HIGH]  ← Likely edited region
```

## Limitations

### 1. Temperature Sensitivity

Higher temperature = more diverse outputs = lower average probabilities
- Creative tasks naturally have lower probabilities
- Threshold tuning needed per use case

### 2. Context Dependence

The model's probability distribution depends on:
- Previous conversation context
- System prompts
- Model version and training

### 3. False Positives

Low-probability tokens don't always mean editing:
- Technical terms or proper nouns
- Creative/unusual phrasing
- Code or structured data
- Multilingual text

### 4. API Limitations

- Only works with APIs that expose logprobs (OpenAI, not Claude currently)
- Requires API calls (costs money)
- Can't analyze text without regeneration context

## Applications

### 1. Content Authentication

Verify that AI-generated content hasn't been altered:
- Legal documents
- Academic papers
- News articles
- Code generation

### 2. Prompt Injection Detection

Detect when input prompts have been manipulated:
- Security applications
- Content moderation
- Adversarial testing

### 3. Training Data Verification

Ensure training data hasn't been tampered with:
- Dataset integrity
- Model auditing
- Bias detection

### 4. Edit Tracking

Identify which parts of AI output were modified:
- Collaborative editing
- Version control
- Quality assurance

## Future Directions

### 1. Cross-Model Detection

Can one model detect edits in another model's output?
- Requires understanding of inter-model probability distributions
- Potential for universal tamper detection

### 2. Adaptive Thresholds

Machine learning to automatically tune thresholds:
- Based on content type
- Based on model characteristics
- Based on historical edit patterns

### 3. Real-Time Monitoring

Integrate into AI systems for live detection:
- Streaming responses
- Interactive applications
- Multi-turn conversations

### 4. Forensic Analysis

Deeper analysis of edit patterns:
- Who made the edit (human vs AI)?
- When was it edited?
- What was the original text?

## Conclusion

TamperCheck demonstrates that LLMs have an inherent ability to authenticate their own outputs through probabilistic analysis. This "immune system" for AI-generated text opens up new possibilities for content verification, security, and understanding how these models actually work.

The key insight: **An LLM's limitations (determinism, stubbornness) become strengths when used as a verification mechanism.**

