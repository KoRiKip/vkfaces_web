import tensorflow as tf
from scipy import misc
import numpy as np
import sys
import os
curdir = os.path.dirname(__file__)
facenet_dir = os.path.join(curdir, 'facenet_repo/src')
sys.path.append(facenet_dir)
import facenet

weights = os.path.join(curdir, 'weights/20180402-114759/20180402-114759.pb')
sess = tf.Session().__enter__()
graph = tf.Graph().as_default().__enter__()
facenet.load_model(weights)

# Get input and output tensors
images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")
batch_size_placeholder = tf.get_default_graph().get_tensor_by_name("batch_size:0")


def facenet_run(images):
    # Run forward pass to calculate embeddings
    feed_dict = {images_placeholder: images,
                 phase_train_placeholder: False,
                 batch_size_placeholder: len(images)}
    emb = sess.run(embeddings, feed_dict=feed_dict)
    return emb


def crop_center(img, cropx, cropy):
    y,x = img.shape[:2]
    startx = x//2-(cropx//2)
    starty = y//2-(cropy//2)    
    return img[starty:starty+cropy,startx:startx+cropx]


def resize_crop(im, image_size):
    minsize = min(im.shape[:2])
    crop = crop_center(im, minsize, minsize)
    resized = misc.imresize(crop, (image_size, image_size))
    return resized


def im_to_embedding(ims):
    ims = [facenet.prewhiten(im) for im in ims]
    ims = [resize_crop(im, image_size)/255 - 0.5 for im in ims]
    ims = np.array(ims)
    if ims.shape.__len__() < 4:
        ims = np.expand_dims(ims, 0)
    return facenet_run(ims)

def dist(em1, em2):
    return facenet.distance(np.expand_dims(em1, 0), np.expand_dims(em2, 0))[0]


# create NN  classifier by cosine or Euclide distance, TODO move it out
class ClassifierNN:
    def __init__(self, X, Ys):
        """X-features : numpy array
        Y - answers"""
        self._X = X
        self._Ys = Ys
        
    def classifyK(self, x, k=1):
        dists = np.array([dist(x, _x) for _x in self._X])
        
        idx = np.argpartition(dists, k)
        idx = idx[:k]
        ids = self._Ys[0]
        photo_ids = self._Ys[1]
        return ids[idx], photo_ids[idx], dists[idx]
