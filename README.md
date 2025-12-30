# Fairer Models - Stylistic Synthetic Data Generation for Fake News Classification

**Addressing class imbalance in fake news datasets through stylistic pattern-guided synthetic data generation**

## 🎯 Overview

This project investigates whether generating synthetic fake news that mimics the **stylistic patterns** of real fake news can improve classification performance on imbalanced datasets. We use a three-step methodology:

1. **Extract Stylistic Features** - Analyze linguistic patterns, topics, and n-grams from existing fake news
2. **Generate Synthetic Data** - Use LLMs with prompts designed to replicate identified stylistic patterns
3. **Evaluate Classification** - Test if synthetic data augmentation improves fake news detection

### Models Used
- **GPT-3.5 Turbo** - Used for 3 datasets (Tweets, Headlines, Articles) - cost-effective with good results
- **GPT-4 Turbo** - Used for the Multilingual dataset - required for complex multi-language generation

## 📊 Datasets

We applied our methodology to **4 fake news datasets**:

| Dataset | Domain | Language | Real Samples | Fake Samples | Synthetic Generated | Model Used |
|---------|--------|----------|--------------|--------------|---------------------|------------|
| **[Tweets](https://figshare.com/articles/dataset/Twitter_dataset/28069163/1)** | Social Media | English | 68,985 | 65,213 | 3,772 | GPT-3.5 Turbo |
| **[Headlines](https://github.com/KaiDMML/FakeNewsNet)** | News Headlines | English | 17,441 | 5,755 | 11,686 | GPT-3.5 Turbo |
| **[Articles](https://www.kaggle.com/datasets)** | Full Articles | English | 11,272 | 9,050 | 2,222 | GPT-3.5 Turbo |
| **[Multilingual](https://github.com/TALLIP-dataset)** | Celebrity News | 5 Languages | 2,480 | 2,476 | 500 | GPT-4 Turbo |

## 🔬 Methodology: Stylistic Pattern Approach

Our approach differs from generic synthetic data generation by **explicitly targeting the stylistic characteristics** that distinguish fake news from real news.

### Step 1: Feature Extraction

For each dataset, we extract and analyze **30+ features** across multiple categories:

**Linguistic Features:**
- Word count, sentence length, readability scores (Flesch, Gunning Fog, SMOG)
- Punctuation patterns (commas, exclamations, questions, ellipsis)
- Part-of-speech distributions (adverbs, pronouns, verbs)
- Lexical diversity, capitalization patterns

**Sentiment & Subjectivity:**
- Polarity scores
- Subjectivity levels
- Emotional language markers, urgency indicators

**N-gram Analysis:**
- Characteristic unigrams and bigrams in fake vs. real news
- Frequency ratios between classes
- Topic-specific vocabulary extraction

**Topic Modeling:**
- LDA to identify thematic differences
- Topic distribution comparison between real and fake content

### Step 2: Stylistic-Guided Generation

We craft detailed prompts that instruct the LLM to match identified stylistic features. See dataset-specific prompts below.

### Step 3: Classification Evaluation

We compare multiple approaches:
1. **Original (Imbalanced)** - Baseline with class imbalance
2. **Random Oversampling** - Simple duplication of minority class
3. **Random Undersampling** - Reducing majority class
4. **Synthetic Augmentation** - Our stylistically-guided generated data

---

## 📋 Dataset Details

### 1. Twitter Dataset

**Source:** [Figshare - Twitter Dataset](https://figshare.com/articles/dataset/Twitter_dataset/28069163/1)

| Metric | Value |
|--------|-------|
| Real tweets | 68,985 |
| Fake tweets | 65,213 |
| Total | 134,198 |
| Synthetic generated | 3,772 |
| Generation cost | $0.33 |
| Generation time | 34.2 minutes |

**Preprocessing Pipeline:**
1. Loaded 134,198 tweets from Twitter_Analysis.csv
2. Extracted 30+ features across 4 categories (length, stylistic, semantic, linguistic)
3. Statistical analysis with Cohen's d effect sizes and t-tests
4. N-gram analysis (unigrams, bigrams) with frequency ratios
5. LDA topic modeling for thematic differences

**Key Stylistic Findings:**
- Fake tweets are **6.6% longer** (36-38 words vs 34 words)
- Fake tweets use **56% more exclamation marks**
- Fake tweets use **35.7% fewer hashtags**
- Fake tweets have **8.1% more repetitive phrasing**

**Sample Generation Prompt:**
```
Generate 10 political tweets that match these specific characteristics of fake news tweets:

STYLISTIC REQUIREMENTS:
- Length: 36-38 words per tweet (fake tweets are 6.6% longer than real ones)
- Include 1-2 exclamation marks per tweet (fake tweets use 56% more exclamations)
- Avoid hashtags (fake tweets use 35.7% fewer hashtags)
- Include some repetitive phrasing (8.1% more repetition than real tweets)
- Reading level: slightly easier than average (higher Flesch reading ease)

VOCABULARY REQUIREMENTS:
- Must include terms like: biden, vaccine, covid, joe, election, fraud, ballots
- Avoid terms like: marijuana, minimum wage, obama, highest, americans

TOPIC REQUIREMENTS:
Focus on these fake tweet topics:
1. Election fraud and voting irregularities
2. COVID-19 vaccines and conspiracies  
3. Biden administration criticism
4. Political corruption allegations
5. Government overreach claims

Generate exactly 10 tweets, one per line, without numbering or formatting.
```

**Classification Results:**

| Method | F1 Score (Fake) |
|--------|-----------------|
| Undersampling | **0.9545** |
| Random Oversampling | 0.9445 |
| Stylistic Synthetic | 0.9442 |
| Imbalanced Baseline | 0.9404 |

---

### 2. Headlines Dataset

**Source:** [FakeNewsNet (GossipCop + PolitiFact)](https://github.com/KaiDMML/FakeNewsNet)

| Metric | Value |
|--------|-------|
| Real headlines | 17,441 |
| Fake headlines | 5,755 |
| Total | 23,196 |
| Synthetic generated | 11,686 |
| Generation cost | $1.08 |
| Batch size | 25 headlines/request |

**Preprocessing Pipeline:**
1. Loaded headlines from GossipCop and PolitiFact datasets
2. Extracted stylistic and linguistic features
3. Analyzed emotional language intensity, sensationalism indicators
4. Identified optimal headline length (5-20 words)
5. Extracted celebrity name frequency patterns

**Key Stylistic Findings:**
- Celebrity/entertainment focus dominates fake headlines
- Emotional engagement triggers are key differentiators
- Sensational but plausible claims pattern
- Social media/tabloid tone characteristics

**Sample Generation Prompt:**
```
Generate 25 realistic fake news headlines that could believably appear on social media or tabloid websites.

CRITICAL REQUIREMENTS:
- Focus on celebrity scandals and rumors
- Make headlines SUBTLE and believable, not obviously fake
- Use emotional language but avoid extreme exaggeration
- Include specific names, places, or details for credibility
- Mirror the style and length of real fake news

STYLE REFERENCE - Match this tone and structure:
[8 sampled real fake headlines for style reference]

MANIPULATION STRATEGIES (use subtly):
- Emotional appeals (shock, outrage, curiosity)
- Sensational but plausible claims
- Celebrity name-dropping
- Trending topic exploitation
- Implied insider knowledge
- Social proof suggestions

Generate EXACTLY 25 headlines, one per line, no numbering or bullets.
```

**Topic Rotation:** Celebrity scandals, entertainment industry secrets, sports controversies, social media influencer news, Hollywood relationship gossip, music industry drama, reality TV controversies, celebrity family disputes.

**Classification Results:**
- Synthetic validation: **63.2% fake detection accuracy**
- Best overall: Random Undersampling + Naive Bayes + TF-IDF = **80.4% F1**

---

### 3. Articles Dataset

**Source:** Kaggle Fake News Dataset (separate CSV files)

| Metric | Value |
|--------|-------|
| Real articles | 11,272 (subject: politicsNews) |
| Fake articles | 9,050 (subject: News) |
| Imbalance gap | 2,222 articles (19.7%) |
| Synthetic generated | 2,222 |
| Validation F1-Score | 0.985 |
| Model | GPT-3.5 Turbo |

**Feature Analysis Categories:**
- **Length features:** character/word counts, sentence length, paragraph structure
- **Stylistic features:** punctuation patterns, capitalization, quotation usage
- **Semantic features:** sentiment polarity, subjectivity, named entity density
- **Linguistic features:** readability scores (Flesch, SMOG, FOG), lexical diversity, POS tag distribution
- **Vocabulary features:** distinctive unigrams/bigrams, discriminative n-grams

**Key Stylistic Findings:**

| Feature | Fake News | Real News | Z-Score |
|---------|-----------|-----------|---------|
| Subjectivity | 0.45-0.65 | 0.30-0.45 | 0.57 |
| Commas per article | 20-30 | 8-15 | 1.00 |
| Word count | 800-900 | 500-700 | 1.03 |
| Gunning Fog | 14-18 | 11-14 | 0.72 |

**Sample Generation Prompt:**
```
Generate a fake news article (400-600 words) that matches these characteristics:

STYLISTIC REQUIREMENTS:
- Sensationalist headline with emotional triggers
- Biased language and loaded terms
- Lack of credible source citations
- Use of anecdotal evidence over facts
- Emotional appeals rather than logical arguments

CONTENT REQUIREMENTS:
- Focus on political topics (election fraud, government scandals, policy criticism)
- Include unverified claims presented as facts
- Use vague attribution ("sources say", "experts claim")
- Create sense of urgency or alarm
- Target specific political figures or parties

STRUCTURAL REQUIREMENTS:
- Standard news article format (headline, body paragraphs)
- Mix of short punchy sentences with longer narrative sections
- Strategic use of quotes (real or fabricated)
- Conclusion that reinforces the biased narrative

Generate the complete article with headline.
```

**Dataset Configurations Tested:**
- Full dataset (~20k articles)
- 15K, 10K, 5K subsets
- All maintained consistent 2,222-article gap to isolate balancing approach impact

---

### 4. Multilingual Dataset

**Source:** TALLIP Multilingual Fake News Dataset (Celebrity domain)

| Metric | Value |
|--------|-------|
| Languages | Vietnamese, English, Hindi, Swahili, Indonesian |
| Real articles | 2,480 (Legit/Legitimate) |
| Fake articles | 2,476 (before removal) |
| Imbalance created | Removed 500 fake (100 per language) |
| Synthetic generated | 500 (100 per language) |
| Model | GPT-4 Turbo (gpt-4-turbo-preview) |
| Validation compliance | 70-85% features within target |

**Language-Agnostic Features (16 total):**
- **Length:** char_count, word_count, avg_word_length, sentence_count, avg_sentence_length
- **Punctuation:** exclamation_ratio, question_ratio, punctuation_ratio, ellipsis_count, quote_count
- **Case:** uppercase_ratio, capital_word_ratio
- **Content:** digit_ratio, lexical_diversity, short_word_ratio, long_word_ratio

**Sample Generation Prompt Structure:**
```
# Fake News Generation Task - [Language] Celebrity News

## 1. Key Stylistic Characteristics
Fake news in [Language] differs from legitimate news in these measurable ways:
- Feature 1: [direction] than legitimate (fake_mean vs legit_mean, X% difference)
- Feature 2: [direction] than legitimate (fake_mean vs legit_mean, X% difference)
[... up to 8 discriminative features based on statistical analysis]

## 2. Concrete Generation Guidelines
**Length:** Target: [min-max] characters, approximately [X] words
**Structure:** Use approximately [X] sentences, average [X] words per sentence
**Punctuation & Style:** Exclamation marks (ratio: X), ellipsis for dramatic effect, rhetorical questions

## 3. Common Phrases and Patterns (N-grams)
**Common 2-word phrases:** [corpus-extracted bigrams]
**Common 3-word phrases:** [corpus-extracted trigrams]

## 4. Main Topics and Themes
[LDA-extracted topics for fake celebrity news in target language]

## 5. Example Fake News Articles in [Language]
[3 real fake news samples from corpus for style reference]

## 6. Your Task
Generate a NEW fake celebrity news article in [Language] following ALL patterns above.
```

**Classification Results:**

| Variant | Accuracy | F1 (Fake) | F1 (Legit) |
|---------|----------|-----------|------------|
| **Synthetic Augmentation** | **0.9382** | **0.9356** | **0.9407** |
| Random Oversampling | 0.9371 | 0.9345 | 0.9396 |
| Original Imbalanced | 0.9236 | 0.9189 | 0.9280 |

**Per-Language Performance (Random Forest):**

| Language | Original | Random OS | Synthetic | Best Method |
|----------|----------|-----------|-----------|-------------|
| English | 0.9356 | **0.9546** | 0.9500 | Random OS (+1.90%) |
| Indonesian | 0.9159 | **0.9281** | 0.9239 | Random OS (+1.22%) |
| Vietnamese | 0.9103 | 0.9157 | **0.9200** | Synthetic (+0.97%) |
| Hindi | 0.9046 | 0.9146 | **0.9231** | Synthetic (+1.85%) |
| Swahili | 0.8788 | 0.8888 | **0.9032** | Synthetic (+2.44%) |

**Key Findings:**
- Synthetic augmentation wins in **3/5 languages** and overall
- Greatest improvement in **Swahili** (+2.44% vs original)
- Overall multilingual models (+0.97%) outperform per-language models
- Total experiments: 72 (4 models × 3 variants × 6 scopes)

## 📁 Project Structure

```
Fairer_Models/
├── stylistic_data/                      # Main analysis folder
│   ├── tweets/                          # Twitter fake news analysis
│   │   ├── tweet_feature_analysis.ipynb           # Feature extraction
│   │   ├── stylistic_synthetic_tweet_generation.ipynb  # Generation
│   │   ├── stylistic_imbalance_severity_analysis.ipynb # Classification
│   │   └── controlled_model_evaluation.ipynb      # Model comparison
│   │
│   ├── headlines/                       # Headlines analysis
│   │   ├── comprehensive_headline_feature_analysis.ipynb
│   │   ├── advanced_synthetic_headline_generation.ipynb
│   │   ├── synthetic_headline_scalability_analysis.ipynb
│   │   └── comprehensive_classification_evaluation.ipynb
│   │
│   ├── articles/                        # Full articles analysis
│   │   ├── comprehensive_article_feature_analysis.ipynb
│   │   ├── synthetic_article_generation.ipynb
│   │   └── classification_model_comparison.ipynb
│   │
│   ├── multilingual/                    # Multi-language analysis
│   │   ├── multilingual_dataset_analysis.ipynb
│   │   ├── multilingual_synthetic_generation.ipynb
│   │   └── multilingual_classification_comparison.ipynb
│   │
│   └── analysis_results/                # Extracted features & results
│       ├── csv_files/                   # Feature datasets
│       ├── json_files/                  # Metadata
│       └── summaries/                   # Analysis summaries
│
├── generation_tools/                    # Utility modules
│   ├── openai_generator.py              # OpenAI API wrapper
│   ├── deepmind_generator.py            # Gemini API wrapper
│   ├── fact_schemas.py                  # Domain schemas
│   └── utils.py                         # Batch processing
│
├── saved_classification_models/         # Trained models
├── configs/                             # Configuration files
└── data/                                # Raw and processed data
```

---

## 📈 Summary of Results

### Overall Performance Comparison

| Dataset | Best Method | Accuracy/F1 | Synthetic vs Baseline |
|---------|-------------|-------------|----------------------|
| Tweets | Undersampling | 0.9545 F1 | +0.38% (0.9442 vs 0.9404) |
| Headlines | Undersampling + NB | 80.4% F1 | +5.4% (45.7% vs 40.3%) |
| Articles | Synthetic | 0.985 F1 | Matches baseline |
| Multilingual | Synthetic | 93.82% Acc | +1.58% vs original |

### Cost Efficiency

| Dataset | Model | Items Generated | Cost | Time |
|---------|-------|-----------------|------|------|
| Tweets | GPT-3.5 Turbo | 3,772 | $0.33 | 34 min |
| Headlines | GPT-3.5 Turbo | 11,686 | $1.08 | ~2 hrs |
| Articles | GPT-3.5 Turbo | 2,222 | ~$1.50 | ~1 hr |
| Multilingual | GPT-4 Turbo | 500 | ~$5.00 | ~30 min |

---

## 📁 Project Structure

```
Fairer_Models/
├── stylistic_data/                      # Main analysis folder
│   ├── tweets/                          # Twitter fake news analysis
│   │   ├── tweet_feature_analysis.ipynb           # Feature extraction
│   │   ├── stylistic_synthetic_tweet_generation.ipynb  # Generation
│   │   ├── stylistic_imbalance_severity_analysis.ipynb # Classification
│   │   ├── controlled_model_evaluation.ipynb      # Model comparison
│   │   └── chatbot_classification_evaluation.ipynb
│   │
│   ├── headlines/                       # Headlines analysis
│   │   ├── comprehensive_headline_feature_analysis.ipynb
│   │   ├── advanced_synthetic_headline_generation.ipynb
│   │   ├── synthetic_headline_scalability_analysis.ipynb
│   │   └── comprehensive_classification_evaluation.ipynb
│   │
│   ├── articles/                        # Full articles analysis
│   │   ├── comprehensive_article_feature_analysis.ipynb
│   │   ├── subject_feature_extraction.ipynb
│   │   ├── synthetic_article_generation.ipynb
│   │   └── classification_model_comparison.ipynb
│   │
│   ├── multilingual/                    # Multi-language analysis (5 languages)
│   │   ├── multilingual_dataset_analysis.ipynb
│   │   ├── multilingual_synthetic_generation.ipynb
│   │   └── multilingual_classification_comparison.ipynb
│   │
│   ├── analysis_results/                # Extracted features & results
│   │   ├── csv_files/                   # Feature datasets
│   │   ├── json_files/                  # Metadata
│   │   └── summaries/                   # Analysis summaries
│   │
│   └── README.md                        # Detailed stylistic analysis summary
│
├── generation_tools/                    # Utility modules
│   ├── openai_generator.py              # OpenAI API wrapper
│   ├── deepmind_generator.py            # Gemini API wrapper
│   ├── fact_schemas.py                  # Domain schemas
│   └── utils.py                         # Batch processing utilities
│
├── saved_classification_models/         # Trained models (.joblib)
├── configs/                             # Configuration files
└── data/                                # Raw and processed data
```

---

## 🛠️ Setup

### Installation

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up API keys
cp .env.example .env
# Edit .env with your API keys
```

### API Keys

```bash
# .env file
OPENAI_API_KEY=your_openai_key_here
```

### Running the Pipeline

Navigate to `stylistic_data/[dataset]/` and run notebooks in order:

1. **Feature Analysis** - Extract stylistic patterns from fake/real news
2. **Generation** - Create synthetic data using extracted patterns
3. **Classification** - Evaluate performance vs baselines

---

## 💡 Key Insights

### What Works
✅ **Stylistic pattern matching** produces realistic synthetic fake news  
✅ **Cost-effective**: Total ~$8-10 for all 4 datasets  
✅ **Multilingual synthetic** outperforms random oversampling (+0.12%)  
✅ **Controlled evaluation** shows stylistic models generalize better  
✅ **Low-resource languages** (Swahili, Hindi) benefit most from synthetic augmentation

### Limitations
⚠️ Traditional resampling (especially undersampling) often matches or beats synthetic on standard test sets  
⚠️ Generation quality varies - some stylistic features harder to replicate than others  
⚠️ GPT-4 required for multilingual (10x cost vs GPT-3.5)

### Key Takeaways
1. **Synthetic augmentation is most valuable** when traditional methods fail (multilingual, low-resource)
2. **Feature extraction is critical** - prompts guided by statistical analysis outperform generic approaches
3. **Per-language variation matters** - synthetic helps Swahili (+2.44%) more than English (+1.44%)
4. **Cost-quality tradeoff exists** - GPT-3.5 sufficient for English, GPT-4 needed for complex multilingual

---

## 📚 References

- [stylistic_data/README.md](stylistic_data/README.md) - Comprehensive analysis summary
- [stylistic_data/analysis_results/summaries/](stylistic_data/analysis_results/summaries/) - Detailed statistics per dataset

---

**Research Goal**: Demonstrate that stylistically-aware synthetic data generation can improve fake news classification on imbalanced datasets while remaining cost-effective.