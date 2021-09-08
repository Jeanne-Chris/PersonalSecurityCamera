# Import library
import cv2
from pygame import mixer

# Initiate mixer to load sound clip
mixer.init()
mixer.music.load("alert.mp3")

# Initiate camera to capture the current frame
cam = cv2.VideoCapture(0)

while cam.isOpened():
    r, frame = cam.read()
    r, newFrame = cam.read()

    compareFrame = cv2.absdiff(frame, newFrame)
    gray = cv2.cvtColor(compareFrame, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, threshold = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(threshold, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) < 5000:
            continue
        x, y, w, h = cv2.boundingRect(contour)

        # Draw a rectangle if movement is detected
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        # Pray alert sound for any movement detected
        mixer.music.play()

    # Press 'q' to quit application
    if cv2.waitKey(10) == ord('q'):
        break
    cv2.imshow("Personal Security Camera", frame)
