"""Simple command line tool for transcribing audio files to text."""

import argparse
import sys



def transcribe_audio(filename: str, language: str = "ja-JP") -> str:
    """Transcribe a single audio file using Google Speech Recognition.

    Parameters
    ----------
    filename : str
        Path to the audio file (WAV/AIFF/FLAC).
    language : str, optional
        Language code for recognition, by default ``"ja-JP"``.

    Returns
    -------
    str
        Recognized text.
    """

    import speech_recognition as sr

    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    return recognizer.recognize_google(audio, language=language)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Transcribe an audio file using Google Speech Recognition"
    )
    parser.add_argument("input", help="path to the audio file")
    parser.add_argument(
        "-o",
        "--output",
        help="optional path for saving the transcribed text",
    )
    parser.add_argument(
        "-l",
        "--language",
        default="ja-JP",
        help="language code (default: ja-JP)",
    )
    args = parser.parse_args(argv)

    try:
        text = transcribe_audio(args.input, language=args.language)
    except Exception as e:  # pragma: no cover - errors depend on speech_recognition
        print(f"Error during transcription: {e}", file=sys.stderr)
        return 1

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(text)
    else:
        print(text)
    return 0


if __name__ == "__main__":  # pragma: no cover - manual invocation
    raise SystemExit(main())
