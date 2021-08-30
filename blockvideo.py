from imutils.video import VideoStream
import argparse
import datetime
import imutils
import time
import cv2
import os
import glob
import numpy as np

duration = 0.5
freq = 440
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
args = vars(ap.parse_args())
avg = None
vs = VideoStream(src=0).start()
firstFrame = None
i = 0
# loop over the frames of the video


def sharpness(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    lap = cv2.Laplacian(img, cv2.CV_16S)
    mean, stddev = cv2.meanStdDev(lap)
    return stddev[0,0]

while True:
	# grab the current frame and initialize the occupied/unoccupied
	# text
	frame = vs.read()
	b = sharpness(frame)
	frame = frame if args.get("video", None) is None else frame[1]
	text = "undetected"
	if b < 3.2:
		os.system('play -nq -t alsa synth {} sine {}'.format(duration, freq))

	# if the frame could not be grabbed, then we have reached the end
	# of the video
	if frame is None:
		break
	# resize the frame, convert it to grayscale, and blur it
	frame = imutils.resize(frame, width=500)

	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21, 21), 0)
	# if the first frame is None, initialize it
	# if the first frame is None, initialize it
	if firstFrame is None:
		firstFrame = gray
		continue

	# compute the absolute difference between the current frame and
	# first frame
	frameDelta = cv2.absdiff(firstFrame, gray)
	thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
	# dilate the thresholded image to fill in holes, then find contours
	# on thresholded image
	thresh = cv2.dilate(thresh, None, iterations=2)
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)


	# loop over the contours
	for c in cnts:
		# if the contour is too small, ignore it
		if cv2.contourArea(c) < 5000:
			continue


	# set text to show on gui
		text = "Detected"
		# if b < 3.2:
		# 	os.system('play -nq -t alsa synth {} sine {}'.format(duration, freq))
		# cv2.imwrite(os.path.join(path, 'waka.jpg'), img)
		# path = '/home/fiveg/PycharmProjects/Hackathon/output'
		# if i % 30 == 0:
		# 	cv2.imwrite(os.path.join(path, "opencv%d.jpg" % i), frame)
		# i += 1
# draw the text and timestamp on the frame
	cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
	cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
		(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
	# count = 0
	# while frame.isOpen:
	# 	cv2.imwrite("frame%d.jpg" % count, image)
	cv2.imshow("Security Feed", frame)
	# cv2.imshow("Thresh", thresh)
	# cv2.imshow("Frame Delta", frameDelta)
	key = cv2.waitKey(1) & 0xFF
	# if the `q` key is pressed, break from the lop
	if key == ord("q"):
		break



















