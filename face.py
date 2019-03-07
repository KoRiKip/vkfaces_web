import numpy as np


basedir = "/media/a/vk"
dir_photos = basedir + "/photos"
dir_links = basedir + "/links"
dir_faces = basedir + "/faces"
dir_embs = basedir + '/embs'

#create a list of all embeddings and ids
import pickle
import os

print('Read all embedddings')
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
ids = np.array(ids, dtype=np.int)
photo_ids = np.array(photo_ids)
print('Load detector, facenet and classifier')

from scipy import misc
import sys
curdir = os.path.dirname(__file__)
ml_dir = os.path.join(curdir, 'ml')
sys.path.append(ml_dir)
from facenet_embedding import im_to_embedding, ClassifierNN
from detector import get_faces


cl = ClassifierNN(embs, (ids, photo_ids))
print('done')

def classify(im, k=20):
    """"""
    if type(im) is str:
        im = misc.imread(im)
    face = get_faces(im)
    if len(face) == 0:
        raise RuntimeError('No faces have been detected')
    face = face[0]
    emb = im_to_embedding(face)
    predicted_ids, predicted_photo_ids, dists = cl.classifyK(emb, k)
    return predicted_ids, predicted_photo_ids, dists

