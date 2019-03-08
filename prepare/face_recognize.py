from config import basedir, dir_photos, dir_links, dir_faces, dir_embs, image_size, batch_size

import os
from tqdm import tqdm
import numpy as np
from scipy import misc
import shutil
import pickle
import sys

sys.path.append('/media/b/faces/vkfaces_web/ml')
from facenet_embedding import im_to_embedding, dist, ClassifierNN

def is_same(dist):
    return dist < 1.15  # pred


if __name__ == 'main': #todo?
    if os.path.exists(dir_embs):
        shutil.rmtree(dir_embs)
    os.makedirs(dir_embs)


    def batches(l, n):
        """Yield successive n-sized chunks from l."""
        for i in range(0, len(l), n):
            yield l[i:i + n]


    all_embs = {}
    for id in tqdm(os.listdir(dir_faces)):
        id_dir_in = os.path.join(dir_faces, id)

        embs = []
        photo_ids = []
        # batched version
        batches_of_impathes = batches(os.listdir(id_dir_in), batch_size)
        for impathes in batches_of_impathes:
            photo_ids.extend(impathes)
            impathes = [os.path.join(id_dir_in, im_name) for im_name in impathes]
            ims = [misc.imread(path) for path in impathes]
            emb = im_to_embedding(ims, image_size)
            embs.extend(emb)
        all_embs[id] = embs  # add to global storage
        embs = np.stack(embs)
        photo_ids = np.stack(photo_ids)
        # np.save(os.path.join(dir_embs, id+'.npy'), embs)
        pickle.dump({'embs': embs, 'photo_ids': photo_ids}, open(os.path.join(dir_embs, id + '.pickle'), 'wb'))