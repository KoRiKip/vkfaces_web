from PIL import Image
from io import BytesIO
import requests
from IPython.core.display import display, HTML

_cookieHeader = ""
Vk = "http://vk.com"

def grab5(id):
    # проблема в том, что получаются только первые 24 фотографии ?offset=24 не помог ?
    # получение страницы со всеми аватарками
    reqGet = requests.get(Vk + "/album" + str(id) + "_0")
    print(Vk + "/album" + str(id) + "_0")
    #reqGet.Headers.Add(HttpRequestHeader.Cookie, _cookieHeader);
    s = reqGet.text
    
    #display(HTML(s))#todo debug
    
    if (s == ''):
        print('cant load ' + str(id))
        return
    #pat1 = '<div id="photos_container_photos" class="photos_container" '
    pat1 = '<div class="photos_page thumbs_list">'
    try:
        ind1 = s.index(pat1)
    except:
        print('cant find ', pat1)
        return
    pat = '/photo'+str(id)
    moved_index = ind1

    while True:
        try:
            ind1 = s.index(pat, moved_index)
            ind2 = s.index('"', ind1)
        except:
            return        
        url1 = s[ind1:ind2]
        moved_index = ind2

        # preload images
        reqGet = requests.get(Vk + url1);
        print(Vk + url1)

        #reqGet.Headers.Add(HttpRequestHeader.Cookie, _cookieHeader);
        s1 = reqGet.text
        
        #display(HTML(s1))
        #print(s1)
        # разборка новой страницы
        #<img src="https://pp.userapi.com/Nz1veObO844LIBqdTWvk5gl7ET7jmuit8nSRxg/Esu14CSph-M.jpg
        pat1 = '<div class="pv_photo_wrap"><img src="'
        pat2 = '.jpg'

        ind1 = s1.index(pat1)
        ind2 = s1.index(pat2, ind1)
        imgUrl = s1[ind1 + len(pat1): ind2 + len(pat2)]
        #print(imgUrl)

        reqGet = requests.get(imgUrl)

        #reqGet.Headers.Add(HttpRequestHeader.Cookie, _cookieHeader);
        
        image = Image.open(BytesIO(reqGet.content))
        
        yield imgUrl, image
