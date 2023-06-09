from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import time
from main import stop_slider, stop_camera, move_slider_left, move_slider_right, tilt_camera_up, tilt_camera_down
# initialize the camera and grab a reference to the raw camera capture
cam=cv2.VideoCapture(0)

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
	help="max buffer size")
args = vars(ap.parse_args())

orangeLower = (10, 100, 150)
orangeUpper = (30, 255, 255)

pts = deque(maxlen=args["buffer"])

if not cam.isOpened():
    print ("Error open video %s" %str(cam))
    exit()
# keep looping
stop_slider()
stop_camera()
while True:
	# grab the current frame
	(grabbed, frame) = cam.read()
	# Start timer
	timer = cv2.getTickCount()

	# if we are viewing a video and we did not grab a frame,
	# then we have reached the end of the video
	if args.get("video") and not grabbed:
		break

	# convert it to the HSV color space
	frame = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	
	# construct a mask for the color "orange", then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
	mask = cv2.inRange(hsv, orangeLower, orangeUpper)
# 	cv2.imshow('masdk', mask)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)
# 	cv2.imshow('mask', mask)
	# find contours in the mask and initialize the current
	# (x, y) center of the ball
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2]
	center = None
	# only proceed if at least one contour was found
	if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

		# only proceed if the radius meets a minimum size
		if radius > 10:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			cv2.circle(frame, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)

	#update the points queue
	pts.appendleft(center)
	cv2.line(frame, (0,int(0.7*hsv.shape[0])), (hsv.shape[1],int(0.7*hsv.shape[0])), (0, 0, 255), thickness=3)
	cv2.line(frame, (0,int(0.3*hsv.shape[0])), (hsv.shape[1],int(0.3*hsv.shape[0])), (0, 0, 255), thickness=3)
	cv2.line(frame, (int(0.7*hsv.shape[1]),0), (int(0.7*hsv.shape[1]), hsv.shape[0]), (0, 0, 255), thickness=3)
	cv2.line(frame, (int(0.3*hsv.shape[1]),0), (int(0.3*hsv.shape[1]), hsv.shape[0]), (0, 0, 255), thickness=3)
	
    
	if center is not None:
        # Right
		if center[0]> 0.7*hsv.shape[1]:
			cv2.putText(frame, "Right", (300, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)
			move_slider_right()
		# Left
		elif center[0]< 0.3*hsv.shape[1]:
			cv2.putText(frame, "Left", (300, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)
			move_slider_left()
		else:
			stop_slider()
		# Down
		if center[1]> 0.7*hsv.shape[0]:
			cv2.putText(frame, "Tilt down", (400, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)
			tilt_camera_down()
		# Up
		elif center[1]< 0.3*hsv.shape[0]:
			cv2.putText(frame, "Tilt up", (400, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)
			tilt_camera_up()
		else:
			stop_camera()
			cv2.putText(frame, "Stop", (400, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)
	else:
        # stop
		stop_slider()
		stop_camera()
		cv2.putText(frame, "Stop", (400, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)


	#loop over the set of tracked points
	for i in range(1, len(pts)):

		if pts[i - 1] is None or pts[i] is None:
			continue

		thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
		cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
	cv2.putText(frame, "HSV Tracker", (100, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)
	#Calculate Frames per second (FPS)
	fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
	# Display FPS on frame
	cv2.putText(frame, "FPS : " + str(int(fps)), (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)
	#Display ball coodirate
	cv2.putText(frame, str(center), (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)
	# show the frame to our screen
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	#if the space key is pressed, pause the loop
	if key == ord(" "):
		cv2.waitKey(0)
	# if the 'q' key is pressed, stop the loop
	if key == 27:
		break
	
# cleanup the camera and close any open windows
cam.release()
cv2.destroyAllWindows()