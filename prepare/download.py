import matplotlib.pyplot as plt
from grabVK5 import grab5 as grab
import os
from PIL import Image
import numpy as np

from mtcnn.mtcnn import MTCNN

# detector = MTCNN()

if not os.path.exists(dir_photos):
    os.makedirs(dir_photos)

if not os.path.exists(dir_links):
    os.makedirs(dir_links)

log_suc = open('/media/a/vk/download_success_id.txt', 'w')
log_fail = open('/media/a/vk/download_failed_id.txt', 'w')

for id in ids:
    avas = grab(id)
    if avas is None:
        log_fail.write(str(id) + '\n')
        continue
    log_suc.write(str(id) + '\n')
    try:
        subdir = os.path.join(dir_photos, str(id))
        os.makedirs(subdir)
    except:
        pass
    with open(dir_links + str(id) + '.txt', 'w') as f:
        for url, im in avas:
            f.write(url + '\n')
            name = url[url.rfind('/') + 1:]
            im.save(os.path.join(subdir, name))

            """
            faces = detector.detect_faces(np.array(im))
            if faces:
                f.write(url + '\n')
                for face in faces:
                    name = url[url.rfind('/') + 1:]
                    print(os.path.join(subdir, name))
                    bb = face['box']
                    im.crop(bb).save(os.path.join(subdir, name))
            """