from openai import OpenAI
from playsound import playsound
import speech_recognition as sr



class AssistiveFeatures:
    def __init__(self, openai_api_key):
        self.openai_api_key = openai_api_key
        self.recognizer = sr.Recognizer()

    def tts_service(self, input_text):
        client = OpenAI(
            api_key=self.openai_api_key
        )

        speech_file_path = "tts_audio.mp3"

        # TTS API 호출
        response = client.audio.speech.create(
            model="tts-1",
            input=input_text,
            voice="alloy",
            response_format="mp3",
            speed=1.1,
        )

        response.stream_to_file(speech_file_path)
        playsound(speech_file_path)

    def stt_service(self):
        with sr.Microphone() as source:
            print("듣고 있습니다!")
            audio = self.recognizer.listen(source)

            try:
                print("인식된 텍스트: " + self.recognizer.recognize_google(audio, language='ko-KR'))
                stt_user_input = self.recognizer.recognize_google(audio, language='ko-KR')

            except sr.UnknownValueError:
                print("Google Web Speech API가 당신의 말을 이해하지 못했습니다.")
            except sr.RequestError as e:
                print(f"Google Web Speech API 서비스에 문제가 발생했습니다; {e}")

        return stt_user_input
