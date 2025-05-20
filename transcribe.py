import sys
import speech_recognition as sr


def transcribe_wav(filename):
    r = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = r.record(source)
    try:
        text = r.recognize_google(audio, language='ja-JP')
        print(text)
    except sr.UnknownValueError:
        print('Could not understand audio')
    except sr.RequestError as e:
        print(f'Could not request results: {e}')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python transcribe.py path/to/audio.wav')
        sys.exit(1)
    transcribe_wav(sys.argv[1])
