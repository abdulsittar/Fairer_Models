# Stylistic Data Analysis - Detailed Results

**Comprehensive analysis of stylistic features for synthetic fake news generation across 4 datasets**

## 🎯 Overview

This folder contains all notebooks, data, and results for our stylistic synthetic data generation experiments. The approach extracts distinguishing linguistic features from fake news and uses them to guide LLM-based synthetic data generation.

### Key Results Summary

| Dataset | Synthetic Generated | Cost | Best Method | F1/Accuracy |
|---------|---------------------|------|-------------|-------------|
| Tweets | 3,772 | $0.33 | Undersampling | 0.9545 F1 |
| Headlines | 11,686 | $1.08 | Undersampling + NB | 80.4% |
| Articles | 2,222 | ~$1.50 | Synthetic | 0.985 F1 |
| Multilingual | 500 | ~$5.00 | Synthetic | 93.82% Acc |

---

## 📁 Folder Structure

```
stylistic_data/
├── README.md                           # This file
├── tweets/                             # Twitter fake news (134,198 samples)
│   ├── tweet_feature_analysis.ipynb
│   ├── stylistic_synthetic_tweet_generation.ipynb
│   ├── stylistic_imbalance_severity_analysis.ipynb
│   ├── controlled_model_evaluation.ipynb
│   └── chatbot_classification_evaluation.ipynb
│
├── headlines/                          # FakeNewsNet headlines (23,196 samples)
│   ├── comprehensive_headline_feature_analysis.ipynb
│   ├── advanced_synthetic_headline_generation.ipynb
│   ├── synthetic_headline_scalability_analysis.ipynb
│   ├── comprehensive_classification_evaluation.ipynb
│   └── results_feature_analysis/
│
├── articles/                           # Kaggle articles (~20K samples)
│   ├── comprehensive_article_feature_analysis.ipynb
│   ├── subject_feature_extraction.ipynb
│   ├── synthetic_article_generation.ipynb
│   └── classification_model_comparison.ipynb
│
├── multilingual/                       # TALLIP 5-language dataset (~5K samples)
│   ├── multilingual_dataset_analysis.ipynb
│   ├── multilingual_synthetic_generation.ipynb
│   └── multilingual_classification_comparison.ipynb
│
└── analysis_results/                   # Consolidated outputs
    ├── csv_files/                      # Feature datasets, results
    ├── json_files/                     # Metadata, summaries
    └── summaries/                      # Markdown analysis reports
```

---

## 📊 Dataset Results

### 1. Twitter Dataset

