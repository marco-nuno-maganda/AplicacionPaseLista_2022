# https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_calib3d/py_calibration/py_calibration.html

import numpy as np
import cv2
import glob



A = [[1019.37187, 0, 618.709848], [0, 1024.2138, 327.280578], [0, 0, 1]] #hardcoded intrinsic matrix for my webcam
A = np.array(A)

def main():
#	marker_colored = cv2.imread('data/m1_flip_new.png')
	marker_colored = cv2.imread('Zorro.png')
	marker_colored =  cv2.resize(marker_colored, (480,480), interpolation = cv2.INTER_CUBIC )
	marker = cv2.cvtColor(marker_colored, cv2.COLOR_BGR2GRAY)


	cv2.namedWindow("webcam")
	vc = cv2.VideoCapture(0)

	h,w = marker.shape
	#considering all 4 rotations
	marker_sig1 = aruco.get_bit_sig(marker, np.array([[0,0],[0,w], [h,w], [h,0]]).reshape(4,1,2))
	marker_sig2 = aruco.get_bit_sig(marker, np.array([[0,w], [h,w], [h,0], [0,0]]).reshape(4,1,2))
	marker_sig3 = aruco.get_bit_sig(marker, np.array([[h,w],[h,0], [0,0], [0,w]]).reshape(4,1,2))
	marker_sig4 = aruco.get_bit_sig(marker, np.array([[h,0],[0,0], [0,w], [h,w]]).reshape(4,1,2))

	sigs = [marker_sig1, marker_sig2, marker_sig3, marker_sig4]

	rval, frame = vc.read()
	h2, w2,  _ = frame.shape
	
	h_canvas = max(h, h2)
	w_canvas = w + w2

	while rval:
		rval, frame = vc.read() #fetch frame from webcam
		key = cv2.waitKey(20) 
		if key == 27:
			break


		canvas = np.zeros((h_canvas, w_canvas, 3), np.uint8) #final display
		canvas[:h, :w, :] = marker_colored #marker for reference

		success, H = aruco.find_homography_aruco(frame, marker, sigs)
		# success = False
		if not success:
			# print('homograpy est failed')
			canvas[:h2 , w: , :] = np.flip(frame, axis = 1)
			cv2.imshow("webcam", canvas )
			continue

		R_T = get_extended_RT(A, H)
		transformation = A.dot(R_T) 
		
		augmented = np.flip(augment(frame, obj, transformation, marker, True), axis = 1) #flipped for better control
		canvas[:h2 , w: , :] = augmented
		cv2.imshow("webcam", canvas)

main()
