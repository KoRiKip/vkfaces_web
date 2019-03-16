from config import basedir, dir_photos, dir_links, dir_faces, dir_embs

import matplotlib.pyplot as plt
from grabVK5 import grab5 as grab
import os

'''
def prepare_ids():
    import json
    from pprint import pprint

    ids = []

    for i in ['2015', '2016', '2017', '2018', '2019', '2020', ]:
        with open('samun_users%s.json' % i) as f:
            data = json.load(f)
        data = data['response']['items']
        ids.extend([d['id'] for d in data])
    ids = list(set(ids))
    print(ids.__len__(), ' ids are there')
    return ids
'''

ids = range(100000000, 999999999)
if not os.path.exists(dir_photos):
    os.makedirs(dir_photos)

if not os.path.exists(dir_links):
    os.makedirs(dir_links)

log_suc = open('/media/a/vk/download_success_id.txt', 'a')
log_fail = open('/media/a/vk/download_failed_id.txt', 'a')

for id in ids:
    avas = grab(id)
    if avas is None:
        log_fail.write(str(id) + '\n')
        print('-')
        continue
    log_suc.write(str(id) + '\n')
    print('+')
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