import os
import pickle
from config import basedir, dir_photos, dir_links, dir_faces, dir_embs
from face_recognize import is_same, batch_size, image_size
import numpy as np
#create a list of all embeddings and ids
import pickle
from facenet_embedding import im_to_embedding, dist, ClassifierNN

embs = []
ids = []
photo_ids = []
for name in os.listdir(dir_embs):
    #id_embs = np.load(os.path.join(dir_embs, name))
    data = pickle.load(open(os.path.join(dir_embs, name), 'rb'))
    id_embs = data['embs']
    id_photos = data['photo_ids']
    id = os.path.splitext(name)[0]
    embs.extend(id_embs)
    ids.extend([id]*len(id_embs))
    photo_ids.extend(id_photos)

embs = np.array(embs)
numerics = [i for i in range(len(ids))]

#here ids became numbers from 0 to N. To get name use ids_to_names[i]
ids_to_names = dict(zip(numerics, ids))
ids = list(ids_to_names.keys())

ids = np.array(ids, dtype=np.int)
photo_ids = np.array(photo_ids)

cl = ClassifierNN(embs, (ids, photo_ids))


def get_classifier():
    return cl