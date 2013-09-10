import satelliteImage
import sys

#############################
## Getiing satellite image  ##
#############################
# haneda air port
simg = satelliteImage.TsatelliteImage( 35.541001, 139.750408, 35.553292, 139.767059)
ret = simg.getImages()
if (ret): 
  sys.stderr.write("Retreiving image from server was failure !!\n")
  exit()
simg.makeImage('haneda.jpg')

# musashi kosugi
simg = satelliteImage.TsatelliteImage( 35.581101, 139.657319, 35.573484,139.668739)
ret = simg.getImages()
if (ret): 
  sys.stderr.write("Retreiving image from server was failure !!\n")
  exit()
simg.makeImage('musako.jpg')

#############################
## Getting map             ##
#############################
simg.setDataID("DJBMM")
simg.setZoomID(17)
simg.setImgFileExt('.png')
ret = simg.getImages()
if (ret): 
  sys.stderr.write("Retreiving image from server was failure !!\n")
  exit()
simg.makeImage('musakoMap.png')

#################################
## Getting elevation countour  ##
#################################
simg = satelliteImage.TsatelliteImage( 34.032296, 129.243585, 30.862276, 133.264581)
simg.setDataID("RELIEF")
simg.setZoomID(7)
simg.setImgFileExt('.png')
ret = simg.getImages()
if (ret): 
  sys.stderr.write("Retreiving image from server was failure !!\n")
  exit()
simg.makeImage('kyusyu.png')
