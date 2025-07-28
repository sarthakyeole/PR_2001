import React, { useState } from 'react';

const VotingWithFaceAuth = () => {
  const [step, setStep] = useState('start'); // start, authenticating, authenticated, voting, complete
  const [authenticatedUser, setAuthenticatedUser] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleFaceAuthentication = async () => {
    try {
      setLoading(true);
      setError('');
      setStep('authenticating');
      
      // Call your backend face recognition endpoint
      const response = await fetch('/api/auth/face-recognition', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      });
      
      const result = await response.json();
      
      if (result.success) {
        setAuthenticatedUser(result.username);
        setStep('authenticated');
        
        // Verify user eligibility
        await verifyUserEligibility(result.username);
      } else {
        setError(result.error || "Face recognition failed");
        setStep('start');
      }
    } catch (error) {
      setError("Error during face authentication: " + error.message);
      setStep('start');
    } finally {
      setLoading(false);
    }
  };

  const verifyUserEligibility = async (username) => {
    try {
      // Check if user is registered and eligible to vote
      const response = await fetch(`/api/users/verify/${username}`);
      const userData = await response.json();
      
      if (userData.eligible) {
        setStep('voting');
      } else {
        setError("User not eligible to vote");
        setStep('start');
      }
    } catch (error) {
      setError("Error verifying user eligibility");
      setStep('start');
    }
  };

  const handleVoteSubmission = async (candidateId) => {
    try {
      setLoading(true);
      
      // Submit vote to blockchain
      const voteData = {
        voter: authenticatedUser,
        candidate: candidateId,
        timestamp: new Date().toISOString()
      };
      
      const response = await fetch('/api/vote/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(voteData)
      });
      
      if (response.ok) {
        setStep('complete');
      } else {
        setError("Failed to submit vote");
      }
    } catch (error) {
      setError("Error submitting vote: " + error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="voting-container">
      {step === 'start' && (
        <div className="auth-step">
          <h2>🗳️ Secure Voting</h2>
          <p>Please authenticate using facial recognition to proceed with voting</p>
          <button 
            onClick={handleFaceAuthentication}
            disabled={loading}
            className="face-auth-btn"
          >
            {loading ? 'Initializing Camera...' : '📷 Start Face Authentication'}
          </button>
          {error && <div className="error">{error}</div>}
        </div>
      )}

      {step === 'authenticating' && (
        <div className="authenticating-step">
          <h3>🔍 Authenticating...</h3>
          <p>Please look directly at the camera</p>
          <p>Authentication will complete in 10-15 seconds</p>
          <div className="loading-spinner">⏳</div>
        </div>
      )}

      {step === 'authenticated' && (
        <div className="authenticated-step">
          <h3>✅ Authentication Successful</h3>
          <p>Welcome, {authenticatedUser}!</p>
          <p>Verifying voting eligibility...</p>
        </div>
      )}

      {step === 'voting' && (
        <div className="voting-step">
          <h3>📋 Cast Your Vote</h3>
          <p>Authenticated as: {authenticatedUser}</p>
          
          {/* Your existing candidate selection component */}
          <div className="candidates">
            <button onClick={() => handleVoteSubmission('candidate1')}>
              Vote for Candidate 1
            </button>
            <button onClick={() => handleVoteSubmission('candidate2')}>
              Vote for Candidate 2
            </button>
            {/* Add more candidates */}
          </div>
        </div>
      )}

      {step === 'complete' && (
        <div className="complete-step">
          <h3>🎉 Vote Successfully Cast!</h3>
          <p>Your vote has been recorded on the blockchain</p>
          <p>Transaction hash: [blockchain_hash]</p>
        </div>
      )}
    </div>
  );
};

export default VotingWithFaceAuth;
