#create a list of all embeddings and ids
from config import basedir, dir_photos, dir_links, dir_faces, dir_embs
from face_recognize import is_same, batch_size, image_size
import pickle
import os
from tqdm import tqdm
import numpy as np
from scipy import misc
import shutil
import pickle
import sys

sys.path.append('/media/b/faces/vkfaces_web/ml')
from facenet_embedding import im_to_embedding, dist, ClassifierNN
sys.path.append('/media/b/faces/vkfaces_web/ml') #TODO
from detector import get_faces
from trained_classifier import get_classifier, embs, ids

cl = get_classifier()
good = 0
c = 0
for emb, id in zip(embs, ids):
    k = 1
    predicted_ids, predicted_photo_ids, dists = cl.classifyK(emb, 4)
    # print(probs)
    if any(id == predicted_ids[1:]):  # compare with 2nd element, bcs 1st is always true.
        good += 1
    c += 1
    if c % 10 == 0:
        print('top ', k, ' accuracy ', good / c)

print('top ', k, ' accuracy ', good / c)

if 0: #test on lfw #TODO
    sys.path.append('/home/administrator/')
    from validate_lfw18 import ValidateLFW

    validator = ValidateLFW()
    validator.process_images(lambda im: get_faces(im),
                             lambda im: im_to_embedding(im, image_size),
                             batch_size)
    validator.compare(dist, is_same)
