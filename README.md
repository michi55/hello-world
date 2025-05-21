# hello-world

TEST
WWW
AAA

## Transcribing audio files

This repository includes a command line tool `transcribe.py` that uses the
`speech_recognition` package to convert an audio file to text. Install the
dependency first:

```bash
pip install SpeechRecognition
```

Then run the script specifying a WAV/AIFF/FLAC file:

```bash
python transcribe.py path/to/your_audio.wav
```

The tool prints the recognized Japanese text to standard output. Use the
`-o` option to save the result to a file and `-l` to change the recognition
language. Example:

```bash
python transcribe.py audio.wav -o result.txt -l ja-JP
```
