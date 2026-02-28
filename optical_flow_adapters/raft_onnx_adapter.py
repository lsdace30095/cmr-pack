import os
import onnxruntime as ort
import numpy as np
import cv2

class RAFTOnnxOpticalFlow:
    def __init__(self):
        model_path = os.getenv("FLOW_MODEL_PATH")
        if not model_path:
            raise ValueError("FLOW_MODEL_PATH environment variable is not set")
        self.session = ort.InferenceSession(model_path)

    def preprocess(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        img = img.astype('float32') / 255.0
        img = np.transpose(img, (2, 0, 1))
        return np.expand_dims(img, axis=0)

    def compute(self, prev_frame, next_frame):
        inp1 = self.preprocess(prev_frame)
        inp2 = self.preprocess(next_frame)
        ort_inputs = {"input_1": inp1, "input_2": inp2}
        flow = self.session.run(None, ort_inputs)[0]
        return flow
