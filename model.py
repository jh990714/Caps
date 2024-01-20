import cv2
import numpy as np
from os import listdir
from os.path import isdir, isfile, join

def train_model(name) :
    data_path = 'faces/' + name + '/'
    face_pics = [f for f in listdir(data_path) if isfile(join(data_path,f))]
    Training_Data, Labels = [], []
    for i, files in enumerate(face_pics):
        image_path = data_path + face_pics[i]
        images = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if images is None:
            continue    
        Training_Data.append(np.asarray(images, dtype=np.uint8))
        Labels.append(i)
    if len(Labels) == 0:
        print("학습 실패")
        return None
    Labels = np.asarray(Labels, dtype=np.int32)
    model = cv2.face.LBPHFaceRecognizer_create()
    model.train(np.asarray(Training_Data), np.asarray(Labels))
    print("학습 완료")
    
    return model

def train_models():
    #faces 폴더의 하위 폴더를 학습
    data_path = 'faces/'
    # 폴더만 색출
    model_dirs = [f for f in listdir(data_path) if isdir(join(data_path,f))]
    
    #학습 모델 저장할 딕셔너리
    models = {}
    # 각 폴더에 있는 얼굴들 학습
    for model in model_dirs:
        print('model : ' + model)
        # 학습 시작
        result = train_model(model)
        # 학습이 안되었다면 패스!
        if result is None:
            continue
        # 학습되었으면 저장
        print('model2 : ' + model)
        models[model] = result

    # 학습된 모델 딕셔너리 리턴
    return models 

def model_detector(models, face_rects, result_img):
    if face_rects is():
        return False
    
    user_rects = []
    for (x1,y1,x2,y2) in face_rects:
        min_score = 999
        rect = (x1,y1,x2,y2)
        roi = result_img[y1:y2, x1:x2]
        roi = cv2.resize(roi, (200,200))
        roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        
        for key, model in models.items():
            result = model.predict(roi)
            if min_score > result[1]:
                min_score = result[1]
        if min_score < 100:
            confidence = int(100*(1-(min_score)/300))
            if confidence > 70:
                user_rects.append(rect)
        
    return user_rects