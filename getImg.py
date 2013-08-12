import requests
import webMercator

def getImgInPoint(lat, lng, outImgFile):
  baseURL = "http://cyberjapandata.gsi.go.jp/sqras/all/"
  dataID = "DJBMO"
  zoomID = 16
  eachDirectNum = 2**zoomID

  x,y = webMercator.latlng2xyOnMap(lat,lng);
  xTileNum , yTileNum = webMercator.getTileNum(zoomID, x, y)
  
  tailURL = procTailURL(xTileNum, yTileNum)
  # request URL
  URL = baseURL + dataID + "/" + "latest/" + str(zoomID) + "/" + tailURL
  print "Request URL:", URL

  # request for api
  res = requests.get(URL)
  if (res.status_code != 200):
    return res.status_code
  with open(outImgFile, "wb") as outFileObj:
    outFileObj.write(res.content)
  print "get image successfully"
  return

def procTailURL(xTileNum, yTileNum):
  xTileNum = '%07d' % xTileNum
  yTileNum = '%07d' % yTileNum
  tileID = xTileNum + yTileNum

  idx = 0
  idxDir = ""
  while(idx<6):
    idxDir += xTileNum[idx] + yTileNum[idx] + "/"
    idx = idx + 1
  fileExt = ".jpg"
  tailURL = idxDir + tileID + fileExt
  return tailURL
