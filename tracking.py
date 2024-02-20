import cv2
import mediapipe as mp
from tqdm import tqdm

def get_center_y(video_path):
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    cap = cv2.VideoCapture(video_path)

    # Get the total number of frames for the video
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    center_y_list = []

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        for i in tqdm(range(total_frames), desc="Processing frames", ncols=100):
            success, image = cap.read()
            if not success:
                break

            # Pose estimation
            results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

            if results.pose_landmarks:
                # Calculate the center y-coordinate
                left_shoulder = results.pose_landmarks.landmark[11].y
                right_shoulder = results.pose_landmarks.landmark[12].y

                center_y = (left_shoulder + right_shoulder) / 2
                center_y_list.append(center_y)
            else:
                center_y_list.append(None)  # Add None if no landmarks are detected

    cap.release()
    return center_y_list