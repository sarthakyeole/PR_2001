import cv2
import os

def test_camera():
    """Test if camera is working"""
    print("Testing camera...")
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Error: Could not open camera")
        return False
    
    print("✅ Camera opened successfully")
    print("Press 'q' to quit camera test")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Error: Could not read frame")
            break
        
        cv2.imshow('Camera Test', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    return True

def test_face_detection():
    """Test basic face detection"""
    print("\nTesting face detection...")
    
    # Load face detection model
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Error: Could not open camera")
        return False
    
    print("✅ Face detection ready")
    print("Position your face in front of the camera")
    print("Press 'q' to quit face detection test")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.putText(frame, 'Face Detected', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
        
        cv2.imshow('Face Detection Test', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    return True

def list_face_images():
    """List all face images in the Faces directory"""
    faces_dir = os.path.join(os.path.dirname(__file__), "..", "Faces")
    
    if not os.path.exists(faces_dir):
        print(f"❌ Faces directory not found: {faces_dir}")
        return
    
    print(f"\n📁 Faces directory: {faces_dir}")
    print("Available face images:")
    
    image_files = [f for f in os.listdir(faces_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    if not image_files:
        print("❌ No image files found in Faces directory")
        return
    
    for i, filename in enumerate(image_files, 1):
        name = os.path.splitext(filename)[0]
        print(f"{i}. {filename} -> User: {name}")

def main():
    print("🔍 Face Recognition System Diagnostic Tool")
    print("=" * 50)
    
    # Test 1: List face images
    list_face_images()
    
    # Test 2: Camera test
    print("\n" + "=" * 50)
    if not test_camera():
        print("❌ Camera test failed. Please check your camera connection.")
        return
    
    # Test 3: Face detection test
    print("\n" + "=" * 50)
    if not test_face_detection():
        print("❌ Face detection test failed.")
        return
    
    print("\n" + "=" * 50)
    print("✅ All tests completed!")
    print("\nNext steps:")
    print("1. Make sure your face images are clear and well-lit")
    print("2. Ensure image filenames match the usernames you want to recognize")
    print("3. Run the face recognition system: python fr_updated.py")

if __name__ == "__main__":
    main()
