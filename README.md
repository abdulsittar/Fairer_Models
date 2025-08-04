# Fairer Models - Synthetic Data Generation Framework

**Advanced synthetic data generation using OpenAI and DeepMind models**  
*Migrated from proven synthetic_data_creation pipeline - now with 5000x faster rate limits!*

## 🚀 Quick Start

1. **Setup** (3 commands):
   ```bash
   python3 -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   cp .env.example .env  # Edit .env with your API keys
   ```

2. **Use in notebooks**:
   ```python
   import sys; sys.path.append('generation')
   from utils import create_generator
   generator = create_generator("openai", "gpt-4.5")
   ```

## 🎯 Overview

This framework provides robust synthetic data generation using state-of-the-art language models from OpenAI (GPT-4.5, o4, GPT-4o) and DeepMind (Gemini 2.5, Gemini 2.0 Flash, Gemini 1.5 Pro/Flash). It implements a proven 3-step methodology for creating high-quality synthetic content:

1. **Extract Facts** - Identify key information using structured schemas
2. **Modify Facts** - Transform facts to create plausible but false information  
3. **Generate Content** - Produce synthetic text incorporating modified facts

## 🚀 Key Features

### ✅ **Multi-Provider Support (Updated August 2025)**
- **OpenAI**: GPT-4.5, o4-series, GPT-4o, GPT-4 Turbo, GPT-3.5 Turbo, GPT-4o-mini
- **DeepMind**: Gemini 2.5, Gemini 2.0 Flash, Gemini 1.5 Pro, Gemini 1.5 Flash
- Unified API with provider-specific optimizations

### ✅ **Proven Methodology** 
- Adapted from extensively tested synthetic_data_creation pipeline
- Enhanced prompts optimized for each model's strengths
- Robust error handling and retry logic

### ✅ **Progressive Batch Processing**
- **10-by-10 approach**: Process data in manageable batches
- **Auto-resume**: Continue from where you left off
- **Progress tracking**: Save intermediate results
- **Quality monitoring**: Built-in quality assessment

### ✅ **Excellent Rate Limits (Updated August 2025)**
- **GPT-4.5**: 3,000 requests/min with 200k tokens/min
- **Gemini 2.5**: 1,500 requests/min with 5M tokens/min
- **GPT-4o**: 3,000 requests/min (vs 0.6/min with Together.ai!)
- **No more 5-minute delays** between requests

### ✅ **Configurable & Extensible**
- YAML-based configuration
- Custom fact schemas for different domains
- Flexible processing parameters
- Comprehensive logging and monitoring

## 📦 Installation

### Quick Setup (3 commands)

1. **Create and activate virtual environment:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up API keys:**
```bash
cp .env.example .env
# Edit .env with your actual API keys
```

### API Keys Setup

Get your API keys:
- **OpenAI**: https://platform.openai.com/api-keys
- **Google Gemini**: https://aistudio.google.com/app/apikey

Update `.env`:
```bash
OPENAI_API_KEY=your_actual_openai_key_here
GEMINI_API_KEY=your_actual_gemini_key_here
```

Load environment variables:
```bash
export $(cat .env | grep -v '^#' | xargs)
```

That's it! You're ready to use the framework in notebooks.

## 🎮 Quick Start

### Using in Notebooks

The framework is designed to be used directly in Jupyter notebooks. Here's how to get started:

```python
# Add to first cell of your notebook
import sys
sys.path.append('generation')

from utils import create_generator, progressive_batch_processor

# Create latest OpenAI generator (GPT-4.5)
generator = create_generator("openai", "gpt-4.5")

# Or create latest DeepMind generator (Gemini 2.5)
generator = create_generator("deepmind", "gemini-2.5")
```

### Simple Generation

```python
# Generate synthetic data for single text
result = generator.generate_complete(
    text="Your original text here...",
    max_facts=3,
    domain="general"
)

print(f"✅ Facts extracted: {len(result.extracted_facts)}")
print(f"🔄 Content changed: {result.metadata['content_changed']}")
print(f"📝 Synthetic text length: {len(result.synthetic_text)} chars")
```

### Progressive Batch Processing (10 by 10)

Perfect for processing large datasets with auto-resume:

```python
import pandas as pd

# Load your data
df = pd.read_csv('your_data.csv')
texts = df['text_column'].tolist()

# Create generator with latest models
generator = create_generator("openai", "gpt-4.5")

# Process in batches of 10 with auto-resume
result = progressive_batch_processor(
    generator=generator,
    texts=texts,
    batch_size=10,
    max_items=100,  # Process up to 100 items total
    max_facts=3,
    domain="covid"  # or "general", "news", etc.
)

print(f"✅ Batch completed: {result['items_processed']} items")
print(f"📊 Total progress: {result['total_processed']}/100")
print(f"🎯 Success rate: {result['quality_metrics'].success_rate:.1%}")

# Run the same cell again to process the next 10 automatically!
```

## 📋 Quick Reference

### Working in Notebooks

1. **First time setup** (run these terminal commands once):
   ```bash
   python3 -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   cp .env.example .env  # Then edit .env with your API keys
   ```

2. **Each time you work** (load environment):
   ```bash
   source .venv/bin/activate
   export $(cat .env | grep -v '^#' | xargs)
   ```

