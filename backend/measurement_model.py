# backend/measurement_model.py

import mediapipe as mp
import cv2
import numpy as np

def extract_measurements(photo_path):
    """
    Extract body measurements from the photo using Mediapipe Pose estimation.
    Returns comprehensive body measurements in centimeters.
    """
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(static_image_mode=True, model_complexity=2, min_detection_confidence=0.5)

    img = cv2.imread(photo_path)

    if img is None:
        return {"error": "Image not found or invalid."}

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(img_rgb)

    if not results.pose_landmarks:
        return {"error": "No pose landmarks detected."}

    landmarks = results.pose_landmarks.landmark
    height, width, _ = img.shape

    # Calculate pixel to cm ratio (assuming average height of 170cm)
    # This is a simplification - for production, you'd need a reference object
    person_height_pixels = abs(landmarks[0].y - landmarks[29].y) * height
    pixel_to_cm_ratio = 170 / person_height_pixels

    # Calculate measurements
    # Shoulder width
    shoulder_width = abs(landmarks[11].x - landmarks[12].x) * width * pixel_to_cm_ratio
    
    # Bust/chest (approximation)
    bust = abs(landmarks[11].x - landmarks[12].x) * width * 1.2 * pixel_to_cm_ratio
    
    # Waist (approximation)
    waist = abs(landmarks[23].x - landmarks[24].x) * width * 1.05 * pixel_to_cm_ratio
    
    # Hip (approximation)
    hip = abs(landmarks[23].x - landmarks[24].x) * width * 1.4 * pixel_to_cm_ratio
    
    # Arm length (shoulder to wrist)
    right_arm = (distance_3d(landmarks[11], landmarks[13]) + 
                distance_3d(landmarks[13], landmarks[15])) * height * pixel_to_cm_ratio
    
    # Inseam (approximation - crotch to ankle)
    inseam = distance_3d(landmarks[24], landmarks[28]) * height * pixel_to_cm_ratio
    
    # Neck circumference (approximation)
    neck_width = distance_3d(landmarks[9], landmarks[10]) * width * pixel_to_cm_ratio
    neck_circumference = neck_width * np.pi * 0.8  # Approximation
    
    # Height
    height_cm = person_height_pixels * pixel_to_cm_ratio

    return {
        "height_cm": round(height_cm, 1),
        "shoulder_width_cm": round(shoulder_width, 1),
        "bust_cm": round(bust, 1),
        "waist_cm": round(waist, 1),
        "hip_cm": round(hip, 1),
        "arm_length_cm": round(right_arm, 1),
        "inseam_cm": round(inseam, 1),
        "neck_circumference_cm": round(neck_circumference, 1)
    }

def distance_3d(landmark1, landmark2):
    """Calculate 3D distance between two landmarks"""
    return np.sqrt((landmark1.x - landmark2.x)**2 + 
                  (landmark1.y - landmark2.y)**2 + 
                  (landmark1.z - landmark2.z)**2)
