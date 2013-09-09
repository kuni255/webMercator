import sateliteImage
import sys

# haneda
#simg = sateliteImage.TsateliteImage( 35.541001, 139.750408, 35.553292, 139.767059)
# musashi kosugi
simg = sateliteImage.TsateliteImage( 35.581101, 139.657319, 35.573484,139.668739)
# musashi kosugi 1 tile x 2 tile
#simg = sateliteImage.TsateliteImage( 35.581101, 139.657319, 35.576144, 139.657500)
# musako 2 tile x 1tile
#simg = sateliteImage.TsateliteImage( 35.581101, 139.657319, 35.579948, 139.658657)
# musako 1 tile x 1tile
#simg = sateliteImage.TsateliteImage( 35.581101, 139.657319, 35.579948, 139.657938)
ret = simg.getImages()
if (ret): 
  sys.stderr.write("Retreiving image from server was failure !!\n")
  exit()
simg.makeImage('test2.jpg')
