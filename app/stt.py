from google.cloud import speech


def transcribe_audio(audio_content: bytes) -> str:
    """Transcribe the given audio content.
    Args:
        audio_content (bytes): Audio contents as bytes.
    Returns:
        str: The response containing the transcription results
    """
    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(content=audio_content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        #sample_rate_hertz=16000,
        language_code="en-US",
    )

    response = client.recognize(config=config, audio=audio)

    return ''.join(
            [result.alternatives[0].transcript for result in response.results])
