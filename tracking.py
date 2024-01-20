import cv2
import numpy as np


class Tracking:        
    def __init__(self):
        self.trackerTypes = ['BOOSTING', 'MIL', 'KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
        #트랙킹 설정
        self.trackerType = "CSRT"
        self.multiTracker = cv2.legacy.MultiTracker_create()
    def multiTracker_clear(self):
        self.multiTracker = cv2.legacy.MultiTracker_create()
        return self.multiTracker 
    
    def createTrackerByName(self, trackerType):
        # tracker종류 
        if trackerType == self.trackerTypes[0]:
            tracker = cv2.legacy.TrackerBoosting_create()
        elif trackerType == self.trackerTypes[1]:
            tracker = cv2.legacy.TrackerMIL_create()
        elif trackerType == self.trackerTypes[2]:
            tracker = cv2.legacy.TrackerKCF_create()
        elif trackerType == self.trackerTypes[3]:
            tracker = cv2.legacy.TrackerTLD_create()
        elif trackerType == self.trackerTypes[4]:
            tracker = cv2.legacy.TrackerMedianFlow_create()
        elif trackerType == self.trackerTypes[5]:
            tracker = cv2.legacy.TrackerGOTURN_create()
        elif trackerType == self.trackerTypes[6]:
            tracker = cv2.TrackerMOSSE_create()
        elif trackerType == self.trackerTypes[7]:
            tracker = cv2.legacy.TrackerCSRT_create()
        else:
            tracker = None
            for t in self.trackerTypes:
                print(t)
                
        return tracker

    def object_tracking(self, result_img):
        #등록 대상 tracking 
        tracking_rects = []
        success, boxes = self.multiTracker.update(result_img)
        if success:  # tracking 대상 좌표 저장
            for i, newbox in enumerate(boxes):
                x1 = int(newbox[0])
                y1 = int(newbox[1])
                x2 = int(newbox[0] + newbox[2]) 
                y2 = int(newbox[1] + newbox[3])
                    
                tracking_rect = (x1, y1, x2, y2)
                tracking_rects.append(tracking_rect)
        else: 
            # 사라진 tracking 대상 지우기 
            i = np.where(boxes.sum(axis=1) != 0)[0]
            trackers_arr=boxes[i]
            self.multiTracker_clear()
            for rect in trackers_arr:
                self.multiTracker.add(self.createTrackerByName(self.trackerType), result_img, tuple(rect))
                
        return tracking_rects

                    
    def add_Tracking(self, rect, tracking_rects, result_img):
        x1, y1, x2, y2 = rect
        tracking_rects.append(rect)
        self.multiTracker.add(cv2.legacy.TrackerCSRT_create(), result_img, (x1, y1, (x2-x1), (y2-y1)))
        
        return tracking_rects
    
    def prt_Tracking(self, tracking_rects, result_img) :
        for rect in tracking_rects:
            x1, y1, x2, y2 = rect
            cv2.rectangle(result_img, (x1, y1), (x2, y2), (255, 0, 0), 2, cv2.LINE_AA)