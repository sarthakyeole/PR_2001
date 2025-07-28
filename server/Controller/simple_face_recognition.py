import cv2
import numpy as np
import os
from collections import Counter

class SimpleFaceRecognition:
    def __init__(self, faces_dir):
        self.faces_dir = faces_dir
        # Load OpenCV's pre-trained face detection model
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # Initialize face recognizer
        self.face_recognizer = cv2.face.LBPHFaceRecognizer_create()
        
        # Load known faces
        self.known_faces = []
        self.known_names = []
        self.load_known_faces()
    
    def load_known_faces(self):
        """Load and process all images in the faces directory"""
        if not os.path.exists(self.faces_dir):
            print(f"Faces directory {self.faces_dir} not found!")
            return
        
        faces = []
        labels = []
        names = []
        
        label_counter = 0
        
        for filename in os.listdir(self.faces_dir):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')) and filename != 'temp.jpg':
                name = os.path.splitext(filename)[0]
                image_path = os.path.join(self.faces_dir, filename)
                
                # Load image
                image = cv2.imread(image_path)
                if image is not None:
                    # Convert to grayscale
                    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                    
                    # Detect faces
                    detected_faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
                    
                    if len(detected_faces) > 0:
                        # Take the first (largest) face
                        (x, y, w, h) = detected_faces[0]
                        face_roi = gray[y:y+h, x:x+w]
                        
                        # Resize face to standard size
                        face_roi = cv2.resize(face_roi, (100, 100))
                        
                        faces.append(face_roi)
                        labels.append(label_counter)
                        names.append(name)
                        
                        print(f"Loaded face for: {name}")
                        label_counter += 1
                    else:
                        print(f"No face detected in {filename}")
        
        if len(faces) > 0:
            # Train the face recognizer
            self.face_recognizer.train(faces, np.array(labels))
            self.known_names = names
            print(f"Training completed with {len(faces)} faces")
        else:
            print("No faces found for training!")
    
    def recognize_face_from_camera(self, duration_seconds=10, confidence_threshold=50):
        """Recognize face from camera feed"""
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Could not open camera")
            return None
        
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        recognized_names = []
        frame_count = 0
        max_frames = duration_seconds * 10  # Check every few frames
        
        print(f"Starting face recognition for {duration_seconds} seconds...")
        print("Press 'q' to quit early")
        
        while frame_count < max_frames:
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame")
                break
            
            # Convert to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
            
            for (x, y, w, h) in faces:
                # Extract face ROI
                face_roi = gray[y:y+h, x:x+w]
                face_roi = cv2.resize(face_roi, (100, 100))
                
                # Recognize face
                if len(self.known_names) > 0:
                    label, confidence = self.face_recognizer.predict(face_roi)
                    
                    # Lower confidence means better match
                    if confidence < confidence_threshold:
                        name = self.known_names[label]
                        recognized_names.append(name)
                        print(f"Recognized: {name} (confidence: {confidence:.2f})")
                        
                        # Draw rectangle and name
                        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                        cv2.putText(frame, f"{name} ({confidence:.1f})", 
                                  (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                    else:
                        # Unknown face
                        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
                        cv2.putText(frame, "Unknown", 
                                  (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
                else:
                    # No trained faces
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                    cv2.putText(frame, "No trained faces", 
                              (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
            
            # Display the frame
            cv2.imshow('Face Recognition', frame)
            
            # Check for quit
            if cv2.waitKey(100) & 0xFF == ord('q'):  # Check every 100ms
                break
            
            frame_count += 1
        
        cap.release()
        cv2.destroyAllWindows()
        
        # Determine the most recognized face
        if recognized_names:
            most_common = Counter(recognized_names).most_common(1)
            return most_common[0][0]  # Return the most frequently recognized name
        
        return None
    
    def test_recognition(self):
        """Test the recognition system"""
        print("Available faces:")
        for name in self.known_names:
            print(f"- {name}")
        
        if len(self.known_names) == 0:
            print("No faces loaded! Please add face images to the Faces directory.")
            return None
        
        print(f"\nStarting camera recognition test...")
        print("Make sure your camera is working and position your face in front of it.")
        
        result = self.recognize_face_from_camera(duration_seconds=15)
        
        if result:
            print(f"\nRecognition result: {result}")
        else:
            print("\nNo face recognized or confidence too low")
        
        return result

# Create a simplified version that can be imported
def recognize_face(faces_directory, duration=10):
    """Simple function to recognize a face"""
    recognizer = SimpleFaceRecognition(faces_directory)
    return recognizer.recognize_face_from_camera(duration)

# Example usage
if __name__ == "__main__":
    # Update this path to match your faces directory
    faces_directory = os.path.join(os.path.dirname(__file__), "..", "Faces")
    
    # Create face recognition instance
    face_recognizer = SimpleFaceRecognition(faces_directory)
    
    # Test the system
    face_recognizer.test_recognition()
