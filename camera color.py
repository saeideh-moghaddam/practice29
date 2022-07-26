import cv2
import keyboard
import numpy as np

video_cap = cv2.VideoCapture(0)
frame_rate = 40

def colorDetection(frame):
    rows, cols, _ = frame.shape
    result = np.zeros((rows, cols), "uint8")
    mask = np.ones((25, 25)) / 25**2
    min_y, max_y = int(rows * (2/5)), int(rows * (3/5))
    min_x, max_x =  int(cols * (2/5)), int(cols * (3/5))
    result = cv2.filter2D(frame, -1, mask)
    result[min_y:max_y, min_x:max_x] = frame[min_y:max_y, min_x:max_x]
    cv2.rectangle(result, (min_x, min_y), (max_x, max_y), (0, 0, 0), 2)
    
    alpha = 1 
    beta = 30
    result[min_y:max_y, min_x:max_x] = cv2.convertScaleAbs(result[min_y:max_y, min_x:max_x], alpha=alpha, beta=beta)
    result_blurred = cv2.GaussianBlur(result, (3, 3), 3)
    frame_RGB = cv2.cvtColor(result_blurred, cv2.COLOR_BGR2RGB)
    R, G, B = cv2.split(frame_RGB)
    
    R_avg = int(np.average(R[min_y:max_y, min_x:max_x]))
    G_avg = int(np.average(G[min_y:max_y, min_x:max_x]))
    B_avg = int(np.average(B[min_y:max_y, min_x:max_x]))
    
    if R_avg > 240 and G_avg > 240 and B_avg > 240:
        color = "White"
    elif R_avg < 70 and G_avg < 70 and B_avg < 70:
        color = "Black"
    elif (R_avg < 170 and G_avg < 170 and B_avg < 170) and R_avg == G_avg == B_avg:
        color = "Gray"
    elif R_avg < 80 and G_avg < 80 and B_avg > 200:
        color = "Blue"
    elif R_avg > 200 and G_avg < 80 and B_avg < 80:
        color = "Red"
    elif R_avg < 80 and G_avg > 200 and B_avg < 80:
        color = "Green"
    elif R_avg > 190 and G_avg < 50 and 90 < B_avg < 120:
        color = "Magenta"
    elif R_avg > 230 and G_avg > 230 and B_avg < 80:
        color = "Yellow"
    elif R_avg < 80 and G_avg > 210 and B_avg > 210:
        color = "Cyan"
    else:
        color = "Unrecognizable"
    
    cv2.putText(result, f"RGB: ({R_avg}, {G_avg}, {B_avg})", (50, 50), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(255, 187, 0) ,thickness=1)
    cv2.putText(result, f"Color: {color}", (50, 80), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(255, 187, 0),thickness=1)
    
    return result

frame_width, frame_height = int(video_cap.get(4)), int(video_cap.get(5))
size = (frame_width, frame_height)
fourcc = cv2.VideoWriter_fourcc(*"mp4v")

while True:
    ret, frame = video_cap.read()
    if not ret or keyboard.is_pressed("q"):
        break
    
    result = colorDetection(frame)
    cv2.imshow("Color Guess", result)
    cv2.waitKey(5)

video_cap.release()
cv2.destroyAllWindows()