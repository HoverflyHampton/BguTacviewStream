from bgu_tacview.BGUTranslator import BGUTranslator
from bgu_tacview.TelemetryStreamer import TelemetryStreamer
import threading
import time
import sys

def main(inputFile):
    translator = BGUTranslator(inputFile)
    stream = TelemetryStreamer(translator)
    streamThread = threading.Thread(target=stream.start)
    transThread = threading.Thread(target=translator.startCraftLoop)
    streamThread.start()
    while True:
        if stream.connected:
            break
        time.sleep(0.1)
    transThread.start()
    transThread.join()
    stream.quit = True
    streamThread.join()

if __name__ == "__main__":
    main(sys.argv[1])