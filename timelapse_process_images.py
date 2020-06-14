from imutils.video import VideoStream
from imutils import paths
import progressbar
import argparse
import cv2
import os
from builtins import sorted

def get_number(imagePath):
    return int(imagePath.split(os.path.sep)[-1][:-4])

def main(args):

    # Initialize the FourCC and video writer
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    writer = None

    imagePaths = list(paths.list_images(args.input))
    outputFile = "{}.avi".format(args.input.split(os.path.sep)[2])
    outputPath = os.path.join(args.output,outputFile)

    # Building the progress bar
    print("[INFO] building {}...".format(outputPath))
    widgets = ["Building video: ",progressbar.Percentage()," ", progressbar.Bar()," ", progressbar.ETA()]
    pbar = progressbar.ProgressBar(maxval=len(imagePaths),widgets=widgets).start()

    # Buidling the output video
    for (i, imagePath) in enumerate(sorted(imagePaths,key=get_number)):
        image = cv2.imread(imagePath)
        if writer is None:
            (H,W) = image.shape[:2]
            writer = cv2.VideoWriter(outputPath, fourcc, args.fps, (W,H),True)
        writer.write(image)
        pbar.update(i)

    # Clean up, close any open windows and release videos
    print("[INFO] Cleaning up...")
    pbar.finish()
    writer.release()



if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--input', required=True,help="Path to the input directory of image files")
    parser.add_argument('--output', required=True,help="Path to the output directory of video files")
    parser.add_argument('--fps',type=int,default=30,help="frame per second of output video")
    
    args=parser.parse_args() 
    main(args)