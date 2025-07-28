# Face Recognition Setup Guide

## ✅ Current Status
Your face recognition system is now working! Here's what has been set up:

## 📁 Files Created/Updated

### New Python Files:
- `simple_face_recognition.py` - Main face recognition system using OpenCV
- `face_auth_api.py` - API interface for Node.js integration
- `fr_updated.py` - Updated version of your original fr.py
- `test_system.py` - Diagnostic tool for testing camera and face detection

### Updated Files:
- `AuthController.js` - Updated to use the new face recognition system
- `encoded.py` - Fixed file paths

## 🚀 How to Use

### 1. Test Your Setup
```bash
cd server/Controller
python test_system.py
```

### 2. Test Face Recognition Directly
```bash
cd server/Controller
python fr_updated.py
```

### 3. Test API (for Node.js integration)
```bash
cd server/Controller
python face_auth_api.py 15 60
```

### 3a. Test API with more lenient settings (recommended)
```bash
cd server/Controller
python face_auth_api.py 10 80

# Use this command to run the face recognition model
C:/Users/sarth/AppData/Local/Programs/Python/Python313/python.exe face_auth_api.py 10 80
```
Parameters: duration (seconds), confidence_threshold (lower = stricter, higher = more lenient)

## 🔧 Integration with Your Voting App

Your Node.js server can now call the face recognition endpoint. The updated `AuthController.js` will:

1. Run the Python face recognition script
2. Return JSON response with authentication result
3. Include the recognized username if successful

### API Endpoints Available:
- `POST /api/face-recognition` - Main face recognition endpoint
- `POST /api/op` - Alternative endpoint (same functionality)

### Frontend Integration:
```javascript
// Call face recognition from your React app
const response = await fetch('/api/face-recognition', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' }
});
const result = await response.json();
// Returns: {success: true, username: "recognized_user"}
```

### Voting Flow:
1. **User clicks "Vote"** → 
2. **Face Recognition Authentication** → 
3. **Verify user eligibility** → 
4. **Show ballot/candidates** → 
5. **Submit vote to blockchain**

See `VOTING_INTEGRATION_EXAMPLE.jsx` for complete React component example.

### API Response Format:
```json
{
  "success": true,
  "username": "sarthak",
  "message": "Face recognition successful"
}
```

## 📸 Adding New Users

To add a new user for face recognition:

1. Add their photo to the `server/Faces/` directory
2. Name the file with their username (e.g., `john.jpg`, `mary.png`)
3. Ensure the photo:
   - Shows a clear face
   - Has good lighting
   - Is not too large (system will resize automatically)

## ⚙️ Adjusting Settings

### Confidence Threshold:
- Lower values (30-50): Stricter matching, fewer false positives
- Higher values (60-80): More lenient matching, might accept similar faces

### Duration:
- Shorter (5-10 seconds): Quick authentication
- Longer (15-30 seconds): More reliable recognition

## 🐛 Troubleshooting

### ❌ If you get "ModuleNotFoundError: No module named 'cv2'" in your web app:
This happens when Node.js uses a different Python installation. **Solution:**
1. ✅ A batch file `run_face_auth.bat` has been created to use the correct Python
2. ✅ AuthController has been updated to use this batch file
3. ✅ This ensures the web app uses the Python installation with OpenCV installed

### If face recognition fails:
1. Run `python test_system.py` to check camera and face detection
2. Ensure good lighting when testing
3. Position face clearly in front of camera
4. Check that user photos are clear and well-lit

### If camera doesn't work:
1. Make sure no other applications are using the camera
2. Try changing `cv2.VideoCapture(0)` to `cv2.VideoCapture(1)` in the Python files

### If no faces are detected in photos:
1. Ensure photos show clear frontal faces
2. Try different lighting in the photos
3. Use JPG or PNG format
4. Avoid very large image files

## 📋 Available Users

Your current registered face images:

## 🔄 Next Steps

1. Test the system with your own face
2. Integrate with your voting frontend
3. Add error handling for failed recognitions
4. Consider adding a fallback authentication method

## 💡 Tips for Better Recognition

1. Use consistent lighting when taking photos and during recognition
2. Ensure users look directly at the camera
3. Avoid glasses or face coverings if possible
4. Take multiple photos per user if recognition is unreliable
