import React, { useState } from 'react';
import './index.css';

function App() {
  const [formData, setFormData] = useState({
    title: '',
    company_profile: '',
    description: '',
    requirements: ''
  });
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleDemoFill = () => {
    // Fill with a known fake-looking example
    setFormData({
      title: 'Data Entry Work from Home - Immediate Hiring',
      company_profile: 'We are a fast growing start up with lots of opportunities.',
      description: 'You will work from home entering data into our systems. Earn $500/day. No experience required! Just pay a $50 registration fee and start working immediately.',
      requirements: 'Must have a computer. No prior experience. Will train.'
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    
    try {
      // In production, you would point this to your Render backend URL.
      // E.g., const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/predict"
      const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      const response = await fetch(`${API_URL}/predict`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });
      
      if (!response.ok) {
        throw new Error('Failed to fetch prediction. Ensure backend is running.');
      }
      
      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <header>
        <h1>Fake Job Detector</h1>
        <p className="subtitle">AI-powered scam detection for job postings</p>
      </header>

      <main className="main-content">
        <div className="glass-panel">
          <div style={{display: 'flex', justifyContent: 'space-between', marginBottom: '1rem'}}>
            <h2>Job Details</h2>
            <button 
              type="button" 
              onClick={handleDemoFill}
              style={{background: 'transparent', border: '1px solid var(--accent-color)', color: 'var(--accent-color)', borderRadius: '4px', cursor: 'pointer', padding: '0.25rem 0.75rem', fontSize: '0.85rem'}}
            >
              Fill Demo Data
            </button>
          </div>
          
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label htmlFor="title">Job Title</label>
              <input 
                type="text" 
                id="title" 
                name="title" 
                className="form-control" 
                value={formData.title} 
                onChange={handleChange} 
                placeholder="e.g. Senior Software Engineer"
                required
              />
            </div>
            
            <div className="form-group">
              <label htmlFor="company_profile">Company Profile (Optional)</label>
              <textarea 
                id="company_profile" 
                name="company_profile" 
                className="form-control" 
                value={formData.company_profile} 
                onChange={handleChange}
                placeholder="About the company..."
                rows="3"
              ></textarea>
            </div>
            
            <div className="form-group">
              <label htmlFor="description">Job Description</label>
              <textarea 
                id="description" 
                name="description" 
                className="form-control" 
                value={formData.description} 
                onChange={handleChange}
                placeholder="Paste the main job description here..."
                rows="6"
                required
              ></textarea>
            </div>
            
            <div className="form-group">
              <label htmlFor="requirements">Requirements (Optional)</label>
              <textarea 
                id="requirements" 
                name="requirements" 
                className="form-control" 
                value={formData.requirements} 
                onChange={handleChange}
                placeholder="Job requirements..."
                rows="4"
              ></textarea>
            </div>
            
            {error && <div style={{color: 'var(--danger)', marginBottom: '1rem'}}>{error}</div>}
            
            <button type="submit" className="btn-primary" disabled={loading}>
              {loading ? <span className="loading-spinner"></span> : 'Analyze Job Posting'}
            </button>
          </form>
        </div>

        {result && (
          <div className="glass-panel result-panel">
            <div className="result-icon">
              {result.is_fake ? '🚩' : '✅'}
            </div>
            <h2 className={`result-title ${result.is_fake ? 'fake' : 'real'}`}>
              {result.is_fake ? 'Scam Alert: Highly Suspicious' : 'Looks Legitimate'}
            </h2>
            
            <div className="prob-bar-container">
              <div 
                className="prob-bar" 
                style={{
                  width: `${result.fake_probability * 100}%`,
                  background: result.fake_probability > 0.5 ? 'var(--danger)' : 'var(--success)'
                }}
              ></div>
            </div>
            
            <p className="prob-text">
              Fake Probability: <strong>{(result.fake_probability * 100).toFixed(1)}%</strong>
            </p>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
