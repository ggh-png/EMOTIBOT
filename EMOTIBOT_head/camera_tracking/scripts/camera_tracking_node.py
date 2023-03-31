#!/usr/bin/env python

import os.path
import rospy
import cv2
import math
from std_msgs.msg import Int32



rospy.init_node('camera_traking')
pub = rospy.Publisher('EMOTIBOT/neck_position', Int32, queue_size=10)

# 얼굴을 감지하기 위한 미리 학습된 Haar Cascade 분류기(대상 분류 알고리즘) 로드
file_path = os.path.expanduser(os.path.join('~', 'config/haarcascade_frontalface_default.xml'))
face_cascade = cv2.CascadeClassifier(file_path)

# 기본 카메라로부터 비디오 캡처를 시작 
# 0 : 노트북 이용시 내부 웹캠 사용 
# 1 : 외부 캠 사용 
cap = cv2.VideoCapture(0)

# degree 값을 저장할 배열 선언
degree_array = []

# 비디오 스트림의 각 프레임을 반복 처리
while True:
    # 비디오 스트림으로부터 프레임을 읽어오기
    ret, frame = cap.read()

    # 화면 중앙 픽셀값 960 540
    height, width = frame.shape[:2]
    center_x = int(width / 1.2) 
    center_y = int(height / 2)

    # 프레임을 회색조 이미지로 변환
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 회색조 이미지에서 얼굴을 감지
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=8, minSize=(30, 30))

    # 감지된 얼굴의 크기를 계산하여 큰 얼굴에는 1, 작은 얼굴에는 2를 표시하고 초록색 사각형으로 표시
    faces_sorted_by_size = sorted(faces, key=lambda f: f[2] * f[3], reverse=True)
    for idx, (x, y, w, h) in enumerate(faces_sorted_by_size, 1):
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # 얼굴 사각형 내의 영역을 ROI(관심 영역 지정)로 정의
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]

        # 오른쪽 끝은 1700, 왼쪽 끝은 300(맥북 카메라기준)
        cv2_rectangle_center = [int(x + w / 2), int(y + h / 2)]

        # 픽셀값과 실제 가로, 세로 길이 비율
        proportion_x = 40 / 600
        proportion_y = 50 / 150000

        # 비율 적용한 가로 길이(화면상의 정가운데 픽셀값 - 이동한거리에 따른 픽셀값 * 비율)
        real_x = (center_x - cv2_rectangle_center[0]) * proportion_x

        # 비율 적용한 세로 길이(화면에 인식되는 얼굴의 사각형의 넓이 * 비율)
        real_y = w * h * proportion_y

        # 빗변 길이(피타고라스 사용)
        real_r = (real_x ** 2 + real_y ** 2) ** 0.5

        # 높이/빗변으로 sin값 받아오기
        sin_x = real_x / real_r

        # sin값이 -1에서 1사이가 아닐 경우 예외 처리
        if not -0.99 <= sin_x <= 0.99:
            continue

        # 아크사인값으로 각도값 받아오기 및 디그리 변환
        rad = math.asin(sin_x)
        degree = round(math.degrees(rad), -1)

        text = str(1) if idx == 1 else str(2)
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1
        thickness = 2
        text_size, _ = cv2.getTextSize(text, font, font_scale, thickness)
        text_x = x + w + 10
        text_y = y + int(h / 2) + int(text_size[1] / 2)
        cv2.putText(frame, text, (text_x, text_y), font, font_scale, (0, 255, 0), thickness, cv2.LINE_AA)

        # degree값의 평균필터 5개의 값마다 degree 평균출력
        print("noise degree: ", degree)
        if idx == 1:
            degree_average = 0
            degree_array.append(degree + 90)
            if len(degree_array) > 5:
                degree_array.pop(0)
            degree_average = sum(degree_array) / len(degree_array)
            pub.publish(int(round(degree_average, -1)))

        # count = 0
        # if idx == 1:
        #     degree_array.append(degree + 80)
        # if idx == 1 and len(degree_array) > 5:
        #     degree_average = sum(degree_array) / len(degree_array)
        #     pub.publish(int(round(degree_average, -1)))
        #     degree_array.pop(0)
    # 감지된 얼굴과 ROIs가 포함된 프레임을 표시
    cv2.imshow('Video', frame)

    # 'q' 키가 눌리면 반복문을 종료합니다
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 비디오 캡처를 해제 및 윈도우 종료
cap.release()
cv2.destroyAllWindows()

           
