import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

def extract_measurements(image_path):
    """
    Extract body measurements from an image using MediaPipe Pose.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        Dictionary containing body measurements in centimeters
    """
    # Read the image
    image = cv2.imread(image_path)
    if image is None:
        raise Exception("Could not read the image")
    
    # Convert to RGB for MediaPipe
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Process the image with MediaPipe Pose
    with mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5) as pose:
        results = pose.process(image_rgb)
        
        if not results.pose_landmarks:
            raise Exception("No person detected in the image")
        
        # Get image dimensions
        h, w, _ = image.shape
        
        # Extract landmarks
        landmarks = results.pose_landmarks.landmark
        
        # Calculate pixel to cm conversion (assuming a person is about 170cm tall)
        # This is a rough estimation and would need calibration in a real application
        person_height_pixels = landmarks[mp_pose.PoseLandmark.HEEL_RIGHT.value].y * h - landmarks[mp_pose.PoseLandmark.NOSE.value].y * h
        pixel_to_cm = 170 / person_height_pixels
        
        # Calculate measurements
        
        # Shoulder width
        left_shoulder = (landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x * w, 
                         landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y * h)
        right_shoulder = (landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x * w, 
                          landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y * h)
        shoulder_width = np.sqrt((left_shoulder[0] - right_shoulder[0])**2 + 
                                 (left_shoulder[1] - right_shoulder[1])**2) * pixel_to_cm
        
        # Chest/Bust
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        shoulder_width_pixels = np.sqrt((left_shoulder.x - right_shoulder.x)**2) * w
        bust = shoulder_width_pixels * 2.5 * pixel_to_cm  # Approximation
        
        # Waist
        left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
        right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
        waist_width_pixels = np.sqrt((left_hip.x - right_hip.x)**2) * w
        waist = waist_width_pixels * 2.2 * pixel_to_cm  # Approximation
        
        # Hips
        hip_width_pixels = np.sqrt((left_hip.x - right_hip.x)**2) * w
        hips = hip_width_pixels * 2.8 * pixel_to_cm  # Approximation
        
        # Arm length
        left_shoulder = (landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x * w, 
                         landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y * h)
        left_wrist = (landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x * w, 
                      landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y * h)
        arm_length = np.sqrt((left_shoulder[0] - left_wrist[0])**2 + 
                             (left_shoulder[1] - left_wrist[1])**2) * pixel_to_cm
        
        # Inseam (approximation)
        left_hip = (landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x * w, 
                    landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y * h)
        left_ankle = (landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x * w, 
                      landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y * h)
        inseam = np.sqrt((left_hip[0] - left_ankle[0])**2 + 
                         (left_hip[1] - left_ankle[1])**2) * pixel_to_cm
        
        # Height
        height = 170  # We used this for calibration
        
        # Neck circumference (approximation)
        neck_width_pixels = shoulder_width_pixels * 0.4  # Approximation
        neck_circumference = neck_width_pixels * 3.14 * pixel_to_cm
        
        # Round all measurements to 1 decimal place
        measurements = {
            'bust': round(bust, 1),
            'waist': round(waist, 1),
            'hips': round(hips, 1),
            'shoulder_width': round(shoulder_width, 1),
            'arm_length': round(arm_length, 1),
            'inseam': round(inseam, 1),
            'height': round(height, 1),
            'neck_circumference': round(neck_circumference, 1)
        }
        
        return measurements