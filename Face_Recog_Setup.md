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






















# Complete Face Recognition Setup Guide for Blockchain E-Voting System

## 📋 Prerequisites
- Windows 10/11
- Git installed
- Node.js installed
- Python 3.12 or 3.13 installed

## 🚀 Step-by-Step Setup Instructions

### Step 1: Clone the Repository
```bash
git clone https://github.com/sarthakyeole/PR_2001.git
cd "PR_2001/Blockchain based E-voting system using Facial Recgonition"
```

### Step 2: Install Node.js Dependencies

#### Install Server Dependencies
```bash
cd server
npm install
```

#### Install Client Dependencies
```bash
cd ../client
npm install
cd ..
```

### Step 3: Python Environment Setup

#### Check Python Version
```bash
python --version
```
*Should show Python 3.12.x or 3.13.x*

#### Install Required Python Packages
```bash
pip install opencv-contrib-python
pip install numpy
```

#### Verify OpenCV Installation
```bash
python -c "import cv2; print('OpenCV version:', cv2.__version__)"
```
*Should show OpenCV version without errors*

### Step 4: Test Camera Access
```bash
cd server/Controller
python test_imports.py
```
*This should show your camera feed. Press 'q' to quit*

### Step 5: Add Face Images for Recognition

#### Create a face image for yourself:
1. Take a clear photo of your face (good lighting, frontal view)
2. Save it as `[your_username].jpg` in the `server/Faces/` folder
3. Example: `john.jpg`, `sarah.png`, etc.

### Step 6: Test Face Recognition System

#### Test Basic Face Recognition
```bash
cd server/Controller
python simple_face_recognition.py
```
*This will load faces and start camera recognition*

#### Test API Interface
```bash
python face_auth_api.py 15 60
```
*Parameters: 15 seconds duration, 60 confidence threshold*

### Step 7: Setup Username Mapping

#### Create username mapping file
Create `server/Controller/username_mapping.json` with your mappings:
```json
{
  "your_photo_name": "your_actual_username",
  "john_photo": "john",
  "sarah_image": "sarah"
}
```

### Step 8: Test Complete System

#### Test with batch file approach
```bash
cd server/Controller
./run_face_auth.bat 10 80
```
*If batch file doesn't exist, create it with:*

Create `server/Controller/run_face_auth.bat`:
```batch
@echo off
C:/Users/%USERNAME%/AppData/Local/Programs/Python/Python313/python.exe face_auth_api.py %1 %2
```

### Step 9: Start the Backend Server
```bash
cd server
npm start
```
*Server should start on port 8000*

### Step 10: Start the Frontend Client
Open a new terminal:
```bash
cd client
npm start
```
*Client should open in browser on port 3000*

### Step 11: Setup MongoDB Database

#### Install MongoDB Community Edition or use MongoDB Atlas
For local installation:
```bash
# Download MongoDB Community Server from official website
# Install and start MongoDB service
```

#### Update database connection in server files if needed

### Step 12: Setup Blockchain Environment

#### Install Truffle (if using smart contracts)
```bash
npm install -g truffle
```

#### Install MetaMask browser extension
- Add MetaMask to your browser
- Create or import wallet
- Connect to appropriate network

### Step 13: Final Integration Test

#### Test face recognition through web app:
1. Open browser to `http://localhost:3000`
2. Navigate to voting page
3. Click "📷 Vote with Face ID" button
4. Face recognition should activate for 10 seconds
5. Should return your mapped username

### Step 14: Final Command - The 10 80 Test
```bash
cd server/Controller
python face_auth_api.py 10 80
```

**Expected Output:**
```
Loaded face for: [your_username]
Loaded face for: [other_faces]...
Training completed with X faces
Starting face recognition for 10 seconds...
Press 'q' to quit early
Recognized: [detected_face] (confidence: XX.XX)
{"success": true, "error": null, "username": "[your_mapped_username]", "detected_face": "[original_detected_name]"}
```

## 🔧 Troubleshooting Commands

### If OpenCV installation fails:
```bash
pip uninstall opencv-python opencv-contrib-python
pip install opencv-contrib-python==4.8.1.78
```

### If camera doesn't work:
```bash
python -c "import cv2; cap = cv2.VideoCapture(0); print('Camera opened:', cap.isOpened()); cap.release()"
```

### If Python path issues in web app:
Find your Python path:
```bash
python -c "import sys; print(sys.executable)"
```
Update the batch file with correct path.

### Check all required modules:
```bash
python -c "import cv2, numpy, json, os, sys; print('All modules imported successfully')"
```

## 📁 Required File Structure After Setup
```
server/
├── Controller/
│   ├── simple_face_recognition.py
│   ├── face_auth_api.py
│   ├── username_mapping.json
│   ├── run_face_auth.bat
│   └── AuthController.js (updated)
├── Faces/
│   ├── [your_username].jpg
│   └── [other_user_photos]
└── package.json

client/
├── src/
├── public/
└── package.json
```

## ✅ Success Indicators

1. **OpenCV installed**: `python -c "import cv2"` works without error
2. **Camera access**: Can see video feed in test scripts
3. **Face detection**: System loads and recognizes faces
4. **Username mapping**: Correct username returned in JSON
5. **Web integration**: Face ID button works in browser
6. **Final test**: `python face_auth_api.py 10 80` returns success JSON

## 🎯 Final Test Command
```bash
cd server/Controller
python face_auth_api.py 10 80
```

This should be the last command that confirms everything is working correctly!

---
**Note**: Make sure to replace `[your_username]` with actual usernames and adjust file paths according to your Python installation path.
