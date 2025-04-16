from transcriber import Transcriber

transcriber = Transcriber()

result = transcriber.transcribe("./test-files/trimmed.mp4")

print(result)
