import cv2
import numpy as np
import math
import keyboard
# Define a callback function for mouse events
RTSP_URL = 'rtsp://admin:admin89881599@192.168.3.210:554/h264/ch1/main/av_stream'
from DrawRect import DrawRect
dragging = False #设置鼠标移动
rect = DrawRect()
def catch_mouse_event(event, x, y, flags, param):
    global dragging
    if event == cv2.EVENT_RBUTTONDOWN:
        rect.collect_point([x,y])
        print(rect.get_data())
    if event == cv2.EVENT_LBUTTONDOWN:
        dragging = True
        print(rect.check_selected([x,y]))
        rect.set_selected([x,y])
    elif event == cv2.EVENT_MOUSEMOVE and dragging:
        rect.move_selected([x, y])
    elif event == cv2.EVENT_LBUTTONUP:
        dragging=False

# load the video file
cap = cv2.VideoCapture(RTSP_URL)
# create a window to display the video
cv2.namedWindow('Video')
# set the mouse callback function
cv2.setMouseCallback('Video', catch_mouse_event)

while True:
    ret, frame = cap.read()
    rect.pass_frame(frame)
    if not ret:
        break
    rect.draw_points()
    frame = rect.draw_rect()
    cv2.imshow('Video', frame)
    key = cv2.waitKey(1)
    check_save = keyboard.is_pressed('enter')
    if check_save:
        rect.save()
    check_load = keyboard.is_pressed('ctrl+l')
    if check_load:
        rect.load()

    if key == ord('q'):
        break

# release the video capture and close the window
cap.release()
cv2.destroyAllWindows()
