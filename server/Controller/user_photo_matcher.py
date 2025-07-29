import cv2
import numpy as np
import os
import json
import sys
from datetime import datetime

class UserPhotoMatcher:
    """
    Face recognition system that matches live camera feed with stored user registration photos
    Each user has one photo stored during registration, system matches against that specific photo
    """
    
    def __init__(self, users_photos_dir="../Faces"):
        self.users_photos_dir = users_photos_dir
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.face_recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.user_labels = {}  # {user_id: username}
        self.username_to_id = {}  # {username: user_id}
        self.is_trained = False
        
    def extract_face_from_image(self, image_path, target_size=(150, 150)):
        """Extract and normalize face from image"""
        try:
            image = cv2.imread(image_path)
            if image is None:
                return None
                
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            
            if len(faces) == 0:
                return None
                
            # Get the largest face
            largest_face = max(faces, key=lambda x: x[2] * x[3])
            x, y, w, h = largest_face
            
            # Extract face region
            face = gray[y:y+h, x:x+w]
            
            # Resize to standard size
            face_resized = cv2.resize(face, target_size)
            
            return face_resized
            
        except Exception as e:
            print(f"Error processing image {image_path}: {e}")
            return None
    
    def load_user_photos_and_train(self):
        """
        Load all user registration photos and train the model
        Expected format: username.jpg, username.png, etc.
        """
        faces = []
        labels = []
        user_id = 0
        
        print("Loading user registration photos...")
        
        if not os.path.exists(self.users_photos_dir):
            print(f"Photos directory {self.users_photos_dir} not found!")
            return False
            
        # Get all image files
        image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
        image_files = []
        
        for file in os.listdir(self.users_photos_dir):
            if any(file.lower().endswith(ext) for ext in image_extensions):
                image_files.append(file)
        
        if len(image_files) == 0:
            print("No user photos found!")
            return False
            
        for image_file in image_files:
            # Extract username from filename (remove extension)
            username = os.path.splitext(image_file)[0]
            image_path = os.path.join(self.users_photos_dir, image_file)
            
            # Extract face from the image
            face = self.extract_face_from_image(image_path)
            
            if face is not None:
                faces.append(face)
                labels.append(user_id)
                self.user_labels[user_id] = username
                self.username_to_id[username] = user_id
                print(f"Loaded photo for user: {username}")
                user_id += 1
            else:
                print(f"No face detected in {image_file}")
        
        if len(faces) == 0:
            print("No valid faces found in photos!")
            return False
            
        print(f"Training model with {len(faces)} user photos...")
        
        # Train the recognizer
        self.face_recognizer.train(faces, np.array(labels))
        self.is_trained = True
        
        print(f"Training completed! Registered users: {list(self.user_labels.values())}")
        return True
    
    def match_face_with_user(self, duration_seconds=10, confidence_threshold=80):
        """
        Capture live video and try to match with registered user photos
        Returns the matched username or None
        """
        if not self.is_trained:
            return None, "Model not trained"
            
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return None, "Could not open camera"
        
        print(f"Starting face matching for {duration_seconds} seconds...")
        print("Look directly at the camera...")
        
        start_time = cv2.getTickCount()
        best_match = None
        best_confidence = float('inf')
        match_count = {}  # Count matches for each user
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            
            for (x, y, w, h) in faces:
                # Extract face region
                face_roi = gray[y:y+h, x:x+w]
                face_resized = cv2.resize(face_roi, (150, 150))
                
                # Predict user
                user_id, confidence = self.face_recognizer.predict(face_resized)
                
                # Draw rectangle around face
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                
                if confidence < confidence_threshold:
                    username = self.user_labels.get(user_id, "Unknown")
                    
                    # Count this match
                    if username in match_count:
                        match_count[username] += 1
                    else:
                        match_count[username] = 1
                    
                    # Track best match
                    if confidence < best_confidence:
                        best_confidence = confidence
                        best_match = username
                    
                    # Display recognition
                    cv2.putText(frame, f"{username} ({confidence:.1f})", 
                              (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    
                    print(f"Matched: {username} (confidence: {confidence:.2f})")
                else:
                    cv2.putText(frame, "Unknown", (x, y-10), 
                              cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            
            cv2.imshow('Face Recognition - Press q to quit', frame)
            
            # Check if time is up
            elapsed_time = (cv2.getTickCount() - start_time) / cv2.getTickFrequency()
            if elapsed_time >= duration_seconds:
                break
                
            # Check for quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
        
        # Determine final result based on most frequent match
        if match_count:
            most_matched_user = max(match_count, key=match_count.get)
            match_frequency = match_count[most_matched_user]
            
            print(f"Match results: {match_count}")
            print(f"Most frequent match: {most_matched_user} ({match_frequency} times)")
            
            # Require at least 3 successful matches for reliability
            if match_frequency >= 3:
                return most_matched_user, None
            else:
                return None, "Insufficient reliable matches"
        else:
            return None, "No face matches found"

def authenticate_user(duration=10, confidence_threshold=80):
    """
    Main authentication function for API integration
    """
    try:
        # Initialize the matcher
        matcher = UserPhotoMatcher()
        
        # Load and train with user photos
        if not matcher.load_user_photos_and_train():
            return {
                "success": False,
                "error": "Failed to load user photos or train model",
                "username": None
            }
        
        # Perform face matching
        matched_user, error = matcher.match_face_with_user(duration, confidence_threshold)
        
        if matched_user:
            return {
                "success": True,
                "error": None,
                "username": matched_user,
                "message": f"Successfully matched with user: {matched_user}"
            }
        else:
            return {
                "success": False,
                "error": error or "Face recognition failed",
                "username": None
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": f"System error: {str(e)}",
            "username": None
        }

def main():
    """Main function for command line usage"""
    # Parse command line arguments
    duration = 10
    confidence_threshold = 80
    
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
    
    print(f"Starting face recognition with duration={duration}s, confidence_threshold={confidence_threshold}")
    
    # Run authentication
    result = authenticate_user(duration, confidence_threshold)
    
    # Print JSON result for API integration
    print(json.dumps(result))

if __name__ == "__main__":
    main()
