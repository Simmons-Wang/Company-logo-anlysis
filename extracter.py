import fitz
import time
import re
import os

from tqdm import tqdm

os.chdir(r'C:\Users\Simmons\PycharmProjects\stocklogo')

# checkXO = r"/Type(?= */XObject)"
# checkIM = r"/Subtype(?= */Image)"


for root, dirs, files in os.walk("./output"):
    pass


for file in tqdm(files):
    stk, date = file.split('_')[1], file.split('_')[2].replace('.pdf', '')
    doc = fitz.open(r'./output/{0}'.format(file))
    img_1 = doc.get_page_images(0)
    if not img_1:
        continue
    else:
        try:
            os.mkdir('./img/{}'.format(stk))
        except FileExistsError:
            pass
        pix = fitz.Pixmap(doc, img_1[0][0])
        try:
            if pix.n < 5:
                pix.writePNG(r'./img/{0}/{1}.png'.format(stk, date))
            else:
                pix0 = fitz.Pixmap(fitz.csRGB, pix)
                pix0.writePNG(r'./img/{0}/{1}.png'.format(stk, date))
                pix0 = None
        except ValueError:
            print(stk)


