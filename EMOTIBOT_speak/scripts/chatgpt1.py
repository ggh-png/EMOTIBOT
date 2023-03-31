#!/usr/bin/env python3

import openai
import rospy
import sys
import playsound
import time
import os.path
from std_msgs.msg import String

from google.cloud import texttospeech

from EMOTIBOT_speak.srv import stt, sttResponse

flag = 0

OPENAI_API_KEY = 'please input openai key'

openai.api_key = OPENAI_API_KEY

#모델 - GPT 3.5 Turbo 선택

model = "gpt-3.5-turbo"

messages = [{"role": "system", "content": "너는 좋은 상담사가되어 100자 이내로 답변 해줘"}]
# messages = []



def make_tts(input_text):
    file_path = os.path.expanduser(os.path.join('~', 'config/stt_key.json'))
    client = texttospeech.TextToSpeechClient.from_service_account_file(file_path)

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=input_text)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.VoiceSelectionParams(
        language_code="ko-KR", ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open("output1.mp3", "wb") as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        print('Audio content written to file "output1.mp3"')

    playsound.playsound("output1.mp3")


def chatgpt(data):
    pub = rospy.Publisher('EMOTI/neo', String, queue_size=10)


    global flag, end_time  #질문 작성하기
    start_time = time.time()
    

    question = data.input_message 
    print(question)

    if flag == 0:
        if question.strip() == "하이 이모티":
            pub.publish("speaking")
            flag = 1
            make_tts("네")
            end_time = time.time()
        return sttResponse("네")

    if flag == 1:
        messages.append({"role": "user", "content": f"{question}"})

        # ChatGPT API 호출하기
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages
        )

        answer = response['choices'][0]['message']['content'].strip()

        print("--------답변 생성 중 --------")

        messages.append({"role": "assistant", "content": f"{answer}"}) 
        print(answer)
        make_tts(answer)
        pub.publish("wait")
        flag = 0
     
        return sttResponse(answer)


def listener():
    rospy.init_node('EMOTI_chatgpt', sys.argv)
    s = rospy.Service('stt', stt, chatgpt)
    rospy.spin()

if __name__ == '__main__':
    listener()