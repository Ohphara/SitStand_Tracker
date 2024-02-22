# SitStand_Tracker

이 프로젝트는 사람의 행동(예: 일어서기, 앉기)을 비디오에서 감지하는 것을 목표로 합니다.

## 파일 구조

- `main.py`: 프로그램의 시작점입니다. 먼저, `tracking.py`로 비디오에서 center_y(t)를 추출합니다. 그 다음, `detect_action.py`를 사용하여 center_y(t)에 sliding window를 적용하여 행동(일어서기, 앉기)이 언제 발생했는지 감지합니다. 이때, 윈도우의 max[]-min[] 값이 `minmax_threshold`보다 크면 TRUE를 반환합니다. 그 후, `get_action_frames.py`를 사용하여 감지된 행동이 있는 프레임에 1을 반환하고, 각 프레임은 1 또는 0의 값을 가집니다. 마지막으로, `show.py`를 사용하여 그래프와 비디오를 보여줍니다.
- `tracking.py`: 이 파일은 비디오에서 사람의 자세를 추적하고, 어깨의 중심 위치(center_y)를 계산하여 리스트로 반환하는 역할을 합니다. OpenCV와 Mediapipe의 pose estimation 기능을 이용하여 각 프레임에서 사람의 자세를 추정하고, 이를 바탕으로 왼쪽 어깨와 오른쪽 어깨의 중심 y 좌표를 계산합니다. 만약 사람의 자세를 감지할 수 없는 경우에는 None을 리스트에 추가합니다.
- `detect_action.py`: 이 파일은 sliding window 방식을 사용해 center_y 리스트를 분석하고, 윈도우 내에서의 y 좌표의 변화가 주어진 임계값보다 큰지를 판단하여 행동(예: 일어서기, 앉기)을 감지합니다. 윈도우 크기는 비디오의 프레임 수(fps)를 사용하며, 윈도우 간의 중첩 비율은 설정 가능합니다. 윈도우 내에서의 최대 y 좌표와 최소 y 좌표의 차이가 임계값보다 크면 해당 윈도우에서 행동이 감지되었다고 판단하고, 아닌 경우에는 감지되지 않았다고 판단합니다.
- `get_action_frames.py`: 이 파일은 `detect_action.py`에서 감지된 행동들을 기반으로, 각 프레임이 행동을 포함하는지 아닌지를 나타내는 리스트를 생성합니다. `detect_action.py`에서 감지된 각 행동에 대해, 해당 행동이 발생한 프레임에 1을 할당합니다. 이때, 프레임 간의 중첩 비율을 고려하여 step size를 계산합니다.
- `show.py`: 이 파일은 비디오와 그래프를 동시에 보여주는 역할을 합니다. Matplotlib 라이브러리를 사용하여 center_y 데이터를 시간에 따라 시각화하고, Mediapipe 라이브러리를 사용하여 각 프레임에서 사람의 어깨 위치를 표시합니다. 또한, 각 프레임이 행동을 포함하는지 여부에 따라 그래프에 색상을 채워 시각적으로 표시합니다.
- `config.py`: 프로그램의 설정 값들을 정의하는 파일입니다. 예를 들어, 비디오의 프레임 수(fps), 윈도우 간의 중첩 비율, y 좌표의 최대-최소 차이에 대한 임계값 등이 설정되어 있습니다.
- `requirements.txt`: 프로젝트를 실행하기 위해 필요한 파이썬 패키지들이 명시되어 있습니다.