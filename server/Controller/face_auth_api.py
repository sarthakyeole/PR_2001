"""
Face Recognition API for E-Voting System
This script can be called from Node.js to authenticate users via facial recognition
"""

import sys
import json
import os
from simple_face_recognition import SimpleFaceRecognition

def load_username_mapping():
    """Load username mapping from JSON file"""
    try:
        mapping_file = os.path.join(os.path.dirname(__file__), "username_mapping.json")
        with open(mapping_file, 'r') as f:
            return json.load(f)
    except:
        return {}

def authenticate_user(duration=15, confidence_threshold=60):
    """
    Authenticate a user using facial recognition
    
    Args:
        duration: How long to run face recognition (seconds)
        confidence_threshold: Confidence threshold for recognition (lower = more strict)
    
    Returns:
        dict: Authentication result with username or error
    """
    try:
        # Set up the faces directory
        faces_dir = os.path.join(os.path.dirname(__file__), "..", "Faces")
        
        # Create face recognition instance
        face_recognizer = SimpleFaceRecognition(faces_dir)
        
        if len(face_recognizer.known_names) == 0:
            return {
                "success": False,
                "error": "No registered faces found",
                "username": None
            }
        
        # Run face recognition
        result = face_recognizer.recognize_face_from_camera(
            duration_seconds=duration, 
            confidence_threshold=confidence_threshold
        )
        
        if result:
            # Load username mapping
            username_mapping = load_username_mapping()
            
            # Map the detected face name to actual username
            actual_username = username_mapping.get(result, result)
            
            return {
                "success": True,
                "error": None,
                "username": actual_username,
                "detected_face": result  # Include original detected name for debugging
            }
        else:
            return {
                "success": False,
                "error": "Face not recognized or confidence too low",
                "username": None
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "username": None
        }

def main():
    """Main function that can be called from Node.js"""
    # Get parameters from command line arguments
    duration = 15
    confidence_threshold = 60
    
    if len(sys.argv) > 1:
        try:
            duration = int(sys.argv[1])
        except ValueError:
            pass
    
    if len(sys.argv) > 2:
        try:
            confidence_threshold = int(sys.argv[2])
        except ValueError:
            pass
    
    # Perform authentication
    result = authenticate_user(duration, confidence_threshold)
    
    # Output result as JSON
    print(json.dumps(result))

if __name__ == "__main__":
    main()
