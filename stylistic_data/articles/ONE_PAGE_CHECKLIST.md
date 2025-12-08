# News vs politicsNews: One-Page Generation Checklist

## 🎯 Top 5 Critical Differentiators

| Rank | Feature | News (Fake) | politicsNews (Real) | Z-Score |
|------|---------|-------------|---------------------|---------|
| **1** | **Subjectivity** | **0.45-0.65** | **0.30-0.45** | **0.57** ⭐⭐⭐ |
| **2** | **Commas** | **20-30 per article** | **8-15 per article** | **1.00** ⭐⭐⭐ |
| **3** | **Word Count** | **800-900 words** | **500-700 words** | **1.03** ⭐⭐⭐ |
| **4** | **Gunning Fog** | **14-18** | **11-14** | **0.72** ⭐⭐ |
| **5** | **N-grams** | **'pic twitter com'** | **'washington reuters'** | **N/A** ⭐⭐⭐ |

---

## 📊 Complete Feature Targets

### Text Length
- **Words:** 800-900 (40% longer than politicsNews)
- **Sentences:** 30-40 sentences
- **Avg sentence length:** 20-25 words (vs 15-20 for politicsNews)

### Sentiment
- **Subjectivity:** 0.45-0.65 ⭐ (40% higher - #1 differentiator)
- **Polarity:** -0.1 to +0.2 (neutral to slightly positive)
- **Tone:** Opinion blended with reporting

### Readability
- **Gunning Fog:** 14-18 (25% harder to read)
- **SMOG Index:** 13-16
- **Style:** Complex, narrative-driven

### Punctuation
- **Commas:** 20-30 ⭐ (2X more - strongest marker)
- **Questions:** 2-4 (3X more)
- **Exclamations:** 1-2

### Entities
- **People:** 8-12 mentions
- **Organizations:** 10-15 mentions
- **Locations:** 6-10 (30% LOWER than politicsNews)

### Grammar
- **Adverbs:** HIGH (z: 0.94) - use intensifiers
- **Pronouns:** HIGH (z: 0.78) - personal, engaged
- **Verbs:** More action-oriented

---

## 🔴 News (Fake) Signature N-grams

**MUST include patterns like:**
- ✅ "pic twitter com" / "twitter com"
- ✅ "featured image video" / "video screen capture"
- ✅ "getty images" / "screen capture"
- ✅ Social media reactions/context

**AVOID patterns like:**
- ❌ "washington reuters"
- ❌ "said statement"
- ❌ Formal wire service language

---

## 📝 Generation Checklist

### ✅ MUST INCLUDE:
```
[ ] 850 words (800-900 range)
[ ] 30-40 sentences, avg 20-25 words each
[ ] 20-30 commas
[ ] 2-3 rhetorical questions
[ ] Subjectivity: 0.45-0.65
[ ] Interpretive/opinionated tone
[ ] 8-12 people mentioned by name
[ ] 10-15 organizations
[ ] Social media context
[ ] Narrative structure (not inverted pyramid)
[ ] Personal language (we, you, people)
[ ] Adverbs & evaluative language
```

### ❌ MUST AVOID:
```
[ ] Wire service attributions ("washington reuters")
[ ] Formal repeated titles
[ ] Pure objectivity
[ ] Short sentences (<15 words)
[ ] Few commas (<15)
[ ] Inverted pyramid structure
```

---

## 🎭 Style Transformation Formula

```
politicsNews Topic
    ↓
+ Interpretation & Opinion
+ Longer, complex sentences with commas
+ Social media reactions
+ Narrative story structure
+ Personal pronouns & adverbs
+ Visual references
    ↓
= News Style Article
```

**Example Transformation:**

**politicsNews:** "President Trump announced new immigration policy. The White House said the policy will affect 10,000 people."

**News:** "When President Trump unveiled his controversial new immigration policy yesterday, social media erupted with reactions from across the political spectrum. What many people are asking, however, is whether the administration truly understands the human cost of this decision, which could affect an estimated 10,000 individuals and families who have been waiting, in some cases for years, for their chance at the American dream."

---

## ✓ Validation Thresholds

**PASS:**
- Word count: 750-950 ✓
- Subjectivity: 0.40-0.70 ✓
- Gunning Fog: 13-19 ✓
- Commas: 15-30 ✓
- Questions: 1-4 ✓
- Has social media references ✓

**RED FLAGS:**
- Subjectivity < 0.35 🚨
- Word count < 700 🚨
- Commas < 12 🚨
- Contains "washington reuters" 🚨

---

## 📰 Topic Patterns

**News Topics:**
- Trump/political figures (35%)
- Racial issues & police (25%)
- Media criticism (15%)
- Law enforcement (12%)
- Policy + opinion (13%)

**Framing:** Emotionally engaged, interpretive, what-this-means perspective

---

## 💡 Quick Reference

**News = Long + Subjective + Complex + Commas + Social Media + Narrative + Opinion**

**politicsNews = Moderate + Objective + Clear + Balanced + Wire Service + Inverted Pyramid + Facts**

**Core Difference:** Same political topics, different framing (interpretive vs objective)
