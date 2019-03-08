import json


ids = []

for i in ['2015', '2016', '2017', '2018', '2019', '2020', ]:
    with open('samun_users%s.json' % i) as f:
        data = json.load(f)
    data = data['response']['items']
    ids.extend([d['id'] for d in data])
ids = list(set(ids))
print(ids.__len__(), ' ids')
