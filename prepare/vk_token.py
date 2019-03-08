import json
from pprint import pprint

import sys
sys.path.append('/home/administrator/repo/vk_photos')
from photos3 import auth as vk_auth, check_token, request

#vk_auth('nesoriti@ya.ru', '.') doesn't work. just use flow authorization and copy access_token
token = '92802345f428f0b09aeffebb2b7fac2bf745e6576a4b421d8f32d9809ca9a07e9ed78b90fb36809737fc3'
f = open('repo/vk_photos/token', 'w')
f.write(token)
f.close()
#check_token(token)
params = {'access_token': token, 'v': 5.92}
check = request('users.get', params, is_one=True)
print(check)


ava = request('users.get', {**params, **{'user_ids':'210700286', 'fields': 'photo_400_orig'}}, is_one=True)
print(ava['photo_400_orig'])

req = request('photos.getAll', {**params, **{'owner_id':'210700286',
                                         'offset': '0',
                                         'count': 200}},
              is_one=False)
print(req)
