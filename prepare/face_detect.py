from config import basedir, dir_photos, dir_links, dir_faces, dir_embs

import numpy as np
import sys
sys.path.append('/media/b/faces/vkfaces_web/ml') #TODO
from detector import get_faces
import os
import shutil

if os.path.exists(dir_faces):
    shutil.rmtree(dir_faces)

import matplotlib.pyplot as plt
from PIL import Image
import os
from tqdm import tqdm

for id in tqdm(os.listdir(dir_photos)):
    id_dir_in = os.path.join(dir_photos, id)
    id_dir_out = os.path.join(dir_faces, id)

    for im_name in os.listdir(id_dir_in):
        im = np.array(Image.open(os.path.join(id_dir_in, im_name)))
        # plt.imshow(im)
        faces = list(get_faces(im))
        if faces.__len__() != 0 and not os.path.exists(id_dir_out):
            os.makedirs(id_dir_out)
        for i, im_face in enumerate(faces):
            # plt.imshow(im_face)
            # plt.show()
            im_face = Image.fromarray(im_face)

            if len(faces) == 1:
                im_face.save(os.path.join(id_dir_out, im_name))
            else:
                # add index to names
                name = os.path.splitext(im_name)
                name = name[0] + '_' + str(i) + name[1]
                print(name, 'has ', len(faces), ' faces')

                im_face.save(os.path.join(id_dir_out, name))
