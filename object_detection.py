import cv2
import cvlib as cv
from cvlib.object_detection import draw_bbox

class Object:
    def __init__(self):
        #모델 
        self.model_path = 'face_model\\opencv_face_detector_uint8.pb'
        self.config_path = 'face_model\\opencv_face_detector.pbtxt'
        self.net = cv2.dnn.readNetFromTensorflow(self.model_path, self.config_path)
        self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
        self.conf_threshold = 0.7

    def pointInRect(self, point, rects):
        for rect in rects:
            x1, y1, x2, y2 = rect
            x, y = point
        
            if (x1 < x and x < x2):
                if (y1 < y and y < y2):
                    return rect
        return False

    def overlap(self, rect, rects):
        for rect2 in rects:
            x1 = max(rect[0], rect2[0])
            y1 = max(rect[1], rect2[1])
            x2 = min(rect[2], rect2[2])
            y2 = min(rect[3], rect2[3])
    
            w = x2 - x1
            h = y2 - y1
            if (w > 0) and (h > 0):
                area_overlap = w * h
                area_rect = (rect[2] - rect[0]) * (rect[3] - rect[1])
                area_rect2 = (rect2[2] - rect2[0]) * (rect2[3] - rect2[1])
                
                iou = area_overlap / (area_rect + area_rect2 - area_overlap)
                if iou > 0.1:
                    return rect2
        return False
            
    def car_detect(self, result_img):
        #-- detect 함수 불러오기
        bbox, label, conf = cv.detect_common_objects(result_img, enable_gpu=True)
    
        
        #-- 검출 객체 박스 처리
        if label:
            out = draw_bbox(result_img, bbox, label, conf, write_conf=True)
            cv2.imshow("result", out)
        else:
            cv2.imshow("result", result_img)
            

    def face_detect(self, result_img, tracking_rects):
        # 얼굴 찾기
        h, w, _ = result_img.shape
        blob = cv2.dnn.blobFromImage(result_img, 1.0, (224, 224), [104, 117, 123], False, False)
        self.net.setInput(blob)
        face_detections = self.net.forward()
        face_rects = []
        mosaic_rects = []
        
        for i in range(face_detections.shape[2]):
            confidence = face_detections[0, 0, i, 2]
            if confidence > self.conf_threshold:
                x1 = int(face_detections[0, 0, i, 3] * w)
                y1 = int(face_detections[0, 0, i, 4] * h)
                x2 = int(face_detections[0, 0, i, 5] * w)
                y2 = int(face_detections[0, 0, i, 6] * h)
                
                face_rect = (x1, y1, x2, y2)   
                face_rects.append(face_rect)
                    
                if not self.overlap(face_rect, tracking_rects):
                    mosaic_rects.append(face_rect)
            
                cv2.rectangle(result_img, (x1, y1), (x2, y2), (0, 255, 0), 2, cv2.LINE_AA)
        return face_rects, mosaic_rects