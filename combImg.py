import requests
import Image

url = "http://cyberjapandata.gsi.go.jp/sqras/all/DJBMO/latest/16/00/00/52/85/27/71/00582740025716.jpg"
url2 = "http://cyberjapandata.gsi.go.jp/sqras/all/DJBMO/latest/16/00/00/52/85/27/71/00582750025716.jpg"
res = requests.get(url)
res2 = requests.get(url2)
with open("output.jpg", "wb") as code:
  code.write(res.content)
with open("output2.jpg", "wb") as code2:
  code2.write(res2.content)

img1 = Image.open("output.jpg")
img2 = Image.open("output2.jpg")
newImg = Image.new("RGB", (512,256))
imgWidth = 256
newImg.paste(img1, (0,0))
newImg.paste(img2, (imgWidth,0))
newImg.save("int.jpg")
