from lib.detetions.ObjectDetectionMaster import ObjectDetectionMaster


bestEggs=""
yolov8n="../traingModel/weights/falldown_x.pt"
yolo_best = "C:/Users/anyang/Desktop/project/backend/traingModel/weights/falldown_x.pt"

sizeOfScreen=(960,640)

ob=ObjectDetectionMaster(yolo_best,sizeOfScreen)
def mainMaster(frame):
    frame,class_id=ob.detectionSupervision(frame)
    return frame,class_id