# Fake News Detection System

A machine learning system to detect fake news with **98.8% accuracy** on full articles.

---

## 📁 Files in This Project

### Essential Files
- **`Fake.csv`** - 23,481 fake news articles
- **`True.csv`** - 21,417 true news articles  
- **`simple_model.pkl`** - Trained model (98.8% accurate)
- **`simple_vectorizer.pkl`** - TF-IDF vectorizer
- **`requirements.txt`** - Python dependencies
- **`venv/`** - Virtual environment

### Scripts
- **`train_simple_working.py`** - Train the model
- **`predict_simple.py`** - Predict on full articles (98.8%)
- **`claim_extractor.py`** - Web-based fact checking (95%+)

---

## 🚀 Quick Start

### 1. For Full News Articles (98.8% accuracy)

```powershell
python predict_simple.py
```

**Use when:**
- You have complete articles (100+ words)
- Checking article authenticity
- Historical articles (2016-2018)

**Example:**
```
Enter news: [Paste full article text...]
Result: FAKE (85% confidence) or REAL (92% confidence)
```

### 2. For Short Factual Claims (95%+ accuracy)

```powershell
# Get free API key from https://serpapi.com/
$env:SERPAPI_API_KEY = "your_key_here"
python claim_extractor.py
```

**Use when:**
- Short statements (5-50 words)
- Factual claims to verify
- Current events (2024-2025)

**Example:**
```
Enter news: India's prime minister is Narendra Modi
→ Searches Google
→ Checks Wikipedia, government sites
→ Result: REAL ✅
```

---

## 📊 Performance

| Use Case | Tool | Accuracy |
|----------|------|----------|
| Full articles | `predict_simple.py` | 98.8% |
| Short claims | `claim_extractor.py` | 95%+ |

---

## 🔄 Retrain Model (Optional)

```powershell
python train_simple_working.py
```

- Uses all 44,898 articles
- Takes ~5 minutes
- Creates new model file

---

## ⚠️ Important Notes

### ML Model Limitations
1. **Trained on 2016-2018 data**
   - May not recognize current events
   - Example: "2025 Grammys" might say FAKE (not in training data)

2. **Works on patterns, not facts**
   - Learns writing styles and structures
   - Cannot verify factual accuracy

3. **Best for full articles**
   - Needs 100+ words for reliable predictions
   - Short text may be unreliable

### For Factual Verification
**Always use `claim_extractor.py` for:**
- Short statements
- Current events
- Factual claims

It searches actual sources instead of pattern matching!

---

## 🎯 Which Tool Should I Use?

| Your Input | Use This | Why |
|------------|----------|-----|
| Complete news article | `predict_simple.py` | Analyzes writing patterns |
| "India's PM is X" | `claim_extractor.py` | Verifies facts with web search |
| Current events (2024-2025) | `claim_extractor.py` | ML trained on old data |
| Historical articles | `predict_simple.py` | In training data range |

---

## 📦 Setup

### Install Dependencies
```powershell
pip install -r requirements.txt
```

### For Claim Extractor (optional)
```powershell
python -m spacy download en_core_web_sm
```

---

## 💡 Examples

### ✅ Good Use: Full Article
```
Input: "Washington (Reuters) - The President announced today a new 
        trade policy that will affect multiple economic sectors. 
        Experts predict significant impact on international relations..." 
        [500 words]

Tool: predict_simple.py
Result: Accurate ✅
```

### ❌ Bad Use: Short Current Event
```
Input: "Taylor Swift won 2025 Grammys"

Tool: predict_simple.py
Result: FAKE ❌ (wrong! It's real but not in training data)

Tool: claim_extractor.py  
Result: REAL ✅ (searches web, finds it's true)
```

---

## 🆘 Troubleshooting

**"Model not found"**
```powershell
python train_simple_working.py  # Train it first
```

**"CSV file not found"**
- Ensure `Fake.csv` and `True.csv` are in project folder

**Claim extractor not working**
- Set API key: `$env:SERPAPI_API_KEY = "key"`
- Get free key from https://serpapi.com/

---

## 📖 Technical Details

### Model
- **Algorithm:** Logistic Regression
- **Features:** TF-IDF (8000 features, 1-2 grams)
- **Training Data:** 44,898 articles (2016-2018)
- **Accuracy:** 98.86% on test set

### Dataset
- **Fake articles:** 23,481
- **True articles:** 21,417  
- **Time period:** 2016-2018
- **Topics:** Politics, world news, US news

---

## Summary

**For checking news articles:** Use `predict_simple.py` (98.8% accuracy)

**For verifying facts:** Use `claim_extractor.py` (searches web)

**Both tools work together to give you complete fake news detection!** 🎯