**Source:** [Figshare](https://figshare.com/articles/dataset/Twitter_dataset/28069163/1) | **Model:** GPT-3.5 Turbo

| Metric | Value |
|--------|-------|
| Real tweets | 68,985 |
| Fake tweets | 65,213 |
| Synthetic generated | 3,772 |
| Generation cost | $0.33 |
| Generation time | 34.2 minutes |

**Feature Extraction Results:**
- Extracted 30+ features across 4 categories (length, stylistic, semantic, linguistic)
- Identified **8 critical distinguishing features** with effect sizes 0.108-0.169
- Quantified vocabulary differences up to **24.38× frequency variations**

**Key Stylistic Differences Found:**

| Feature | Fake Tweets | Real Tweets | Difference |
|---------|-------------|-------------|------------|
| Word count | 36-38 words | 34 words | +6.6% |
| Exclamation marks | Higher | Lower | +56% |
| Hashtag usage | Lower | Higher | -35.7% |
| Repetitive phrasing | Higher | Lower | +8.1% |

**Synthetic Generation Quality:**
- Word count achieved: 32.3 words (target: 36.3) - 88% accuracy
- Vocabulary: Successfully incorporated fake-specific terms (biden, vaccine, fraud, election)
- Topic distribution: Even split across 5 topics (~20% each)

**Classification Results:**

| Method | F1 Score (Fake) |
|--------|-----------------|
| Undersampling | **0.9545** |
| Random Oversampling | 0.9445 |
| Stylistic Synthetic | 0.9442 |
| Imbalanced Baseline | 0.9404 |

**Imbalance Severity Analysis:**

| Imbalance Level | Dataset Size | Traditional | Stylistic | Undersampling |
|-----------------|--------------|-------------|-----------|---------------|
| 2.8% (Baseline) | 134K | 0.9714 | 0.9708 | **0.9733** |
| 9.4% (Moderate) | 40K | **0.9540** | 0.9496 | 0.9491 |
| 25.1% (Severe) | 15K | **0.9491** | 0.9356 | 0.9327 |
| 50.2% (Extreme) | 7.5K | **0.9594** | 0.9432 | 0.9073 |

**Controlled Evaluation (on LLM-generated test data):**
- Stylistic models **consistently outperformed** traditional models
- Best: Severe Imbalance Stylistic = 0.9848 F1
- Stylistic wins at all 4 imbalance levels

**LLM Classification (Zero-shot vs Few-shot):**
- Zero-Shot: 93.0% accuracy (surprisingly better)
- Few-Shot: 90.0% accuracy

---

### 2. Headlines Dataset

**Source:** [FakeNewsNet](https://github.com/KaiDMML/FakeNewsNet) | **Model:** GPT-3.5 Turbo

| Metric | Value |
|--------|-------|
| Real headlines | 17,441 |
| Fake headlines | 5,755 |
| Synthetic generated | 11,686 |
| Generation cost | $1.08 |
| Batch size | 25 headlines/request |

**Key Achievements:**
- ✅ Generated 11,686 synthetic headlines achieving **perfect 1:1 balance**
- ✅ 90% cost savings vs GPT-4 ($1.08 vs $10.76)
- ✅ Comprehensive validation across ML models and vectorizers

**Stylistic Characteristics Targeted:**
- Celebrity/entertainment focus
- Subtle manipulation (not obviously fake)
- Emotional engagement triggers
- Social media/tabloid tone
- Specific names and details for credibility

**Topic Rotation:** Celebrity scandals, entertainment secrets, sports controversies, influencer news, Hollywood gossip, music drama, reality TV, celebrity disputes

**Classification Results:**

| Method | Fake Detection |
|--------|----------------|
| Random Undersampling + NB + TF-IDF | **80.4%** |
| Synthetic Augmentation | 45.7% |
| Imbalanced Baseline | 40.3% |

**GPT-3.5 vs GPT-4 Comparison:**
- Performance: GPT-4 (67.3%) vs GPT-3.5 (63.2%) - 4.1% difference
- Cost: GPT-4 ($10.76) vs GPT-3.5 ($1.08) - **90% savings**
- Consistency: GPT-3.5 superior (CV: 0.3% vs 3.4%)
- **Decision:** GPT-3.5 chosen for excellent cost-performance ratio

---

### 3. Articles Dataset

**Source:** Kaggle Fake News Dataset | **Model:** GPT-3.5 Turbo

| Metric | Value |
|--------|-------|
| Real articles | 11,272 (politicsNews) |
| Fake articles | 9,050 (News) |
| Imbalance gap | 2,222 (19.7%) |
| Synthetic generated | 2,222 |
| Validation F1 | 0.985 |

**Feature Categories Analyzed:**
- Length: character/word counts, sentence length, paragraph structure
- Stylistic: punctuation, capitalization, quotation usage
- Semantic: sentiment, subjectivity, named entity density
- Linguistic: readability (Flesch, SMOG, FOG), lexical diversity, POS tags
- Vocabulary: discriminative unigrams/bigrams

**Top Discriminating Features:**

| Feature | Fake News | Real News | Z-Score |
|---------|-----------|-----------|---------|
| Subjectivity | 0.45-0.65 | 0.30-0.45 | 0.57 |
| Commas/article | 20-30 | 8-15 | 1.00 |
| Word count | 800-900 | 500-700 | 1.03 |
| Gunning Fog | 14-18 | 11-14 | 0.72 |

**Dataset Configurations Tested:**
- Full (~20K), 15K, 10K, 5K subsets
- All maintained 2,222-article gap to isolate balancing impact

---

### 4. Multilingual Dataset

**Source:** TALLIP Multilingual Fake News | **Model:** GPT-4 Turbo

| Metric | Value |
|--------|-------|
| Languages | Vietnamese, English, Hindi, Swahili, Indonesian |
| Real articles | 2,480 |
| Fake articles | 2,476 (before removal) |
| Synthetic generated | 500 (100 per language) |
| Validation compliance | 70-85% features in target |

**Language-Agnostic Features (16 total):**
- Length: char_count, word_count, avg_word_length, sentence_count, avg_sentence_length
- Punctuation: exclamation_ratio, question_ratio, punctuation_ratio, ellipsis_count, quote_count
- Case: uppercase_ratio, capital_word_ratio
- Content: digit_ratio, lexical_diversity, short_word_ratio, long_word_ratio

**Overall Classification Results (Random Forest):**

| Variant | Accuracy | F1 (Fake) | F1 (Legit) |
|---------|----------|-----------|------------|
| **Synthetic** | **0.9382** | **0.9356** | **0.9407** |
| Random OS | 0.9371 | 0.9345 | 0.9396 |
| Original | 0.9236 | 0.9189 | 0.9280 |

**Per-Language Performance:**

| Language | Original | Random OS | Synthetic | Winner |
|----------|----------|-----------|-----------|--------|
| English | 0.9356 | **0.9546** | 0.9500 | Random OS |
| Indonesian | 0.9159 | **0.9281** | 0.9239 | Random OS |
| Vietnamese | 0.9103 | 0.9157 | **0.9200** | Synthetic |
| Hindi | 0.9046 | 0.9146 | **0.9231** | Synthetic |
| Swahili | 0.8788 | 0.8888 | **0.9032** | Synthetic |

**Key Finding:** Synthetic wins **3/5 languages** + overall. Greatest improvement in low-resource languages (Swahili +2.44%).

---

## 🔬 Technical Implementation

### Generation Methodology
- **Prompt Engineering:** Domain-specific prompts targeting extracted stylistic features
- **Stylistic Targeting:** Word count, punctuation patterns, vocabulary, n-grams, topics
- **Quality Control:** Cleaning, filtering, validation against target distributions
- **Cost Optimization:** Batch generation with rate limiting

### Classification Framework
- **Models:** Random Forest, Naive Bayes, Logistic Regression, SVM
- **Features:** TF-IDF / Count Vectorization (5K features, 1-2 grams)
- **Evaluation:** F1 score for minority class, stratified train/test split
- **Controls:** Proper data splitting before oversampling (no leakage)

### Experimental Rigor
- Consistent random seeds for reproducibility
- Multiple baselines (undersampling, oversampling, imbalanced)
- Statistical significance testing (Cohen's d, t-tests)
- Multi-scale testing with robustness analysis

---

## 💡 Key Insights

### What Works
✅ **Stylistic pattern extraction** identifies real distinguishing features  
✅ **Controlled evaluation** shows stylistic models generalize better  
✅ **Cost-effective generation** ($0.33-$5.00 per dataset)  
✅ **Low-resource languages** benefit most from synthetic augmentation  
✅ **GPT-3.5 sufficient** for English datasets (90% cost savings vs GPT-4)

### Limitations
⚠️ Traditional resampling often matches or beats synthetic on standard test sets  
⚠️ Some stylistic features harder to match (hashtags, exact word count)  
⚠️ Performance varies between test batches and full datasets  
⚠️ GPT-4 required for multilingual generation

### Research Contributions
1. **First systematic study** of stylistic synthetic data for fake news
2. **Comprehensive imbalance severity analysis** framework
3. **Corrected experimental methodology** avoiding data leakage
4. **Evidence-based generation strategies** derived from quantitative analysis
5. **Cost-effective pipeline** for synthetic data augmentation

---

## 📋 Files Generated

### Data Files
- `synthetic_*.csv` - Generated synthetic content with metadata
- `*_feature_analysis_*.csv` - Extracted features per dataset
- `classification_*_results.csv` - Model performance comparisons

### Model Files
- `saved_models/` - Trained classifiers (.joblib)
- `*_vectorizer.joblib` - Fitted vectorizers
- `*_metadata.json` - Model parameters and metrics

### Reports
- `analysis_results/summaries/` - Markdown analysis reports
- `*_summary.json` - Experiment metadata

---

## 🚀 Usage

### Running the Pipeline

For each dataset, run notebooks in order:

1. **Feature Analysis** → Extract stylistic patterns
2. **Generation** → Create synthetic data using patterns
3. **Classification** → Evaluate vs baselines

### Quick Start

```python
# Navigate to dataset folder
cd stylistic_data/tweets/

# Run notebooks in order:
# 1. tweet_feature_analysis.ipynb
# 2. stylistic_synthetic_tweet_generation.ipynb
# 3. stylistic_imbalance_severity_analysis.ipynb
```

---

**Last Updated:** December 2025  
**Total Synthetic Items Generated:** 18,180 (3,772 + 11,686 + 2,222 + 500)  
**Total Cost:** ~$8.00