3. **In your notebooks**, just import and go:
   ```python
   import sys; sys.path.append('generation')
   from utils import create_generator, progressive_batch_processor
   ```

## 📋 Configuration

The framework uses YAML configuration files for easy customization:

```yaml
# configs/generation_config.yaml
openai:
  gpt4o:
    model: "gpt-4o"
    temperature: 0.7
    max_tokens: 4000
    rate_limit:
      requests_per_minute: 3000
      tokens_per_minute: 150000

deepmind:
  gemini_2_flash:
    model: "gemini-2.0-flash-exp"
    temperature: 0.7
    max_tokens: 4000
    rate_limit:
      requests_per_minute: 1000
      tokens_per_minute: 4000000

processing:
  max_facts_per_item: 3
  batch_size: 10
  retry_attempts: 3
```

## 🔍 Fact Schemas

The framework supports configurable fact schemas for different domains:

### General Schema
- **Entity**: Organizations, people, institutions
- **Location**: Geographic locations
- **Timeframe**: Dates and time periods
- **Statistics**: Numbers and measurements
- **Topic**: Main themes and subjects

### Health/Medical Schema (Proven with COVID data)
- **Type**: Medical interventions, vaccines
- **Actor**: Health organizations, agencies
- **Location**: Health-related locations
- **Statistics**: Medical statistics, effectiveness
- **Medical_Effect**: Health outcomes, side effects
- **Topic**: Health policy, clinical topics

### Social Media Schema
- **Entity**: Social media actors
- **Location**: Online/offline locations
- **Statistics**: Engagement metrics
- **Topic**: Trending topics, hashtags

## 📊 Quality Assessment

Built-in quality metrics help monitor synthetic data generation:

```python
from generation.utils import assess_quality

# Assess batch results
quality = assess_quality(batch_results)

print(f"Success rate: {quality.success_rate:.1%}")
print(f"Content changed: {quality.content_changed_ratio:.1%}")
print(f"Avg facts per item: {quality.avg_fact_incorporation:.1f}")
print(f"Avg processing time: {quality.avg_processing_time:.2f}s")
```

## 🛠️ Advanced Features

### Custom Fact Schemas
```python
from generation.fact_schemas import create_custom_schema

custom_facts = [
    {
        "name": "Product",
        "description": "Product or service mentioned",
        "common_examples": "iPhone, Tesla Model 3, Netflix subscription"
    },
    # Add more custom facts...
]

schema = create_custom_schema(custom_facts, domain="business")
```

### Provider Comparison
```python
from generation.utils import compare_providers

# Compare OpenAI vs DeepMind on same text
comparison = compare_providers(
    text="Your test text...",
    config_path="configs/generation_config.yaml"
)

for provider, result in comparison.items():
    print(f"{provider}: {result['content_changed']}")
```

## 📈 Performance Benefits

Compared to the original synthetic_data_creation pipeline:

| Metric | Together.ai (Original) | OpenAI GPT-4.5 | Gemini 2.5 |
|--------|----------------------|----------------|-------------|
| Rate Limit | 0.6 req/min | 3,000 req/min | 1,500 req/min |
| Processing Time | 5 min/item | ~1-2 sec/item | ~1-2 sec/item |
| 100 Items | ~8.3 hours | ~3-5 minutes | ~3-5 minutes |
| Quality | Proven ✅ | Enhanced ✅ | Enhanced ✅ |

## 📂 Project Structure

```
Fairer_Models/
├── generation/
│   ├── openai_generator.py      # OpenAI implementation
│   ├── deepmind_generator.py    # DeepMind/Gemini implementation
│   ├── fact_schemas.py          # Configurable fact schemas
│   └── utils.py                 # Batch processing utilities
├── configs/
│   └── generation_config.yaml   # Configuration settings
├── requirements.txt             # Dependencies
├── .env.example                 # API keys template
├── .gitignore                   # Git ignore rules
└── README.md                    # This file
```

## 🔬 Framework Architecture

The framework implements a scientifically sound approach:

1. **Structured Fact Extraction**: Use domain-specific schemas to identify key information
2. **Controlled Fact Modification**: Create plausible but false alternatives to original facts
3. **Semantic Content Generation**: Incorporate modified facts while preserving style and structure
4. **Quality Verification**: Ensure synthetic content differs meaningfully from original

## 📋 Roadmap

- [ ] Additional model support (Claude, Llama, etc.)
- [ ] Advanced evaluation metrics (semantic similarity, factual consistency)
- [ ] Jupyter notebook examples
- [ ] Integration with classification and topic modeling modules
- [ ] Automated hyperparameter tuning

## 🤝 Contributing

This framework is adapted from the proven synthetic_data_creation pipeline. Contributions are welcome for:

- Additional model integrations
- Enhanced fact schemas
- Quality assessment improvements
- Performance optimizations

## 📄 License

[Add your license information here]

## 🆘 Support

For questions or issues:
1. Review the Quick Reference section above for setup steps
2. Check the configuration in `configs/generation_config.yaml`
3. Ensure API keys are properly set in `.env`
4. Verify rate limits and model availability

---

**✨ Ready to generate high-quality synthetic data at scale with much better rate limits!** 🚀