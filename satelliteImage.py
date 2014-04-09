import os
import tempfile
import requests
import webMercator
import shutil
from PIL import Image

class TsatelliteImage:

  def __init__(self, lat0, lng0, lat1, lng1):
    self.setDataID('DJBMO')
    self.pid = os.getpid()
    self.setImgFileExt('.jpg')

    # API server info.
    self.baseURL = "http://cyberjapandata.gsi.go.jp/sqras/all/"

    # change to P0 (north west) and P1(south east)
    if( lat0 <= lat1 ):
      tmp = lat1
      lat1 = lat0
      lat0 = tmp
    if(lng0 >= lng1):
      tmp = lng1
      lng1 = lng0
      lng0 = tmp

    self.lat0 = lat0
    self.lng0 = lng0
    self.lat1 = lat1
    self.lng1 = lng1

    self.width = 0
    self.height = 0
    self.outFile = ""

    self.setZoomID(16)

  def __del__(self):
    self.cleanupTmpImgFile();

  def setZoomID(self, zoomID): 
    self.zoomID = zoomID

    self.webMrtr = webMercator.TwebMercator(self.zoomID)
    self.x0, self.y0 = self.webMrtr.latlng2xyOnMap(self.lat0, self.lng0);
    self.x1, self.y1 = self.webMrtr.latlng2xyOnMap(self.lat1, self.lng1);
    self.px0, self.py0 = self.webMrtr.xy2pxpyInTile(self.x0, self.y0)
    self.px1, self.py1 = self.webMrtr.xy2pxpyInTile(self.x1, self.y1)
    self.xTileNum0 , self.yTileNum0 = self.webMrtr.getTileNum(self.x0, self.y0)
    self.xTileNum1 , self.yTileNum1 = self.webMrtr.getTileNum(self.x1, self.y1)
    self.numXTile = self.xTileNum1 - self.xTileNum0 + 1
    self.numYTile = self.yTileNum1 - self.yTileNum0 + 1
    return 0

  def getZoomID(self): return self.zoomID

  def setDataID(self, dataID): self.dataID = dataID
  def getDataID(self): return self.dataID


  def setImgFileExt(self, argImgFileExt): self.imgFileExt = argImgFileExt
  def getImgFileExt(self): return self.imgFileExt

  def setOutFile(self, agOutFile): self.outFile = agOutFile
  def getOutFile(self): return self.outFile

  def getimgFilePath(self, xTileNum, yTileNum):
    tmpDir = tempfile.gettempdir()
    outImgFile = tmpDir + os.sep + str(self.pid) + "_" + str('%07d' % xTileNum) + str('%07d' % yTileNum) + self.imgFileExt
    # for debug
    #outImgFile = str('%07d' % xTileNum) + str('%07d' % yTileNum) + self.imgFileExt
    return outImgFile
  
  def getImages(self):
  
    for xTileNum in range(self.xTileNum0, self.xTileNum1 + 1):
      for yTileNum in range(self.yTileNum0, self.yTileNum1 + 1):
        tailURL = self.mkURL(xTileNum, yTileNum)
        outImgFile = self.getimgFilePath(xTileNum, yTileNum)
        # request URL
        URL = self.baseURL + self.dataID + "/" + "latest/" + str(self.zoomID) + "/" + tailURL
        print "Requesting image to ", URL
        # request for api
        res = requests.get(URL)
        if (res.status_code != 200):
          return res.status_code
        with open(outImgFile, "wb") as outFileObj:
          outFileObj.write(res.content)
    print "Getting image successfully"
    return 0
  
  def mkURL(self, xTileNum, yTileNum):
    xTileNum = '%07d' % xTileNum
    yTileNum = '%07d' % yTileNum
    tileID = xTileNum + yTileNum
  
    idx = 0
    idxDir = ""
    while(idx<6):
      idxDir += xTileNum[idx] + yTileNum[idx] + "/"
      idx = idx + 1
    tailURL = idxDir + tileID + self.imgFileExt
    return tailURL

  def makeImage(self, agOutFile):
    self.setOutFile(agOutFile)
    if( (self.numXTile == 0) and (self.numYTile == 0 )):
      pass
    elif( self.numXTile == 0 ):
      pass
    elif( self.numYTile == 0 ):
      pass
    else:
      self.calcImageSize()
      self.makeBoundaryImage() 
      self.combineImage()
    return 0

  def calcImageSize(self):
    self.width  = ((self.webMrtr.pxTileWidth - self.px0) + (self.px1 + 1)+ self.webMrtr.pxTileWidth * (self.numXTile - 2)) - 1
    self.height = ((self.webMrtr.pxTileWidth - self.py0) + (self.py1 + 1)+ self.webMrtr.pxTileWidth * (self.numYTile - 2)) - 1

    return 0

  def makeBoundaryImage(self):
    tmpImgFile = 'tmp_' + str(self.pid) + self.imgFileExt
    ###################################
    ## make nourth-west corner image ##
    ###################################
    imgFile = self.getimgFilePath(self.xTileNum0, self.yTileNum0)
    # cut out part of tile image
    imgObj = Image.open(imgFile)
    if (self.numXTile == 1):
      pxEstBoundary = self.px1
    else:
      pxEstBoundary = self.webMrtr.pxTileWidth
    if (self.numYTile == 1):
      pxSouthBoundary = self.py1
    else:
      pxSouthBoundary = self.webMrtr.pxTileWidth
    imgPrtObj = imgObj.crop((self.px0, self.py0, pxEstBoundary, pxSouthBoundary))
    imgPrtObj.save(tmpImgFile, 'JPEG')
    shutil.move(tmpImgFile, imgFile)
    if (self.numXTile>2):
      ## other boundary image
      for curXNum in range( self.xTileNum0 + 1, self.xTileNum1):
        imgFile = self.getimgFilePath(curXNum, self.yTileNum0)
        imgObj =Image.open(imgFile)
        imgPrtObj = imgObj.crop((0, self.py0, self.webMrtr.pxTileWidth, self.webMrtr.pxTileWidth))
        imgPrtObj.save(tmpImgFile, 'JPEG')
        shutil.move(tmpImgFile, imgFile)
    if (self.numYTile>2):
      for curYNum in range( self.yTileNum0 + 1, self.yTileNum1):
        imgFile = self.getimgFilePath(self.xTileNum0, curYNum)
        imgObj =Image.open(imgFile)
        imgPrtObj = imgObj.crop((self.px0 , 0, self.webMrtr.pxTileWidth, self.webMrtr.pxTileWidth))
        imgPrtObj.save(tmpImgFile, 'JPEG')
        shutil.move(tmpImgFile, imgFile)

    if(self.numXTile==1 and self.numYTile==1): return 0

    ###################################
    ## make south-east corner        ##
    ###################################
    imgFile = self.getimgFilePath(self.xTileNum1, self.yTileNum1)
    # cut out part of tile image
    imgObj = Image.open(imgFile)
    if (self.numXTile == 1):
      pxWstBoundary = self.px0
    else:
      pxWstBoundary = 0
    if (self.numYTile == 1):
      pxNourthBoundary = self.py0
    else:
      pxNourthBoundary = 0
    imgPrtObj = imgObj.crop((pxWstBoundary, pxNourthBoundary, self.px1, self.py1))
    imgPrtObj.save(tmpImgFile, 'JPEG')
    shutil.move(tmpImgFile, imgFile)
    # make other boundary
    if (self.numXTile>2):
      for curXNum in range( self.xTileNum1 - 1, self.xTileNum0 , -1):
        imgFile = self.getimgFilePath(curXNum, self.yTileNum1)
        imgObj =Image.open(imgFile)
        imgPrtObj = imgObj.crop((0, 0, self.webMrtr.pxTileWidth, self.py1))
        imgPrtObj.save(tmpImgFile, 'JPEG')
        shutil.move(tmpImgFile, imgFile)
    if (self.numYTile>2):
      for curYNum in range( self.yTileNum1 - 1, self.yTileNum0, -1):
        imgFile = self.getimgFilePath(self.xTileNum1, curYNum)
        imgObj =Image.open(imgFile)
        imgPrtObj = imgObj.crop((0, 0, self.px1, self.webMrtr.pxTileWidth))
        imgPrtObj.save(tmpImgFile, 'JPEG')
        shutil.move(tmpImgFile, imgFile)
    ###################################
    ## processing other cotner      ##
    ###################################
    if ((self.numXTile>1 or self.numYTile>1) and (self.numXTile*self.numYTile>3)):
      # north-east
      imgFile = self.getimgFilePath(self.xTileNum1, self.yTileNum0)
      imgObj =Image.open(imgFile)
      imgPrtObj = imgObj.crop((0, self.py0, self.px1, self.webMrtr.pxTileWidth))
      imgPrtObj.save(tmpImgFile, 'JPEG')
      shutil.move(tmpImgFile, imgFile)
      # south-west
      imgFile = self.getimgFilePath(self.xTileNum0, self.yTileNum1)
      imgObj =Image.open(imgFile)
      imgPrtObj = imgObj.crop(( self.px0, 0, self.webMrtr.pxTileWidth, self.py1))
      imgPrtObj.save(tmpImgFile, 'JPEG')
      shutil.move(tmpImgFile, imgFile)
    return 0

  def combineImage(self):
    outFile = self.getOutFile()
    allImg = Image.new('RGB', (self.width, self.height))
    imgPosY = 0
    for curYNum in range(self.yTileNum0, self.yTileNum1+1):
      imgPosX = 0
      for curXNum in range(self.xTileNum0, self.xTileNum1+1):
        imgFile = self.getimgFilePath(curXNum, curYNum)
        imgObj = Image.open(imgFile)
        allImg.paste(imgObj, (imgPosX, imgPosY))
        prtWidth , prtHeight = imgObj.size
        imgPosX += prtWidth
      imgPosY += prtHeight
    allImg.save(outFile, 'JPEG')
    return 0

  def cleanupTmpImgFile(self):
    for xTileNum in range(self.xTileNum0, self.xTileNum1 + 1):
      for yTileNum in range(self.yTileNum0, self.yTileNum1 + 1):
        tailURL = self.mkURL(xTileNum, yTileNum)
        outImgFile = self.getimgFilePath(xTileNum, yTileNum)
        if(os.path.exists(outImgFile)): os.remove(outImgFile)
    return 0

# for command run secction
if (__name__ == '__main__'):
  import argparse
  import sys
  import satelliteImage

  ##################################
  ## parse command line arguments ##
  ##################################
  parser = argparse.ArgumentParser(description='Get satelite image from cyber-japan server.')
  parser.add_argument("-n", "--NW", dest="nwArg", required=True, help="Nourth-West point. ex. 35.23,135.456")
  parser.add_argument("-s", "--SE", dest="seArg", required=True, help="South-East point. ex. 35.24,135.467")
  parser.add_argument("-o", "--out-file", dest="outFile", required=True, help="Output file name")
  args = parser.parse_args()
  lat0 , lng0 =  args.nwArg.split(',')
  lat1 , lng1 =  args.seArg.split(',')
  lat0 = float(lat0)
  lng0 = float(lng0)
  lat1 = float(lat1)
  lng1 = float(lng1)
  outFile = args.outFile

  ##################################
  ## Getting image & make image   ##
  ##################################
  simg = satelliteImage.TsatelliteImage( lat0, lng0, lat1, lng1)
  ret = simg.getImages()
  if (ret): 
    sys.stderr.write("Retreiving image from server was failure !!\n")
    exit()
  simg.makeImage(outFile)
