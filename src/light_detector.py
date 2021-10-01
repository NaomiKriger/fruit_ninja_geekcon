# import argparse
#
# import cv2
#
#
# cap = cv2.VideoCapture(0)  # (0) is the laptop's cam, (1) is the external webcam
#
#
# def get_blue_blob_position():
#     ret, frame = cap.read()
#     for col in frame:
#         for pixel in col:
#             pixel[0] = 0
#             pixel[1] = 0
#
#     gray_full = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
#     (minVal_f, maxVal_f, minLoc_f, maxLoc_f) = cv2.minMaxLoc(gray_full)
#     cv2.circle(frame, maxLoc_f, 30, (0, 0, 255), 2)
#
#     cv2.imshow("Robust", frame)
#
#
# cap.release()
# cv2.destroyAllWindows()
