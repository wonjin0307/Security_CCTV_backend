from lib.detetions.ObjectDetectionMaster import ObjectDetectionMaster


bestEggs=""
yolov8n="../../traing Model/weights/yolov8n.pt"

sizeOfScreen=(640,640)

ob=ObjectDetectionMaster(yolov8n,sizeOfScreen)
def mainMaster(frame):
    ob.detectionSupervision(frame)
    return frame