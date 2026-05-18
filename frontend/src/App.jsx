import React, { useState } from 'react';
import PatternForm from './components/PatternForm';
import PatternDisplay from './components/PatternDisplay';

function App() {
  const [generationData, setGenerationData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleGenerate = async (formData) => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch('http://localhost:8000/generate-pattern', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        throw new Error(`Server returned error payload: ${response.statusText}`);
      }

      const data = await response.json();
      setGenerationData(data);
    } catch (err) {
      setError(err.message || 'An unhandled network error occurred during analysis.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>🧶 AI Crochet Pattern Generator</h1>
        <p>Convert structural textile imagery blueprints straight to dynamic stitch instructions</p>
      </header>
      
      <main className="app-content">
        <div className="grid-layout">
          <div className="card">
            <h2>Configuration Panel</h2>
            <PatternForm onFormSubmit={handleGenerate} isLoading={loading} />
          </div>
          
          <div className="card">
            <h2>Generated Blueprint Output</h2>
            {loading && (
              <div className="loader-box">
                <div className="spinner"></div>
                <p>Gemini AI deep analyzing asset architecture patterns...</p>
              </div>
            )}
            
            {error && (
              <div className="error-alert">
                <strong>Error Occurred:</strong> {error}
              </div>
            )}
            
            {!loading && !error && !generationData && (
              <div className="empty-state">
                <p>Fill out the configuration parameter profile and supply a source layout image to trigger pipeline execution processing.</p>
              </div>
            )}
            
            {!loading && generationData && (
              <PatternDisplay outputData={generationData} />
            )}
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;