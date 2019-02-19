Manual:
run setup_dependencies.sh only at first time. It will download facenet repo and weights for it.
run run.sh to start webserver.

# vkfaces_web
TODO korabelnikov:
1. продетектировать все лица в папке с фотками. Done
2. распознать все лица. Записать (пока в txt). Done
3. сохранить все эмбюдинги в удобный для поиска файл. Done
4. для обработки веба детектировать лицо, распознать, найти самое похожее. Done, но берется самое большое лицо, если их
несколько. Можно это также потом дообработать с GUI
5. выкинуть чужие лица из аккаунтов пользователей

ML:
face detection via mtcnn in https://github.com/davidsandberg/facenet/tree/master/src/align
face recognition/embedding https://github.com/davidsandberg/facenet
face matching: NearestNeighbor

Application server:
-Flask

Interface
функция classify(im, k) принимает фотку или путь к ней  и к - количество запрашиваемых ответов. Возвращает айдишники в
 виде интов, строчки-айдишники фоток и расстояние поиска (число большее нуля, чем меньше - тем лучше).