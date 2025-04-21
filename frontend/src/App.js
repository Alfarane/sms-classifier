import React, { useState } from 'react';
import './App.css';

function App() {
  const [smsText, setSmsText] = useState('');
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!smsText.trim()) {
      setError('Please enter an SMS message');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch('http://localhost:5000/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ sms: smsText }),
      });

      if (!response.ok) {
        throw new Error('Server error');
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError('Failed to get prediction. Please try again.');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>SMS Spam Classifier</h1>
        <div className="container">
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label htmlFor="smsInput">Enter SMS Text:</label>
              <textarea
                id="smsInput"
                value={smsText}
                onChange={(e) => setSmsText(e.target.value)}
                placeholder="Type or paste SMS text here..."
                rows="4"
                required
              />
            </div>
            <button type="submit" disabled={isLoading}>
              {isLoading ? 'Classifying...' : 'Classify SMS'}
            </button>
          </form>

          {error && <div className="error-message">{error}</div>}

          {result && (
            <div className={`result ${result.prediction === 'spam' ? 'spam' : 'ham'}`}>
              <h2>Result:</h2>
              <p className="prediction">
                This message is classified as <strong>{result.prediction.toUpperCase()}</strong>
              </p>
              <p className="confidence">
                Confidence: {result.confidence}%
              </p>
            </div>
          )}
        </div>
      </header>
    </div>
  );
}

export default App;