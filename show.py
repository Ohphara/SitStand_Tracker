import cv2
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import mediapipe as mp

def show_video_and_graph(video_path, center_y):
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Calculate the time per frame in seconds
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_times = np.arange(len(center_y)) / fps

    # Create a figure for plotting
    fig, ax = plt.subplots()

    # Set the y-axis limit
    ax.set_ylim(np.min(center_y), np.max(center_y)) 

    # Convert x-axis into time format (min:sec)
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, pos: f'{int(x // 60)}:{int(x % 60):02d}'))

    # Create a line object for center_y
    line, = ax.plot(frame_times, center_y, 'r-')

    # Create a vertical line object for the current time
    vline = ax.axvline(0, color='k')

    # Initialize the graph
    def init():
        line.set_data([], [])
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
                mp.solutions.drawing_utils.draw_landmarks(image, results.pose_landmarks, [mp_pose.PoseLandmark.LEFT_SHOULDER, mp_pose.PoseLandmark.RIGHT_SHOULDER])
            cv2.imshow('Video', image)
            cv2.waitKey(1)

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

