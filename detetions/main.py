from lib.detetions.ObjectDetectionMaster import ObjectDetectionMaster
from ultralytics import YOLO
# yolo_m = YOLO(model='yolov8m.pt')
yolo_nano = "C:/Users/anyang/Desktop/project/backend/traingModel/weights/yolov8n.pt"
yolo_best_fight_n_hul="C:/Users/anyang/Desktop/project/backend/traingModel/weights/fall_down_fight_n_hul.pt"
yolov8n="../traingModel/weights/falldown_x.pt"
yolo_bestx = "C:/Users/anyang/Desktop/project/backend/traingModel/weights/falldown_x.pt"
yolo_bestn = "C:/Users/anyang/Desktop/project/backend/traingModel/weights/falldown_n.pt"
yolo_best_fight_n = "C:/Users/anyang/Desktop/project/backend/traingModel/weights/fall_down_fight_n.pt"
sizeOfScreen=(960,640)

ob=ObjectDetectionMaster(yolo_best_fight_n,sizeOfScreen)
def mainMaster(frame):
    frame,class_id=ob.detectionSupervision(frame)
    return frame,class_id