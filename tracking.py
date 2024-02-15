import cv2
import mediapipe as mp
from tqdm import tqdm

def get_center_y(video_path):
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    cap = cv2.VideoCapture(video_path)

    center_y_list = []
    fps = 10  # frames per second
    total_frames = 5 * 60 * fps  # frames for 5 minutes

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        for i in tqdm(range(total_frames), desc="Processing frames", ncols=100):
            success, image = cap.read()
            if not success:
                break

            # Pose estimation
            results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

            if results.pose_landmarks:
                # Calculate the center y-coordinate
                left_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y
                right_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].y

                center_y = (left_shoulder + right_shoulder) / 2
                center_y_list.append(center_y)

    cap.release()
    return center_y_list

