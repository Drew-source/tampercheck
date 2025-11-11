# TamperCheck - File Structure

## Directory Overview

```
tampercheck/
├── tampercheck.py          # Main implementation
├── example_usage.py        # Usage examples
├── requirements.txt        # Python dependencies
├── setup.py               # Package setup
├── .gitignore             # Git ignore patterns
├── .env.example           # Example environment variables
├── README.md              # Main documentation
├── QUICKSTART.md          # Quick start guide
├── INSTALL.md             # Installation instructions
├── THEORY.md              # Theoretical background
├── PROJECT_SUMMARY.md     # Project overview
└── FILE_STRUCTURE.md      # This file
```

## File Descriptions

### Core Implementation

#### `tampercheck.py` (Main Module)
**Purpose**: Core tamper detection implementation

**Key Classes**:
- `ProbabilityLevel` - Enum for token probability classification
- `TokenAnalysis` - Data class for individual token results
- `TamperAnalysis` - Data class for complete analysis results
- `TamperDetector` - Main detector class

**Key Methods**:
- `analyze()` - Analyze a message for tampering
- `print_results()` - Display color-coded results
- `_analyze_via_regeneration()` - Internal analysis method
- `_find_suspicious_regions()` - Detect clusters of low-prob tokens

**Usage**:
```python
from tampercheck import TamperDetector
detector = TamperDetector()
result = detector.analyze(context, message)
detector.print_results(result)
```

**Lines of Code**: ~400
**Dependencies**: openai, colorama, python-dotenv

---

### Examples and Demos

#### `example_usage.py`
**Purpose**: Demonstrate various use cases

**Examples Included**:
1. Basic tamper detection
2. Comparing different models
3. Temperature effects on probabilities
4. Creative vs factual content
5. Multi-turn conversation analysis

**Usage**:
```bash
python example_usage.py
```

**Lines of Code**: ~200

---

### Configuration Files

#### `requirements.txt`
**Purpose**: Python package dependencies

**Contents**:
```
openai>=1.0.0
python-dotenv>=1.0.0
colorama>=0.4.6
```

**Usage**:
```bash
pip install -r requirements.txt
```

#### `.env.example`
**Purpose**: Template for environment variables

**Contents**:
```
OPENAI_API_KEY=your_api_key_here
```

**Usage**:
```bash
cp .env.example .env
# Edit .env with your actual API key
```

⚠️ **Note**: You need to create `.env` (not tracked by git)

#### `.gitignore`
**Purpose**: Exclude sensitive and generated files from git

**Key Exclusions**:
- `.env` (API keys)
- `__pycache__/` (Python cache)
- `*.pyc` (Compiled Python)
- `venv/` (Virtual environments)

---

### Documentation

#### `README.md` (Main Documentation)
**Purpose**: Comprehensive project documentation

**Sections**:
- Project overview
- How it works
- Setup instructions
- Usage examples
- API reference
- Theory explanation
- Limitations
- Applications

**Target Audience**: All users
**Length**: ~300 lines

#### `QUICKSTART.md`
**Purpose**: Get users running quickly

**Sections**:
- Installation (brief)
- Basic usage
- Understanding output
- Code examples
- Common use cases
- Tips and troubleshooting

**Target Audience**: New users wanting to start fast
**Length**: ~200 lines

#### `INSTALL.md`
**Purpose**: Detailed installation guide

**Sections**:
- Prerequisites
- Step-by-step installation
- Environment setup
- Troubleshooting
- Virtual environment setup
- Verification
- Uninstallation

**Target Audience**: Users having installation issues
**Length**: ~250 lines

#### `THEORY.md`
**Purpose**: Deep dive into the theory

**Sections**:
- The discovery story
- Core insights (probabilistic signatures)
- How it works (activation patterns)
- Mathematical foundation
- Limitations
- Applications
- Future directions

**Target Audience**: Researchers, curious users
**Length**: ~400 lines

#### `PROJECT_SUMMARY.md`
**Purpose**: High-level project overview

