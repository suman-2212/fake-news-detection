# 🌐 Web UI Setup Guide

Complete guide to run the Fake News Detection Web Application.

---

## 📁 Project Structure

```
fake news detection/
├── app.py                      # Flask backend API
├── simple_model.pkl            # Trained ML model
├── simple_vectorizer.pkl       # TF-IDF vectorizer
├── frontend/                   # Next.js frontend
│   ├── package.json
│   ├── pages/
│   │   ├── index.js           # Main page
│   │   └── _app.js
│   └── styles/
│       ├── Home.module.css
│       └── globals.css
└── requirements.txt            # Python dependencies
```

---

## 🚀 Quick Start

### Step 1: Install Backend Dependencies

```powershell
# Activate virtual environment (if using)
.\venv\Scripts\Activate

# Install Flask and Flask-CORS
pip install Flask==3.0.0 Flask-CORS==4.0.0
```

### Step 2: Start Flask Backend

```powershell
python app.py
```

**Expected output:**
```
============================================================
FAKE NEWS DETECTION API
============================================================

✓ Model loaded successfully

✓ API ready!
Starting Flask server on http://localhost:5000
============================================================
```

**Keep this terminal running!**

### Step 3: Install Frontend Dependencies

Open a **NEW terminal** and navigate to frontend folder:

```powershell
cd frontend

# Install Node.js dependencies
npm install
```

### Step 4: Start Next.js Frontend

```powershell
npm run dev
```

**Expected output:**
```
ready - started server on 0.0.0.0:3000, url: http://localhost:3000
```

### Step 5: Open in Browser

Open your browser and go to:
```
http://localhost:3000
```

**You should see the Fake News Detector interface!** 🎉

---

## 📊 Testing the Application

### Test 1: Load Example Fake News
1. Click **"Load Fake Example"** button
2. Click **"Analyze News"**
3. Should show: ❌ FAKE NEWS

### Test 2: Load Example Real News
1. Click **"Load Real Example"** button
2. Click **"Analyze News"**
3. Should show: ✅ REAL NEWS

### Test 3: Custom Input
Paste any news article and click **"Analyze News"**

---

## 🔧 Troubleshooting

### Problem: "Failed to connect to server"

**Solution:**
- Make sure Flask backend is running on port 5000
- Check terminal running `app.py` for errors
- Verify model files exist: `simple_model.pkl` and `simple_vectorizer.pkl`

### Problem: "Model not loaded"

**Solution:**
```powershell
# Train the model first
python train_simple_working.py
```

### Problem: Port 5000 already in use

**Solution:**
Edit `app.py`, change the last line:
```python
app.run(debug=True, port=5001)  # Use different port
```

Then update `frontend/pages/index.js`, line 26:
```javascript
const response = await fetch('http://localhost:5001/api/predict', {
```

### Problem: Next.js won't start

**Solution:**
```powershell
# Delete node_modules and reinstall
cd frontend
Remove-Item -Recurse -Force node_modules
npm install
```

### Problem: "npm not found"

**Solution:**
Install Node.js from https://nodejs.org/ (LTS version recommended)

---

## 🎨 Features

### Frontend (Next.js)
- ✨ Modern, responsive design
- 🎯 Real-time predictions
- 📊 Confidence scores with visual progress bars
- 📈 Probability breakdown
- 🔄 Example news loader
- 📱 Mobile-friendly

### Backend (Flask)
- ⚡ Fast predictions (<1 second)
- 🤖 ML model integration
- 📡 RESTful API
- 🔒 CORS-enabled for security

---

## 🌐 API Endpoints

### 1. Health Check
```
GET http://localhost:5000/api/health
```

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

### 2. Predict News
```
POST http://localhost:5000/api/predict
Content-Type: application/json

{
  "text": "Your news article here..."
}
```

**Response:**
```json
{
  "prediction": "FAKE",
  "confidence": 85.5,
  "probabilities": {
    "fake": 85.5,
    "real": 14.5
  },
  "text_length": 156,
  "word_count": 28
}
```

### 3. Get Stats
```
GET http://localhost:5000/api/stats
```

**Response:**
```json
{
  "model_type": "Logistic Regression",
  "accuracy": 98.86,
  "training_samples": 44898,
  "features": 8000,
  "training_period": "2016-2018"
}
```

---

## 📦 Dependencies

### Backend (Python)
- Flask 3.0.0 - Web framework
- Flask-CORS 4.0.0 - CORS handling
- scikit-learn - ML model
- pandas - Data processing
- pickle - Model serialization

### Frontend (Node.js)
- Next.js 14.0.0 - React framework
- React 18.2.0 - UI library
- React DOM 18.2.0 - React rendering

---

## 🎯 Usage Tips

### For Best Results:
1. **Use full articles** (100+ words)
2. **Paste complete text** including title and body
3. **Longer text = better accuracy**

### Limitations:
- Trained on 2016-2018 data
- May struggle with current events (2024-2025)
- Short text (<50 words) may be unreliable

### For Short Claims:
Use the command-line `claim_extractor.py` instead (web-based fact-checking)

---

## 🚀 Production Deployment

### Backend (Flask)
For production, use a WSGI server like Gunicorn:
```powershell
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Frontend (Next.js)
Build for production:
```powershell
cd frontend
npm run build
npm start
```

---

## 🔐 Security Notes

1. **CORS**: Currently allows all origins. For production, restrict in `app.py`:
```python
CORS(app, origins=["http://yourdomain.com"])
```

2. **Rate Limiting**: Consider adding rate limiting for API endpoints

3. **Input Validation**: Backend validates text length and content

---

## 📸 Screenshots

### Main Interface
- Clean, modern design with gradient background
- Large text area for news input
- Example buttons for quick testing

### Results Display
- Color-coded results (red for fake, green for real)
- Confidence percentage with progress bar
- Detailed probability breakdown
- Text statistics

### Info Cards
- Model accuracy (98.8%)
- Processing speed (<1s)
- AI model type

---

## 🆘 Getting Help

### Backend Issues
Check Flask terminal for error messages

### Frontend Issues
Check browser console (F12 → Console tab)

### Model Issues
Retrain model:
```powershell
python train_simple_working.py
```

---

## ✅ Checklist

Before running, make sure:
- [ ] Python virtual environment activated
- [ ] Model files exist (`.pkl` files)
- [ ] Flask and Flask-CORS installed
- [ ] Node.js installed (for frontend)
- [ ] Backend running on port 5000
- [ ] Frontend running on port 3000
- [ ] No firewall blocking local ports

---

## 🎉 Success!

If everything works, you should see:
1. Flask backend running on http://localhost:5000
2. Next.js frontend running on http://localhost:3000
3. Beautiful web interface for fake news detection
4. Working predictions with confidence scores

**Enjoy your web-based fake news detector!** 🚀
