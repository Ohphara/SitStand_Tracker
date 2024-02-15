from tracking import get_center_y
from show import show_video_and_graph

def main():
    video_path = r"C:\Users\PJO\23kist\json_location_pose\child_focus_240123_13_SI008L0F_T2_10fps.mp4"
    
    # tracking.py로부터 center_y(t)를 얻습니다.
    center_y = get_center_y(video_path)
    
    # show.py를 통해 동영상과 그래프를 함께 보여줍니다.
    show_video_and_graph(video_path, center_y)

if __name__ == "__main__":
    main()
