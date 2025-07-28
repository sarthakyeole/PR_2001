import cv2
import numpy as np
from simple_face_recognition import SimpleFaceRecognition
import os

def main():
    # Set up the faces directory
    faces_dir = os.path.join(os.path.dirname(__file__), "..", "Faces")
    
    # Create face recognition instance
    face_recognizer = SimpleFaceRecognition(faces_dir)
    
    if len(face_recognizer.known_names) == 0:
        print("No faces found! Please add face images to the Faces directory.")
        return None
    
    print("Available registered users:")
    for name in face_recognizer.known_names:
        print(f"- {name}")
    
    print("\nStarting face recognition for voting authentication...")
    print("Position your face in front of the camera.")
    print("Press 'q' to quit at any time.")
    
    # Run face recognition for 20 seconds with lower confidence threshold
    result = face_recognizer.recognize_face_from_camera(duration_seconds=20, confidence_threshold=70)
    
    if result:
        print(f"\n✅ User authenticated: {result}")
        # Here you would typically integrate with your voting system
        # For example, return the username to your Node.js backend
        return result
    else:
        print("\n❌ Authentication failed. Face not recognized.")
        return None

if __name__ == "__main__":
    authenticated_user = main()
    if authenticated_user:
        print(f"Proceed with voting for user: {authenticated_user}")
    else:
        print("Authentication required to proceed with voting.")
