import cv2
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import mediapipe as mp
from config import fps

def show_video_and_graph(video_path, center_y, action_frames):
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Calculate the time per frame in seconds
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_times = np.arange(len(center_y)) / fps

    # Create a figure for plotting
    fig, ax = plt.subplots()
    
    # Set the y-axis limit
    valid_center_y = [y for y in center_y if y is not None]  # Filter out None values
    ax.set_ylim(np.min(valid_center_y), np.max(valid_center_y))
    plt.xticks(np.arange(min(frame_times), max(frame_times)+1, 60))  # x축 눈금을 1분(60초) 단위로 설정
    # Convert x-axis into time format (min:sec)
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, pos: f'{int(x // 60)}:{int(x % 60):02d}'))
    
    # Create a line object for center_y
    line, = ax.plot(frame_times, center_y, 'r-')
    
    # Create a vertical line object for the current time
    vline = ax.axvline(0, color='k')

    # Add filled areas for action_detected times
    for i, detected in enumerate(action_frames):
        if detected:
            ax.fill_between([i/fps, (i+1)/fps], ax.get_ylim()[0], ax.get_ylim()[1], color='orange', alpha=0.3)  # Use orange color for detected actions

    # Initialize the graph
    def init():
        line.set_data(frame_times, center_y)  # Plot all center_y data
        vline.set_xdata(0)
        return line, vline
    
    # Pose estimation
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5)

    

# Update the graph
    def update(frame):
        # Show the current frame of the video
        ret, image = cap.read()
        if ret:
            # Draw the landmarks on the image
            results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            if results.pose_landmarks:
                for landmark in [mp_pose.PoseLandmark.LEFT_SHOULDER, mp_pose.PoseLandmark.RIGHT_SHOULDER]:
                    image_hight, image_width, _ = image.shape
                    x = int(results.pose_landmarks.landmark[landmark].x * image_width)
                    y = int(results.pose_landmarks.landmark[landmark].y * image_hight)
                    cv2.circle(image, (x, y), 5, (0, 255, 0), -1)
            cv2.imshow('Video', image)
            key = cv2.waitKey(int(100 / fps))  # Wait for the correct amount of time
            
            # Check if space bar is pressed
            if key == ord(' '):
                
                # Pause the video
                while True:
                    key2 = cv2.waitKey(1)
                    cv2.imshow('Video', image)
                    
                    # If space bar is pressed again, resume the video
                    if key2 == ord(' '):
                        break
        
        # Update the position of the vertical line
        vline.set_xdata(frame_times[frame])
        
        return line, vline
    
    # Create an animation
    ani = animation.FuncAnimation(fig, update, frames=len(center_y),
                                  init_func=init, blit=True)
    
    # Show the figure
    plt.show()
    
    # Release the video file
    cap.release()
    
    # Close all OpenCV windows
    cv2.destroyAllWindows()