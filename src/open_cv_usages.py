import numpy as np
import cv2

# img = cv2.imread('assets/python_logo.jpg', 1)
# cv2.imshow('Image', img)
# cv2.waitKey(1000)
# cv2.destroyAllWindows()
from src.utils import get_darkness_blobs, get_darkened_pixels

print(get_darkness_blobs([0, 1, 2, 3, 6, 7, 8, 10, 11]))


cap = cv2.VideoCapture(1)  # (0) is the laptop's cam, (1) is the external webcam
while True:
    ret, frame = cap.read()
    width = int(cap.get(3))
    height = int(cap.get(4))

    image = np.zeros(frame.shape, np.uint8)
    image[180] = frame[180]

    # smaller_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
    # image[:height // 2, : width // 2] = cv2.rotate(smaller_frame, cv2.cv2.ROTATE_180)
    # image[:height//2, : width//2] = cv2.rotate(smaller_frame, cv2.cv2.ROTATE_180)
    # image[height//2:, : width//2] = smaller_frame
    # image[:height//2, width//2:] = smaller_frame
    # image[height//2:, width//2:] = smaller_frame

    cv2.imshow('frame', image)
    print(get_darkened_pixels(frame))
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
