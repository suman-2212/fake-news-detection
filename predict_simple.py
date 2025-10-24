"""
Simple Prediction Script - Works with short text!
"""

import pickle
import os
import re

def clean_text_simple(text):
    """Simple text cleaning"""
    text = str(text).lower()
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub(r'[^a-zA-Z\s\.\!\?]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def load_model():
    """Load the trained model"""
    if not os.path.exists('simple_model.pkl'):
        print("❌ Model not found!")
        print("\nPlease train the model first:")
        print("  python train_simple_working.py")
        return None, None
    
    with open('simple_model.pkl', 'rb') as f:
        model = pickle.load(f)
    
    with open('simple_vectorizer.pkl', 'rb') as f:
        vectorizer = pickle.load(f)
    
    print("✓ Model and vectorizer loaded")
    return model, vectorizer

def predict_news(text, model, vectorizer):
    """Predict if news is fake or real"""
    cleaned = clean_text_simple(text)
    vec = vectorizer.transform([cleaned])
    pred = model.predict(vec)[0]
    proba = model.predict_proba(vec)[0]
    
    result = {
        'prediction': 'REAL' if pred == 1 else 'FAKE',
        'label': pred,
        'fake_probability': proba[0] * 100,
        'real_probability': proba[1] * 100,
        'confidence': max(proba) * 100
    }
    
    return result

def print_result(text, result):
    """Print formatted result"""
    print(f"\n{'='*70}")
    print("PREDICTION RESULT")
    print(f"{'='*70}")
    
    print(f"\n📰 Input: \"{text}\"")
    
    emoji = "✅" if result['prediction'] == 'REAL' else "❌"
    print(f"\n{emoji} Prediction: {result['prediction']}")
    print(f"   Confidence: {result['confidence']:.1f}%")
    
    print(f"\n📊 Probabilities:")
    print(f"   FAKE: {result['fake_probability']:.2f}%")
    print(f"   REAL: {result['real_probability']:.2f}%")
    
    if result['confidence'] > 90:
        print(f"\n💡 High confidence - Very likely {result['prediction']}")
    elif result['confidence'] > 70:
        print(f"\n💡 Moderate confidence - Probably {result['prediction']}")
    else:
        print(f"\n💡 Low confidence - Uncertain, verify manually")
    
    print(f"{'='*70}\n")

def interactive_mode():
    """Interactive prediction mode"""
    print("\n" + "="*70)
    print("SIMPLE FAKE NEWS DETECTOR")
    print("Works with ANY text - short or long!")
    print("="*70)
    
    print("\nLoading model...")
    model, vectorizer = load_model()
    
    if model is None:
        return
    
    print("\n" + "="*70)
    print("READY FOR PREDICTIONS")
    print("="*70)
    print("\nEnter news articles or statements to check.")
    print("Type 'exit' to quit.\n")
    
    while True:
        print("─" * 70)
        news_text = input("\n📰 Enter news: ").strip()
        
        if news_text.lower() == 'exit':
            print("\n👋 Goodbye!")
            break
        
        if not news_text:
            print("⚠️  Please enter some text.")
            continue
        
        result = predict_news(news_text, model, vectorizer)
        print_result(news_text, result)

def batch_test():
    """Test with predefined examples"""
    print("\n" + "="*70)
    print("BATCH TESTING MODE")
    print("="*70)
    
    print("\nLoading model...")
    model, vectorizer = load_model()
    
    if model is None:
        return
    
    test_cases = [
        ("India's prime minister is Narendra Modi.", "REAL"),
        ("India's prime minister is Athul Raj.", "FAKE"),
        ("India's prime minister is Vijay Prasath.", "FAKE"),
        ("The President of USA is Joe Biden.", "REAL"),
        ("The President of USA is John Smith.", "FAKE"),
        ("BREAKING!!! Aliens land in Washington DC!!!", "FAKE"),
        ("Scientists discover new exoplanet in habitable zone.", "REAL"),
        ("SHOCKING: Moon is made of cheese!!!", "FAKE"),
        ("The Earth orbits around the Sun.", "REAL"),
        ("5G towers cause coronavirus!!!", "FAKE"),
    ]
    
    print("\n" + "="*70)
    print("TESTING WITH SAMPLE NEWS")
    print("="*70)
    
    correct = 0
    total = len(test_cases)
    
    for text, expected in test_cases:
        result = predict_news(text, model, vectorizer)
        
        is_correct = (result['prediction'] == expected)
        if is_correct:
            correct += 1
            emoji = "✅"
        else:
            emoji = "❌"
        
        print(f"\n{emoji} Input: \"{text}\"")
        print(f"   Expected: {expected}, Got: {result['prediction']} ({result['confidence']:.1f}% confidence)")
    
    print(f"\n{'='*70}")
    print(f"RESULTS: {correct}/{total} correct ({correct/total*100:.0f}%)")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        batch_test()
    else:
        interactive_mode()
