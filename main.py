from PIL import ImageGrab
import cv2
import numpy as np
import mouse
import pytesseract
from mosaic import *
from tracking import *
from object_detection import *
from model import *
from gui import *

# app 개발 시 분리 예정
def mouse_event(event, x, y, flags, param):
    tracking_rects = param
    
    if event == cv2.EVENT_LBUTTONDBLCLK:    
        rect = object.pointInRect((x, y), face_rects)
        if rect :
            #모자이크 해제
            mosaic_rect = object.overlap(rect, mosaic_rects)
            if mosaic_rect : 
                tracking_rects = tracking.add_Tracking(mosaic_rect, tracking_rects, result_img)
                return
           
            #모자이크 처리
            tracking_rect = object.overlap(rect, tracking_rects)
            if tracking_rect :
                tracking_rects = add_Mosiac(tracking_rect, tracking, tracking_rects, result_img)

# 선택영역 표시            
def set_roi():
    print("Select your ROI using mouse drag.")
    while(mouse.is_pressed() == False):
        x1, y1 = mouse.get_position()
        while(mouse.is_pressed() == True):
            x2, y2 = mouse.get_position()
            while(mouse.is_pressed() == False):
                print("Your ROI : {0}, {1}, {2}, {3}".format(x1, y1, x2, y2))
                
                return x1, y1, x2, y2

def change_range(self):
    value = "현재 범위 값 : " + str(range_scale.get());
    range_label.config(text=value);
    set_range(range_scale.get());
    
    
def change_strength(self):
    value = "현재 강도 값 : " + str(strength_scale.get());
    strength_label.config(text=value);    
    set_strength(strength_scale.get());

window=tkinter.Tk()


window.title("Real - Time Mosaic")
window.geometry("240x150")
window.resizable(False, False)

label = ttk.Label(window, text="세팅이 완료되면 프로그램을 종료하시오...")
label.grid(row=0, column=0);

range_scale = tkinter.Scale(window, command=change_range, to=2, resolution=0.1, length=200, orient="horizontal");
range_scale.set(1);
range_scale.grid(row=1, column=0);

range_label = ttk.Label(window, text="현재 범위 값 : 0")
range_label.grid(row=2, column=0);

strength_scale = tkinter.Scale(window, command=change_strength, from_=0.1, to=0, resolution=0.01, length=200, orient="horizontal");
strength_scale.set(0.05);
strength_scale.grid(row=3, column=0);

strength_label = ttk.Label(window, text="현재 강도 값 : 0")
strength_label.grid(row=4, column=0);
window.mainloop()

# video 캠
video_path = 0
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print('eeerrrrooorrr')

# fps 계산
frame_count, tt = 0, 0

# 배율
scaler = 1

# rect 초기화
tracking_rects = []
face_rects = []

# Tracking 객체 생성
tracking = Tracking()
tracking.__init__()

# Object 객체 생성
object = Object()
object.__init__()

# user train
models = train_models()

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe '

input("imgView - enter")
img_view = set_roi()
img_view_w = img_view[2] - img_view[0]
img_view_h = img_view[3] - img_view[1]

input("numView - enter")
num_view = set_roi()

pre_point = [-1, -1]

rate_w = img_view_w / 1000
rate_h = img_view_h / 1600

while True :
    img = cv2.cvtColor(np.array(ImageGrab.grab(bbox=img_view)), cv2.COLOR_BGR2RGB)
    num_img = cv2.cvtColor(np.array(ImageGrab.grab(bbox=num_view)), cv2.COLOR_BGR2RGB)
                
    # 영상 설정
    img = cv2.resize(img, (int(img.shape[1] * scaler), int(img.shape[0] * scaler)))
    result_img = img.copy()
    
    # car 찾기
    # object.car_detect(result_img)
    
    # face 찾기
    face_rects, mosaic_rects = object.face_detect(result_img, tracking_rects)
    
    # 대상 tracking
    tracking_rects = tracking.object_tracking(result_img)
    tracking_rects = tracking.check_user(models, face_rects, tracking_rects, result_img)
    tracking.prt_Tracking(tracking_rects, result_img)
    
    # unknown 대상 모자이크
    prt_Mosaic(mosaic_rects, result_img)
    
    # mouse_event 를 통한 신원 임시 등록
    param = tracking_rects
    cv2.setMouseCallback('result', mouse_event, param=param)
    
    # 터치 이벤트를 통한 좌표값
    num_pix = num_img[1,1]
    if(num_pix[0] <= 10 or num_pix[2] <= 10):
        result = pytesseract.image_to_string(num_img, lang='kor')
        result = result.replace("\n", "")
        point = result.split(" ")
        
        if point[0].isdigit() and point[1].isdigit() and (len(point) == 2):
            point[0] = int(int(point[0])*rate_w)              
            point[1] = int(int(point[1])*rate_h)
            
            rect = object.pointInRect(tuple(point), face_rects) 
            if rect : 
                if (num_pix[0] <= 10) : #모자이크 처리   
                    tracking_rect = object.overlap(rect, tracking_rects)
                    if tracking_rect :
                        add_Mosiac(tracking_rect, tracking, tracking_rects, result_img)
                elif (num_pix[2] <= 10) : #모자이크 해제
                    mosaic_rect = object.overlap(rect, mosaic_rects)
                    if mosaic_rect : 
                        tracking.add_Tracking(mosaic_rect, tracking_rects, result_img)
                        
    # 출력
    # print("face", face_rects)
    # print("mosaic", mosaic_rects)
    # print("tracking", tracking_rects)
    
    cv2.imshow('result', result_img)
    cv2.imshow('point', num_img)
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()