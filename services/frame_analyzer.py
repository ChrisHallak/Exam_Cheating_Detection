import os
from services.image_helper import ImageHelper
from services.object_detection import YOLOService
from PIL import Image
from typing import List, Tuple
import numpy as np
import mediapipe as mp

# Initialize MediaPipe FaceMesh globally
mp_face_mesh = mp.solutions.face_mesh

Actual_YOLO_Objects = [
    'cell phone',
    'mobile phone',
    'smartphone',
    'book',
    'laptop',
    'headphones',
]

detector = YOLOService()


class FrameAnalyzer:
    def __init__(self):
        self.CHEATING_OBJECTS = [
            'cell phone', 'mobile phone', 'smartphone',
            'book',
            'notebook',
            'laptop',
            'tablet',
            'headphones', 'earphones',
            'paper', 'note',
            'calculator'
        ]
        self.CHEATING_OBJECTS_MAP = {
            'cell phone': 'MOB',
            'mobile phone': 'MOB',
            'smartphone': 'MOB',
            'book': 'BOK',
            'notebook': 'NOT',
            'laptop': 'LAP',
            'tablet': 'TAB',
            'headphones': 'HED',
            'earphones': 'HED',
            'paper': 'NOT',
            'note': 'NOT',
            'calculator': 'CAL'
        }

        # Initialize FaceMesh once in __init__
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            min_detection_confidence=0.5
        )

    @staticmethod
    def _filter_boxes_by_classes(detections, target_classes: List[str]) -> Tuple[
        List[List[int]], List[str], List[float]]:
        boxes = []
        class_names = []
        confidences = []

        for box in detections[0].boxes:
            class_id = int(box.cls)
            class_name = detector.yolo_model.names[class_id]
            if class_name in target_classes:
                boxes.append(box.xyxy[0].cpu().numpy().astype(int).tolist())
                class_names.append(class_name)
                confidences.append(float(box.conf))

        return boxes, class_names, confidences

    @staticmethod
    def _extract_face_crops(frame_rgb: np.ndarray, boxes: List[List[int]], margin: int = 50) -> List[np.ndarray]:
        crops = []
        h, w = frame_rgb.shape[:2]

        for box in boxes:
            x1, y1, x2, y2 = box

            box_width = x2 - x1
            box_height = y2 - y1

            face_x1 = x1 + int(box_width * 0.25)
            face_x2 = x2 - int(box_width * 0.25)
            face_y1 = y1 + int(box_height * 0.25)
            face_y2 = y2 - int(box_height * 0.5)

            face_x1 = max(0, face_x1 - margin)
            face_x2 = min(w, face_x2 + margin)
            face_y1 = max(0, face_y1 - margin)
            face_y2 = min(h, face_y2 + margin)

            face_crop = frame_rgb[face_y1:face_y2, face_x1:face_x2]

            if face_crop.size > 0 and face_crop.shape[0] > 10 and face_crop.shape[1] > 10:
                crops.append(face_crop)

        return crops

    @staticmethod
    def _preprocess_image(pil_image, frame_id):
        np_image = ImageHelper.convert_pil_to_numpy(pil_image)
        return np_image

    def analyze_frame(self, pil_frame: Image.Image, frame_id):
        try:
            np_frame_image = self._preprocess_image(pil_frame, frame_id)

            detections = detector.apply_yolo(np_frame_image)

            person_boxes, _, _ = self._filter_boxes_by_classes(detections, ['person'])
            people_count = len(person_boxes)

            if people_count < 1:
                frame_report = {
                    'violations': ["ABS"],
                    'angles': [],
                }
                return frame_report
            elif people_count > 1:
                frame_report = {
                    'violations': ["ADP"],
                    'angles': [],
                }
                return frame_report
            else:
                face_crops = self._extract_face_crops(np_frame_image, person_boxes, margin=70)
                if not face_crops:
                    frame_report = {
                        'violations': ['AMB'],
                        'angles': [],
                    }
                    return frame_report

                angles = []
                face_image_numpy = face_crops[0]
                results = self._extract_angles_geometry(face_image_numpy)

                if results is not None and "pitch" in results and "yaw" in results:
                    angles.append(int(results["pitch"]))
                    angles.append(int(results["yaw"]))

                    cheating_objects, cheating_class_names, cheating_confidences = self._filter_boxes_by_classes(
                        detections, self.CHEATING_OBJECTS)

                    cheating_objects_codes = list({
                        self.CHEATING_OBJECTS_MAP.get(name, '')
                        for name in cheating_class_names
                        if name in self.CHEATING_OBJECTS_MAP
                    })

                    violations = cheating_objects_codes

                    frame_report = {
                        'violations': violations,
                        'angles': angles,
                    }
                    return frame_report
                else:
                    frame_report = {
                        'violations': ['AMB'],
                        'angles': [],
                    }
                    return frame_report

        except Exception as e:
            print(f"Error in frame analysis: {str(e)}")
            raise

    def _extract_angles_geometry(self, frame):
        """Extract head pose angles using MediaPipe FaceMesh"""
        try:
            # Convert to RGB if needed (MediaPipe expects RGB)
            if frame.shape[2] == 3 and frame.dtype == np.uint8:
                # MediaPipe expects RGB, but if your frame is BGR, convert
                # Assuming frame is already RGB from PIL conversion
                results = self.face_mesh.process(frame)

                if results.multi_face_landmarks:
                    landmarks = results.multi_face_landmarks[0].landmark

                    # Get key points (normalized coordinates)
                    left_eye = (landmarks[33].x, landmarks[33].y)
                    right_eye = (landmarks[263].x, landmarks[263].y)
                    nose_tip = (landmarks[1].x, landmarks[1].y)
                    mouth_center = (
                        (landmarks[61].x + landmarks[291].x) / 2,
                        (landmarks[61].y + landmarks[291].y) / 2
                    )

                    # Calculate roll (head tilt)
                    dY = right_eye[1] - left_eye[1]
                    dX = right_eye[0] - left_eye[0]
                    roll = np.degrees(np.arctan2(dY, dX)) - 180

                    # Calculate pitch (nodding up/down)
                    nose_mouth_dist = np.sqrt(
                        (nose_tip[0] - mouth_center[0]) ** 2 +
                        (nose_tip[1] - mouth_center[1]) ** 2
                    )
                    eyes_mouth_dist = np.sqrt(
                        ((left_eye[0] + right_eye[0]) / 2 - mouth_center[0]) ** 2 +
                        ((left_eye[1] + right_eye[1]) / 2 - mouth_center[1]) ** 2
                    )

                    # Avoid division by zero
                    if eyes_mouth_dist > 0:
                        pitch = np.degrees(np.arcsin(np.clip(nose_mouth_dist / eyes_mouth_dist, -1.0, 1.0)))
                    else:
                        pitch = 0

                    # Calculate yaw (turning left/right)
                    eye_center_x = (left_eye[0] + right_eye[0]) / 2
                    face_width = np.abs(right_eye[0] - left_eye[0])
                    if face_width > 0:
                        yaw = (nose_tip[0] - eye_center_x) / (face_width / 2) * 45
                    else:
                        yaw = 0

                    return {'pitch': pitch, 'yaw': yaw, 'roll': roll}

            return None

        except Exception as e:
            print(f"Error extracting angles: {str(e)}")
            return None


def save_frame_as_jpg(pil_frame, frame_name, folder_path):
    save_folder_path = os.path.join('images', folder_path)
    os.makedirs(save_folder_path, exist_ok=True)

    filename = os.path.join(save_folder_path, f"frame_{frame_name}.jpg")

    if pil_frame.mode in ("RGBA", "P"):
        pil_frame = pil_frame.convert("RGB")

    try:
        pil_frame.save(filename, format="JPEG")
        print(f"Saved image to {filename}")
    except Exception as save_err:
        print(f"Failed to save image: {save_err}")