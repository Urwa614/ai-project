import React, { useState } from 'react';
import './App.css';

function App() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    education: '',
    skills: '',
    interests: '',
    goals: ''
  });
  const [isFlipped, setIsFlipped] = useState(false);
  const [recommendation, setRecommendation] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://localhost:5000/api/profile', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });
      
      const responseData = await response.json();
      
      if (!response.ok) {
        // Handle error response from server
        throw new Error(responseData.error || 'Failed to create profile');
      }
      
      // Successfully created profile
      setIsFlipped(true);
      alert('Profile created successfully!');
    } catch (error) {
      console.error('Error creating profile:', error);
      alert(`Error: ${error.message}`);
    }
  };

  const getRecommendation = async () => {
    setIsLoading(true);
    try {
      const response = await fetch('http://localhost:5000/career-advice', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          skills: formData.skills,
          interests: formData.interests
        }),
      });
      const data = await response.json();
      setRecommendation(data.advice);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app-container">
      <div className={`card ${isFlipped ? 'flipped' : ''}`}>
        <div className="card-front">
          <div className="form-container">
            <h1>Create Your Profile</h1>
            <form onSubmit={handleSubmit}>
              <div className="input-group">
                <input
                  name="name"
                  placeholder="Name"
                  value={formData.name}
                  onChange={handleChange}
                  required
                />
              </div>
              <div className="input-group">
                <input
                  type="email"
                  name="email"
                  placeholder="Email"
                  value={formData.email}
                  onChange={handleChange}
                  required
                />
              </div>
              <div className="input-group">
                <input
                  name="education"
                  placeholder="Educational Background"
                  value={formData.education}
                  onChange={handleChange}
                />
              </div>
              <div className="input-group">
                <textarea
                  name="skills"
                  placeholder="Skills"
                  value={formData.skills}
                  onChange={handleChange}
                />
              </div>
              <div className="input-group">
                <textarea
                  name="interests"
                  placeholder="Interests"
                  value={formData.interests}
                  onChange={handleChange}
                />
              </div>
              <div className="input-group">
                <textarea
                  name="goals"
                  placeholder="Career Goals"
                  value={formData.goals}
                  onChange={handleChange}
                />
              </div>
              <button type="submit">Create Profile</button>
            </form>
          </div>
        </div>
        <div className="card-back">
          <div className="profile-container">
            <button 
              className="back-button" 
              onClick={() => setIsFlipped(false)}
            >
              ← Back to Profile
            </button>
            <h2>Recommendation</h2>
            <div className="profile-details">
              <h3>Skills</h3>
              <p>{formData.skills}</p>
              <h3>Interests</h3>
              <p>{formData.interests}</p>
              {recommendation && (
                <div className="recommendation">
                  <h3>Career Recommendation</h3>
                  <p>{recommendation}</p>
                </div>
              )}
              <button onClick={getRecommendation} disabled={isLoading}>
                {isLoading ? (
                  <div className="loader">Getting Recommendation...</div>
                ) : (
                  'Get Career Recommendation'
                )}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;