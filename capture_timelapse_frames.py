# import all the necessary packages
from imutils.video import VideoStream
from datetime import datetime
import argparse
import signal
import time
import cv2
import sys
import os

# helper function to handle properly the intereption of the program with ctrl+c
def signal_handler(sig, frame):
    print("[INFO] You pressed 'ctrl+c' Your picture are saved"\
        " in the output directory you specified...")
    sys.exit(0)

def main(args):
    # Initialize the output directory path
    outputDir = os.path.join(args.output,datetime.now().strftime("%Y-%m-%d-%H%M"))
    os.makedirs(outputDir)

    print("[INFO] warming up camera...")
    vs = VideoStream(usePiCamera=False, resolution=(1920,1280),framerate=30).start()
    time.sleep(2)

    count = 0

    # Signal trap to handle keyboard interrupt
    signal.signal(signal.SIGINT, signal_handler)
    print("[INFO] Press 'ctrl+c' to exit, or 'q' to quit if you have the display option on...")

    # Loop  over frames from the video stream
    while True:
        frame = vs.read()
        ts = datetime.now().strftime("%A %d %B %Y %I:%M:%S%p")
        cv2.putText(frame, ts, (10, frame.shape[0]-10),cv2.FRONT_HERSHEY_SIMPLEX,
                    0.35,(0,0,255),1)
        filename = "{}.jpg".format(str(count).zfill(16))
        cv2.imwrite(os.path.join(outputDir,filename),frame)
        if args.display:
            cv2.imshow("frame",frame)
            key = cv2.waitkey(1) & 0xFF

            if key == ord("q"):
                break
        count += 1

        # Sleep for specified number of stream
        time.sleep(args.delay)
    
    # Clean up, close any open windows and release videos
    print("[INFO] Cleaning up...")
    if args.display:
        cv2.destroyAllWindows()
    vs.stop()



if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output', required=True,help="path to the output directory")
    parser.add_argument('--delay',type=float,default=5.0,help="delay in seconds between frames captured")
    parser.add_argument('--display',type=int,default=0,help="boolean used to indicate if frames should be displayed")
    
    args=parser.parse_args() 
    main(args)