# EMOTIBOT: Face Tracking and Emotion-Responsive Robot

### Member :

[윤우성(Woosung Yun )](https://github.com/ggh-png) , [최인규(Ingyu Choi)](https://github.com/ingyu0808), [이민혁(Minhyuk Lee)](https://github.com/robotDevelop), [김대완(Daewan Kim)](https://github.com/dawan0111), [김민호(Minho Kim)](https://github.com/Realminho), [김경현(Kyunghyun Kim)](https://github.com/Kyung-Hyun36), [고건영(Geonyoeng Go)](https://github.com/GogeonYoeng), [김시온(Sion Kim)](https://github.com/kkksion), [이현승(Hyunseung Lee)](https://github.com/lhs7358)

[![Video Label](https://user-images.githubusercontent.com/71277820/229018411-f07b4968-bd42-49c3-8d1f-664b5eae80e9.jpg)][(https://www.youtube.com/watch?v=m5WHLP0AGW0&t=1s)]

( 위 이미지를 클릭하시면 데모 링크를 보실 수 있습니다.)

EMOTIBOT은 다이나믹셀로 구성된 얼굴이 있는 로봇이다. 사용자의 얼굴 위치를 추정하여, 다이나믹셀을 이용해 눈 마주침을 가능하게 한다. 또한, 사용자가 "하이 이모티"라고 말하면, 감정적인 질문을 할 수 있는 기능이 생기며, 이 질문은 GPT API에 입력되어 상담사가 직접 답변하는 것과 같이 사용자의 감정 상태에 따라 답변을 해준다.

### **기술 스택**

---

EMOTIBOT은 다음과 같은 기술 스택을 사용한다.

- STT (Speech-to-Text) : 사용자의 음성 입력을 인식하기 위해 사용된다.
- TTS (Text-to-Speech) : 로봇의 음성 출력을 위해 사용된다.
- GPT-3.5 Turbo : 사용자의 감정 상태를 파악하여 대화하기 위해 사용된다.
- OpenCV : 얼굴 인식을 위해 OpenCV의 Cascade Classifier를 사용한다.
- ROS(Noetic) : 로봇의 다양한 노드 간 통신을 위해 사용된다.
- Dynamixel : 로봇의 눈 움직임을 구현하기 위해  사용된다.
- Arduino : 로봇이의 상태를 neo led를 통해 알아보기 위해 사용된다.

### **기능**

---

EMOTIBOT의 기능은 다음과 같다.

- 얼굴 위치 추정 기능 : OpenCV Cascade Classifier를 사용하여 사용자의 얼굴 위치를 추정하고, 추정된 위치를 이용해 다이나믹셀을 이용해 로봇의 눈을 움직인다.
- 감정 상태 인식 기능 : 사용자의 음성 입력을 통해 감정 상태를 인식하고, GPT-3.5 Turbo를 이용해 상담사와 대화하듯이 사용자와 대화한다.
- 음성 출력 기능 : TTS API를 이용해 사용자와 대화하거나, 다양한 알림을 제공한다.

### ****Hardware Architecture****

---

![emoti2](https://user-images.githubusercontent.com/71277820/229018453-7f779820-db51-48f2-86ec-d5417581d183.jpeg)

### Workflow & NodeGraph

---

![emotiflow](https://user-images.githubusercontent.com/71277820/229275157-437aedc9-78b6-4813-8798-c089c40bcf09.png)


![EMOTI_graph](https://user-images.githubusercontent.com/71277820/229018476-8cc22a08-1a2a-4687-bc25-529a08dde858.png)

### install

---

```bash

cd ~/catkin_ws/src
git clone https://github.com/ggh-png/EMOTIROBOT.git
git clone https://github.com/ROBOTIS-GIT/DynamixelSDK.git
cd ~/catkin_ws && catkin_make
```

```bash
pip install pyaudio
pip install google-cloud-speech
pip install google-cloud-texttospeech
pip install playsound
pip install six
pip install openai
```

### launch

---

```bash
roslaunch EMOTI_core EMOTI_core.launch
```
