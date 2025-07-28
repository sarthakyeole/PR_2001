import cv2
import numpy as np
import os
from pathlib import Path

class FaceRecognitionOpenCV:
    def __init__(self, faces_dir):
        self.faces_dir = faces_dir
        self.mp_face_detection = mp.solutions.face_detection
        self.mp_drawing = mp.solutions.drawing_utils
        self.face_detection = self.mp_face_detection.FaceDetection(
            model_selection=0, min_detection_confidence=0.5)
        
        # Load known faces
        self.known_faces = {}
        self.load_known_faces()
    
    def load_known_faces(self):
        """Load and process all images in the faces directory"""
        if not os.path.exists(self.faces_dir):
            print(f"Faces directory {self.faces_dir} not found!")
            return
            
        for filename in os.listdir(self.faces_dir):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                name = os.path.splitext(filename)[0]
                image_path = os.path.join(self.faces_dir, filename)
                
                # Load and process the image
                image = cv2.imread(image_path)
                if image is not None:
                    # Convert to RGB for MediaPipe
                    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    
                    # Detect faces
                    results = self.face_detection.process(rgb_image)
                    
                    if results.detections:
                        # Store the image and name
                        self.known_faces[name] = {
                            'image': rgb_image,
                            'detection': results.detections[0]
                        }
                        print(f"Loaded face for: {name}")
                    else:
                        print(f"No face detected in {filename}")
    
    def extract_face_roi(self, image, detection):
        """Extract face region of interest from detection"""
        h, w, _ = image.shape
        bbox = detection.location_data.relative_bounding_box
        
        # Convert relative coordinates to absolute
        x = int(bbox.xmin * w)
        y = int(bbox.ymin * h)
        width = int(bbox.width * w)
        height = int(bbox.height * h)
        
        # Ensure coordinates are within image bounds
        x = max(0, x)
        y = max(0, y)
        width = min(width, w - x)
        height = min(height, h - y)
        
        # Extract face ROI
        face_roi = image[y:y+height, x:x+width]
        return face_roi
    
    def compare_faces(self, face1, face2):
        """Simple face comparison using histogram correlation"""
        if face1.size == 0 or face2.size == 0:
            return 0.0
            
        # Resize faces to same size for comparison
        target_size = (100, 100)
        face1_resized = cv2.resize(face1, target_size)
        face2_resized = cv2.resize(face2, target_size)
        
        # Convert to grayscale
        face1_gray = cv2.cvtColor(face1_resized, cv2.COLOR_RGB2GRAY)
        face2_gray = cv2.cvtColor(face2_resized, cv2.COLOR_RGB2GRAY)
        
        # Calculate histograms
        hist1 = cv2.calcHist([face1_gray], [0], None, [256], [0, 256])
        hist2 = cv2.calcHist([face2_gray], [0], None, [256], [0, 256])
        
        # Compare histograms using correlation
        correlation = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
        
        return correlation
    
    def recognize_face_from_camera(self, duration_seconds=30, recognition_threshold=0.6):
        """Recognize face from camera feed"""
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Could not open camera")
            return None
        
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        recognized_names = []
        frame_count = 0
        max_frames = duration_seconds * 30  # Assuming 30 FPS
        
        print(f"Starting face recognition for {duration_seconds} seconds...")
        print("Press 'q' to quit early")
        
        while frame_count < max_frames:
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame")
                break
            
            # Convert to RGB for MediaPipe
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Detect faces in current frame
            results = self.face_detection.process(rgb_frame)
            
            if results.detections:
                for detection in results.detections:
                    # Extract face ROI
                    current_face = self.extract_face_roi(rgb_frame, detection)
                    
                    # Compare with known faces
                    best_match = None
                    best_score = 0
                    
                    for name, known_face_data in self.known_faces.items():
                        known_face_roi = self.extract_face_roi(
                            known_face_data['image'], 
                            known_face_data['detection']
                        )
                        
                        score = self.compare_faces(current_face, known_face_roi)
                        
                        if score > best_score:
                            best_score = score
                            best_match = name
                    
                    # If match is above threshold, record it
                    if best_score > recognition_threshold:
                        recognized_names.append(best_match)
                        print(f"Recognized: {best_match} (score: {best_score:.2f})")
                    
                    # Draw bounding box on display frame
                    bbox = detection.location_data.relative_bounding_box
                    h, w, _ = frame.shape
                    x = int(bbox.xmin * w)
                    y = int(bbox.ymin * h)
                    width = int(bbox.width * w)
                    height = int(bbox.height * h)
                    
                    cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 255, 0), 2)
                    
                    if best_match and best_score > recognition_threshold:
                        cv2.putText(frame, f"{best_match} ({best_score:.2f})", 
                                  (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            
            # Display the frame
            cv2.imshow('Face Recognition', frame)
            
            # Check for quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
            frame_count += 1
        
        cap.release()
        cv2.destroyAllWindows()
        
        # Determine the most recognized face
        if recognized_names:
            from collections import Counter
            most_common = Counter(recognized_names).most_common(1)
            return most_common[0][0]  # Return the most frequently recognized name
        
        return None
    
    def test_recognition(self):
        """Test the recognition system"""
        print("Available faces:")
        for name in self.known_faces.keys():
            print(f"- {name}")
        
        print("\nStarting camera recognition test...")
        result = self.recognize_face_from_camera(duration_seconds=10)
        
        if result:
            print(f"\nRecognition result: {result}")
        else:
            print("\nNo face recognized")
        
        return result

# Example usage
if __name__ == "__main__":
    # Update this path to match your faces directory
    faces_directory = os.path.join(os.path.dirname(__file__), "..", "Faces")
    
    # Create face recognition instance
    face_recognizer = FaceRecognitionMediaPipe(faces_directory)
    
    # Test the system
    face_recognizer.test_recognition()
