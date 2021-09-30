import argparse

import cv2

ap = argparse.ArgumentParser()

args = vars(ap.parse_args())

cap = cv2.VideoCapture(1)  # (0) is the laptop's cam, (1) is the external webcam
while True:
    ret, frame = cap.read()
    width = int(cap.get(3))
    height = int(cap.get(4))

    gray_full = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    (minVal_f, maxVal_f, minLoc_f, maxLoc_f) = cv2.minMaxLoc(gray_full)
    print(maxLoc_f)
    cv2.circle(frame, maxLoc_f, 30, (0, 0, 255), 2)

    cv2.imshow("Robust", frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