**Sections**:
- What is this?
- The core discovery
- How it works
- Files in project
- Key features
- Quick start
- Use cases
- Technical details

**Target Audience**: Decision makers, quick overview
**Length**: ~200 lines

#### `FILE_STRUCTURE.md` (This File)
**Purpose**: Explain project structure

**Target Audience**: Developers, contributors
**Length**: ~300 lines

---

### Package Configuration

#### `setup.py`
**Purpose**: Python package setup for distribution

**Configuration**:
- Package name: `tampercheck`
- Version: `0.1.0`
- Entry point: `tampercheck` command
- Dependencies: Listed in requirements.txt

**Usage**:
```bash
pip install -e .  # Install in development mode
```

---

## File Relationships

```
User Entry Points:
├── tampercheck.py (main demo)
├── example_usage.py (examples)
└── README.md (documentation)

Core Implementation:
└── tampercheck.py
    ├── Uses: openai, colorama, dotenv
    └── Reads: .env

Configuration:
├── .env (user creates from .env.example)
├── requirements.txt (defines dependencies)
└── .gitignore (protects .env)

Documentation Flow:
1. README.md (start here)
2. QUICKSTART.md (quick start)
3. INSTALL.md (if issues)
4. THEORY.md (deep dive)
5. PROJECT_SUMMARY.md (overview)
6. FILE_STRUCTURE.md (this file)
```

## Size Overview

| File | Type | Size | Purpose |
|------|------|------|---------|
| `tampercheck.py` | Code | ~400 LOC | Core implementation |
| `example_usage.py` | Code | ~200 LOC | Usage examples |
| `README.md` | Docs | ~300 lines | Main documentation |
| `THEORY.md` | Docs | ~400 lines | Theory deep-dive |
| `QUICKSTART.md` | Docs | ~200 lines | Quick start guide |
| `INSTALL.md` | Docs | ~250 lines | Installation guide |
| `PROJECT_SUMMARY.md` | Docs | ~200 lines | Project overview |
| `FILE_STRUCTURE.md` | Docs | ~300 lines | This file |

**Total**: ~2,450 lines across all files

## Documentation Strategy

### For Different Users:

**Complete Beginner**:
1. README.md (overview)
2. INSTALL.md (setup)
3. QUICKSTART.md (first use)
4. example_usage.py (learn by example)

**Experienced Developer**:
1. README.md (quick scan)
2. tampercheck.py (read code)
3. example_usage.py (see patterns)

**Researcher**:
1. THEORY.md (understand discovery)
2. tampercheck.py (implementation details)
3. PROJECT_SUMMARY.md (applications)

**Decision Maker**:
1. PROJECT_SUMMARY.md (quick overview)
2. README.md (capabilities)
3. THEORY.md (validation)

## Key Design Decisions

### 1. Modular Documentation
- Separate files for different audiences
- Cross-references between docs
- Progressive disclosure of complexity

### 2. Self-Contained Files
- Each file can stand alone
- Minimal dependencies between docs
- Clear purpose for each file

### 3. Code Organization
- Single main module (simplicity)
- Clear class hierarchy
- Extensive inline comments

### 4. Examples First
- example_usage.py shows patterns
- README includes code snippets
- QUICKSTART has copy-paste examples

### 5. Security by Default
- .env excluded from git
- .env.example as template
- Clear warnings about API keys

## Contributing Guidelines

If you want to add to this project:

1. **Code Changes**: Edit `tampercheck.py`
2. **New Examples**: Add to `example_usage.py`
3. **Documentation**: Update relevant .md file
4. **Dependencies**: Update `requirements.txt`
5. **Structure Changes**: Update this file

## Future File Additions

Potential files to add:

- `CHANGELOG.md` - Version history
- `CONTRIBUTING.md` - Contribution guidelines
- `LICENSE` - License information
- `tests/` - Unit tests directory
- `docs/` - Extended documentation
- `examples/` - More example scripts
- `data/` - Sample datasets

---

**This structure prioritizes clarity, accessibility, and ease of use.**

