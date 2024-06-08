import cv2
import os
import numpy as np


class FrontalFaceDetector:
    FONT = cv2.FONT_HERSHEY_COMPLEX
    TEXT_COLOR = (0, 255, 255)
    BOX_COLOR = (0, 0, 255)
    THICKNESS = 1
    SCALE = 1

    def __init__(self, effects):

        current_dir = os.path.dirname(os.path.realpath(__file__))
        cascade_path = os.path.join(current_dir, 'Haarcascade', 'haarcascade_frontalface_default.xml')

        self.face_cascade = cv2.CascadeClassifier(cascade_path)
        self.effects = effects

    def detect_faces(self, frame: np.ndarray) -> None:

        try:
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(frame_gray, 1.2, 8)

            for (x, y, w, h) in faces:
                dims = [x, y, w, h]
                self.draw_rectangle(frame, dims)

        except Exception as e:
            print(f"Ошибка. Лицо не найдено: {e}")

    def draw_rectangle(self, frame, dims):
        try:
            x, y, w, h = dims
            if self.effects is None:
                cv2.rectangle(frame, (x, y), (x + w, y + h), self.BOX_COLOR, self.THICKNESS)
            elif self.effects == 'blur':
                x2 = x + w
                y2 = y + h

                blur_img = cv2.blur(frame[y:y2, x:x2], (50, 50))

                frame[y:y2, x:x2] = blur_img
        except Exception as e:
            print(f"Ошибка. Невозможно выделить лицо: {e}")