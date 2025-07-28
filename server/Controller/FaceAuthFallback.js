// Alternative approach using child_process to run the batch file
import { exec } from 'child_process';
import path from 'path';

export const faceRecognitionFallback = {
  sc: async (req, res) => {
    const batchPath = path.resolve(process.cwd(), "Controller", "run_face_auth.bat");
    const command = `"${batchPath}" 10 80`; // Changed to 10 seconds, 80 confidence threshold
    
    exec(command, { timeout: 30000 }, (error, stdout, stderr) => {
      if (error) {
        console.error("Face recognition error:", error);
        return res.status(500).json({
          success: false,
          error: "Face recognition system error",
          message: "Error while running face recognition"
        });
      }

      if (stderr) {
        console.error("Python stderr:", stderr);
        return res.status(500).json({
          success: false,
          error: "Face recognition system error",
          message: "Face recognition system error"
        });
      }

      try {
        // Extract JSON from the last line of stdout (like in AuthController)
        const lines = stdout.trim().split('\n');
        const jsonLine = lines[lines.length - 1];
        console.log("Face recognition stdout:", stdout);
        console.log("Extracted JSON line:", jsonLine);
        const authResult = JSON.parse(jsonLine);
        
        if (authResult.success) {
          return res.status(201).json({
            success: true,
            username: authResult.username,
            message: "Face recognition successful"
          });
        } else {
          return res.status(401).json({
            success: false,
            error: authResult.error,
            message: "Face recognition failed"
          });
        }
      } catch (parseError) {
        console.error("JSON parse error:", parseError);
        console.error("stdout was:", stdout);
        return res.status(500).json({
          success: false,
          error: "Error parsing face recognition result",
          message: "Error parsing face recognition result"
        });
      }
    });
  },
};
