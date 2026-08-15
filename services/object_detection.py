from ultralytics import YOLO

class YOLOService:
    def __init__(self):
        self.yolo_model = YOLO("assets/models/yolov8n.pt")
        self.cheating_objects = ['cell phone', 'laptop', 'book', 'headphones']
        self.face_class_id = 0
        self.min_confidence = 0.5
        self.face_match_threshold = 0.6


    def apply_yolo(self,image_numpy):
        detected_objects = self.yolo_model(image_numpy)
        return detected_objects

