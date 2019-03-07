import numpy as np
from mtcnn.mtcnn import MTCNN
minsize = 40 # minimum size of face
threshold = [ 0.6, 0.7, 0.7 ]  # three steps's threshold
factor = 0.709 # scale factor

detector = MTCNN(min_face_size=minsize, steps_threshold=threshold, scale_factor=factor)

margin = 44


def get_faces(im, margin):
    if len(im.shape) == 2:
        im = np.stack([im, im, im], axis=2)  # make it rgb from grayscaled
    faces = detector.detect_faces(im)
    for i, face in enumerate(faces):
        bb = face['box']
        x1, x2, y1, y2 = bb[1], bb[1] + bb[3], bb[0], bb[0] + bb[2]
        x1, y1 = max(x1 - margin // 2, 0), max(y1 - margin // 2, 0)
        x2, y2 = min(x2 + margin // 2, im.shape[0]), min(y2 + margin // 2, im.shape[1])

        yield im[x1:x2, y1:y2, ...]
