from reportlab.platypus import SimpleDocTemplate, Image
from PIL import Image as Img
import qrcode
import glob
import sys
import os

data = 'https://github.com/'

img = qrcode.make(data)
img.save('Test.png')

im = Img.open('./Test.png')
x, y = im.size
image = Image(im, width=x, height=y)

canvas = SimpleDocTemplate("test.pdf", pagesize=(x*2, y*2), title="Pase de Abordar")
canvas.build([image])