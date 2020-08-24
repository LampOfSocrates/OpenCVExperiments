from PIL import Image
import requests
from io import BytesIO
import numpy as np
import cv2

# get the data
url = 'https://i0.wp.com/post.medicalnewstoday.com/wp-content/uploads/sites/3/2020/03/GettyImages-1092658864_hero-1024x575.jpg'
url = 'https://images-na.ssl-images-amazon.com/images/I/61NVn0duI3L._AC_SL1200_.jpg'

#get the data into pil
res = requests.get(url)
pil = Image.open(BytesIO(res.content))
pil.show()
#convert from pil to np in 2 ways
img1 = np.array(pil)
img2 = cv2.cvtColor(np.array(pil), cv2.COLOR_RGB2BGR)
img3 = cv2.cvtColor(np.array(pil), cv2.COLOR_BGR2RGB)
edges1 = cv2.Canny(img1, threshold1=50, threshold2=150, apertureSize=3, L2gradient=True)
edges2 = cv2.Canny(img1, threshold1=100, threshold2=200, apertureSize=3, L2gradient=True)
edges3 = cv2.Canny(img1, threshold1=200, threshold2=300, apertureSize=3, L2gradient=True)


edges1 = cv2.cvtColor(edges1, cv2.COLOR_GRAY2RGB)
edges2 = cv2.cvtColor(edges2, cv2.COLOR_GRAY2RGB)
edges3 = cv2.cvtColor(edges3, cv2.COLOR_GRAY2RGB)

print(edges1.shape)
print(img1.shape)
#img_all = [ img1, img2, img3, edges]

def vconcat_resize_min(im_list, scale=0.7, interpolation=cv2.INTER_CUBIC):
    w_min = min(int(im.shape[1]*scale) for im in im_list)
    im_list_resize = [cv2.resize(im, (w_min, int(im.shape[0] * w_min / im.shape[1])), interpolation=interpolation)
                      for im in im_list]
    return cv2.vconcat(im_list_resize)

def hconcat_resize_min(im_list, scale=0.7, interpolation=cv2.INTER_CUBIC):
    h_min = min(int(im.shape[0]*scale ) for im in im_list)
    im_list_resize = [cv2.resize(im, (int(im.shape[1] * h_min / im.shape[0]), h_min), interpolation=interpolation)
                      for im in im_list]
    return cv2.hconcat(im_list_resize)

def concat_tile_resize(im_list_2d, scale=0.7 ,interpolation=cv2.INTER_CUBIC):
    im_list_v = [hconcat_resize_min(im_list_h, interpolation=cv2.INTER_CUBIC) for im_list_h in im_list_2d]
    return vconcat_resize_min(im_list_v, interpolation=cv2.INTER_CUBIC)

def concat_tile(im_list_2d):
    return cv2.vconcat([cv2.hconcat(im_list_h) for im_list_h in im_list_2d])

#im1_s = cv2.resize(im1, dsize=(0, 0), fx=0.5, fy=0.5)
#im_tile = concat_tile([[img1, img2, ],
#                       [img2, img3,],
#                       ])
                       
img_all_resized = concat_tile_resize([[img1, edges1],
                                     [edges2, edges3, ],
                                     ])
             
                         
#play with ur np
#concat the input and output and convert back to
#img_all_resized = [ cv2.resize(im, ( 300, 200), interpolation=cv2.INTER_CUBIC)  for im in img_all]
#img_all = cv2.vconcat(img_all_resized)
pil_all = Image.fromarray(img_all_resized)
pil_all.show()    
