import numpy as np


basedir = "/media/a/vk"
dir_photos = basedir + "/photos"
dir_links = basedir + "/links"
dir_faces = basedir + "/faces"
dir_embs = basedir + '/embs'

#create a list of all embeddings and ids
import pickle
import os

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


from scipy import misc
import sys
curdir = os.path.dirname(__file__)
ml_dir = os.path.join(curdir, 'ml')
sys.path.append(ml_dir)
from facenet_embedding import im_to_embedding, ClassifierNN


cl = ClassifierNN(embs, (ids, photo_ids))


def classify(im, k=20):
    """"""
    if type(im) is str:
        ims = misc.imread(im)
    emb = im_to_embedding(ims)
    predicted_ids, predicted_photo_ids, dists = cl.classifyK(emb, k)
    return predicted_ids, predicted_photo_ids, dists

