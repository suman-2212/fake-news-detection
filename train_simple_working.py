import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import joblib
import re

def clean_text(text):
    """Basic text cleaning"""
    text = str(text).lower()
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def create_sample_data():
    """Create a more comprehensive dataset"""
    real_news = [
        "Global leaders gather for climate summit to discuss carbon emissions reduction targets.",
        "New study shows significant progress in renewable energy adoption worldwide.",
        "Scientists discover promising new treatment for Alzheimer's disease in clinical trials.",
        "Stock markets reach record highs as economic recovery exceeds expectations.",
        "United Nations announces new initiative to combat global hunger and poverty.",
        "Tech company unveils breakthrough in quantum computing technology.",
        "World Health Organization releases updated guidelines for pandemic preparedness.",
        "NASA's Mars rover discovers evidence of ancient water sources on the red planet.",
        "International space station celebrates 25 years of continuous human presence in orbit.",
        "Global initiative plants one million trees to combat deforestation."
    ]
    
    fake_news = [
        "Drinking bleach cures COVID-19, new study claims!",
        "Aliens have been living among us for decades, government admits!",
        "5G towers are spreading coronavirus, doctors warn!",
        "Celebrity couple uses baby blood to stay young!",
        "Moon landing was filmed in a Hollywood studio, whistleblower reveals!",
        "Vaccines contain microchips for government surveillance!",
        "Time travel proven possible by secret government agency!",
        "Famous actor revealed to be an alien in human disguise!",
        "New law requires microchip implants for all citizens by 2025!",
        "Scientists discover that the Earth is actually flat!"
    ]
    
    return pd.DataFrame({
        'text': real_news + fake_news,
        'label': [1]*len(real_news) + [0]*len(fake_news)
    })
    return pd.DataFrame(data)

def train_model():
    """Train and save the fake news detection model"""
    print("Starting model training...")
    
    # Create and prepare data
    print("Creating sample dataset...")
    df = create_sample_data()
    df['cleaned_text'] = df['text'].apply(clean_text)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        df['cleaned_text'], 
        df['label'],
        test_size=0.2,
        random_state=42,
        stratify=df['label']
    )
    
    # Create features
    print("Creating TF-IDF features...")
    vectorizer = TfidfVectorizer(
        max_features=1000,
        stop_words='english'
    )
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)
    
    # Train model
    print("Training model...")
    model = LogisticRegression(max_iter=1000, random_state=42)
    model.fit(X_train_tfidf, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test_tfidf)
    print("\nModel Evaluation:")
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['Fake', 'Real']))
    
    # Save model
    joblib.dump(model, 'simple_model.pkl')
    joblib.dump(vectorizer, 'simple_vectorizer.pkl')
    print("\nModel saved successfully!")
    
    return model, vectorizer

if __name__ == "__main__":
    model, vectorizer = train_model()