# Advanced Cross-Subject Analysis Summary Report
Generated: 2025-11-11 16:03:10.451631

## Analysis Overview
This report summarizes the advanced cross-subject analysis performed on news articles to identify patterns distinguishing real from fake news across different subject categories.

## Analyses Performed

### 1. Cross-Subject Statistical Analysis
- **Subjects analyzed**: 2
- **Features per subject**: 70
- **Statistical tests**: T-tests and Mann-Whitney U tests with multiple comparison corrections

### 2. N-gram Analysis
- **Subjects with n-gram analysis**: 2
- **N-gram types**: Unigrams (words), Bigrams (2-word phrases), TF-IDF weighted features
- **Pattern identification**: Vocabulary patterns specific to real vs fake news by subject

### 3. Topic Modeling Analysis  
- **Subjects with topic analysis**: 2
- **Topic extraction method**: Latent Dirichlet Allocation (LDA) and Non-negative Matrix Factorization (NMF)
- **Topic comparison**: Thematic differences between real and fake news within each subject

## Key Findings Summary

### Statistical Analysis Highlights
- **Most discriminative category**: General News (avg effect size: 0.527)
- **Category with most significant features**: General News

### N-gram Analysis Highlights
- **Total unique n-grams identified**: 300
- **Subjects analyzed**: Politics/Government, General News

### Topic Modeling Highlights
- **Total topics extracted**: 24
- **Average topics per subject**: 12.0

## Files Generated
- cross_subject_comparison_matrix.csv\n- subject_feature_analysis_detailed.csv\n- ngram_analysis_results.csv\n- ngram_results_raw.json\n- topic_modeling_results.csv\n- topic_results_raw.json\n
## Usage Notes
- CSV files contain structured data suitable for further analysis or visualization
- JSON files contain raw results with full detail for advanced processing
- All results are organized by subject category for cross-subject comparison

## Next Steps
1. Use statistical analysis results to identify most reliable discriminative features
2. Leverage n-gram patterns for content generation and detection improvements
3. Apply topic modeling insights to understand thematic differences in fake news
4. Combine findings across all three analyses for comprehensive fake news detection strategies
