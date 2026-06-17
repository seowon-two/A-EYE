from gtts import gTTS

def speak_medicine_info(medicine: dict):
    text = f"{medicine['ko_name']}. {medicine['guide']} {medicine['usage']} 주의사항: {medicine['warning']}"
    tts = gTTS(text=text, lang="ko")
    tts.save("output.mp3")
    return "output.mp3"
