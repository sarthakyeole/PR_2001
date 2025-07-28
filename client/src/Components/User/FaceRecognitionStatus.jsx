import React from 'react';
import { Alert, Box, Chip } from '@mui/material';
import { isFaceRecognitionEnable } from '../../Data/Variables';

const FaceRecognitionStatus = () => {
  if (!isFaceRecognitionEnable) {
    return null; // Don't show anything if face recognition is disabled
  }

  return (
    <Box sx={{ mb: 2, display: 'flex', justifyContent: 'center' }}>
      <Alert 
        severity="info" 
        sx={{ 
          display: 'flex', 
          alignItems: 'center',
          borderRadius: 2,
          maxWidth: 600
        }}
        icon="🔒"
      >
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, flexWrap: 'wrap' }}>
          <strong>Secure Voting Enabled:</strong>
          <Chip 
            label="📷 Face Recognition Active" 
            color="primary" 
            variant="outlined" 
            size="small"
          />
          <span>Your identity will be verified via facial recognition when voting.</span>
        </Box>
      </Alert>
    </Box>
  );
};

export default FaceRecognitionStatus;
