import cv2

mosaic_strength = 0.05;
mosaic_range = 1;

def set_strength(strength):
    global mosaic_strength
    mosaic_strength = strength;

def set_range(range):
    global mosaic_range
    mosaic_range = range    
    
def add_Mosiac(rect, tracking, tracking_rects, result_img): 
    index = tracking_rects.index(rect)
    tracking_rects.pop(index)
    tracking.multiTracker = tracking.multiTracker_clear()
    for rect in tracking_rects:
        x1, y1, x2, y2 = rect
        tracking.multiTracker.add(cv2.legacy.TrackerCSRT_create(), result_img, (x1, y1, (x2-x1), (y2-y1)))
        
    return tracking_rects
    
def prt_Mosaic(rects, result_img) :     
    for rect in rects:
        x1, y1, x2, y2 = rect

        y_range = ((y2 - y1) - (y2 - y1)*mosaic_range)/2
        y1 += int(y_range)
        y2 -= int(y_range) 
        
        x_range = ((x2 - x1) - (x2 - x1)*mosaic_range)/2
        x1 += int(x_range)
        x2 -= int(x_range)
   
        # 좌표가 -값이 된 곳은 모자이크 x
        if (x1 < 0):
            x1 = 0
        if (y1 < 0):
            y1 = 0
         
        face_region = result_img[y1:y2, x1:x2]
            
        M = face_region.shape[0]
        N = face_region.shape[1]
            
        # try 오류 해결
        # 이미지 크기 조정으로 인해 발생
        try:
            face_region = cv2.resize(face_region, None, fx=mosaic_strength, fy=mosaic_strength, interpolation=cv2.INTER_AREA)
            face_region = cv2.resize(face_region, (N, M), interpolation=cv2.INTER_AREA)
        except:
            break        
        result_img[y1:y2, x1:x2] = face_region
            
        cv2.rectangle(result_img, (x1, y1), (x2, y2), (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(result_img, 'UNKNOWN', (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)