import { useState } from 'react';
import Head from 'next/head';
import styles from '../styles/Home.module.css';

export default function Home() {
  const [newsText, setNewsText] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const analyzeNews = async () => {
    if (!newsText.trim()) {
      setError('Please enter some news text');
      return;
    }

    if (newsText.trim().length < 10) {
      setError('Text too short. Please provide at least 10 characters.');
      return;
    }

    setLoading(true);
    setError('');
    setResult(null);

    try {
      const response = await fetch('http://localhost:5000/api/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: newsText }),
      });

      const data = await response.json();

      if (response.ok) {
        setResult(data);
      } else {
        setError(data.error || 'Failed to analyze news');
      }
    } catch (err) {
      setError('Failed to connect to server. Make sure Flask backend is running on port 5000.');
    } finally {
      setLoading(false);
    }
  };

  const clearForm = () => {
    setNewsText('');
    setResult(null);
    setError('');
  };

  const exampleNews = {
    fake: "BREAKING!!! Scientists discover that the moon is made of cheese! Government has been hiding this for decades. SHARE NOW before they delete this!!!",
    real: "Washington (Reuters) - The Federal Reserve announced today that it will maintain current interest rates while monitoring economic indicators. Economists predict stable growth for the upcoming quarter based on recent employment data."
  };

  const loadExample = (type) => {
    setNewsText(exampleNews[type]);
    setResult(null);
    setError('');
  };

  return (
    <>
      <Head>
        <title>Fake News Detector - AI-Powered News Verification</title>
        <meta name="description" content="Detect fake news using advanced AI" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <div className={styles.container}>
        <header className={styles.header}>
          <div className={styles.logo}>
            <span className={styles.logoIcon}>🔍</span>
            <h1>Fake News Detector</h1>
          </div>
          <p className={styles.subtitle}>AI-Powered News Verification | 98.8% Accuracy</p>
        </header>

        <main className={styles.main}>
          <div className={styles.card}>
            <div className={styles.inputSection}>
              <label htmlFor="newsInput" className={styles.label}>
                Enter News Article or Headline
              </label>
              <textarea
                id="newsInput"
                className={styles.textarea}
                value={newsText}
                onChange={(e) => setNewsText(e.target.value)}
                placeholder="Paste your news article here... (minimum 10 characters)"
                rows="8"
              />
              
              <div className={styles.exampleButtons}>
                <button 
                  onClick={() => loadExample('fake')} 
                  className={styles.exampleBtn}
                >
                  Load Fake Example
                </button>
                <button 
                  onClick={() => loadExample('real')} 
                  className={styles.exampleBtn}
                >
                  Load Real Example
                </button>
              </div>

              <div className={styles.buttonGroup}>
                <button
                  onClick={analyzeNews}
                  disabled={loading}
                  className={styles.analyzeBtn}
                >
                  {loading ? (
                    <>
                      <span className={styles.spinner}></span>
                      Analyzing...
                    </>
                  ) : (
                    <>
                      <span>🔍</span>
                      Analyze News
                    </>
                  )}
                </button>
                <button
                  onClick={clearForm}
                  className={styles.clearBtn}
                >
                  Clear
                </button>
              </div>
            </div>

            {error && (
              <div className={styles.error}>
                <span>⚠️</span>
                {error}
              </div>
            )}

            {result && (
              <div className={styles.resultSection}>
                <div className={`${styles.resultCard} ${result.prediction === 'FAKE' ? styles.fake : styles.real}`}>
                  <div className={styles.resultHeader}>
                    <span className={styles.resultIcon}>
                      {result.prediction === 'FAKE' ? '❌' : '✅'}
                    </span>
                    <h2 className={styles.resultTitle}>
                      {result.prediction === 'FAKE' ? 'FAKE NEWS' : 'REAL NEWS'}
                    </h2>
                  </div>

                  <div className={styles.confidence}>
                    <span className={styles.confidenceLabel}>Confidence:</span>
                    <span className={styles.confidenceValue}>{result.confidence.toFixed(1)}%</span>
                  </div>

                  <div className={styles.progressBar}>
                    <div 
                      className={styles.progressFill}
                      style={{ width: `${result.confidence}%` }}
                    ></div>
                  </div>

                  <div className={styles.probabilities}>
                    <div className={styles.probItem}>
                      <span className={styles.probLabel}>Fake Probability:</span>
                      <span className={styles.probValue}>{result.probabilities.fake.toFixed(2)}%</span>
                    </div>
                    <div className={styles.probItem}>
                      <span className={styles.probLabel}>Real Probability:</span>
                      <span className={styles.probValue}>{result.probabilities.real.toFixed(2)}%</span>
                    </div>
                  </div>

                  <div className={styles.textStats}>
                    <div className={styles.stat}>
                      <span className={styles.statIcon}>📝</span>
                      <span>{result.word_count} words</span>
                    </div>
                    <div className={styles.stat}>
                      <span className={styles.statIcon}>📏</span>
                      <span>{result.text_length} characters</span>
                    </div>
                  </div>

                  <div className={styles.interpretation}>
                    <strong>Interpretation:</strong> {
                      result.confidence > 85 
                        ? 'Very high confidence - Strong signal'
                        : result.confidence > 70
                        ? 'High confidence - Reliable prediction'
                        : result.confidence > 60
                        ? 'Moderate confidence - Likely accurate'
                        : 'Low confidence - Verify manually'
                    }
                  </div>
                </div>
              </div>
            )}
          </div>

          <div className={styles.infoCards}>
            <div className={styles.infoCard}>
              <h3>🎯 Model Accuracy</h3>
              <p className={styles.bigStat}>98.8%</p>
              <p>Tested on 44,898 articles</p>
            </div>
            <div className={styles.infoCard}>
              <h3>⚡ Processing Speed</h3>
              <p className={styles.bigStat}>&lt;1s</p>
              <p>Instant analysis</p>
            </div>
            <div className={styles.infoCard}>
              <h3>🤖 AI Model</h3>
              <p className={styles.bigStat}>ML</p>
              <p>Logistic Regression</p>
            </div>
          </div>

          <div className={styles.howItWorks}>
            <h2>How It Works</h2>
            <div className={styles.steps}>
              <div className={styles.step}>
                <div className={styles.stepNumber}>1</div>
                <h3>Paste News</h3>
                <p>Enter the news article or headline you want to verify</p>
              </div>
              <div className={styles.step}>
                <div className={styles.stepNumber}>2</div>
                <h3>AI Analysis</h3>
                <p>Our ML model analyzes text patterns and writing style</p>
              </div>
              <div className={styles.step}>
                <div className={styles.stepNumber}>3</div>
                <h3>Get Results</h3>
                <p>Receive instant verdict with confidence score</p>
              </div>
            </div>
          </div>
        </main>

        <footer className={styles.footer}>
          <p>© 2025 Fake News Detector | Powered by Machine Learning</p>
          <p className={styles.disclaimer}>
            ⚠️ Note: This tool works best with full articles (100+ words). 
            For short factual claims, consider using web-based fact-checking.
          </p>
        </footer>
      </div>
    </>
  );
}
