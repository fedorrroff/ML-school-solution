from PIL import Image
import os, os.path
import numpy as np
import argparse

def get_path():
    parser = argparse.ArgumentParser(description='First test task on images similarity.')
    parser.add_argument(
        '--path',
        dest='PATH',
        type=str,
        help='folder with images',
        required=True
    )
    my_namespace = parser.parse_args()
    path = my_namespace.PATH
    return path

def get_files():
    imgs = []
    path = get_path()
    valid_images = [".jpg", ".gif", ".png", ".tga"]
    for f in os.listdir(path):
        ext = os.path.splitext(f)[1]
        if ext.lower() not in valid_images:
            continue
        imgs.append(Image.open(os.path.join(path, f)))
    return imgs

def get_difference(imgs1, imgs2):
    r = np.asarray(imgs1.convert("RGB", (1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0)))
    g = np.asarray(imgs1.convert("RGB", (0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0)))
    b = np.asarray(imgs1.convert("RGB", (0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0)))
    hr, h_bins = np.histogram(r, bins=256, density=True)
    hg, h_bins = np.histogram(g, bins=256, density=True)
    hb, h_bins = np.histogram(b, bins=256, density=True)
    hist1 = np.array([hr, hg, hb]).ravel()

    r = np.asarray(imgs2.convert("RGB", (1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0)))
    g = np.asarray(imgs2.convert("RGB", (0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0)))
    b = np.asarray(imgs2.convert("RGB", (0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0)))
    hr, h_bins = np.histogram(r, bins=256, density=True)
    hg, h_bins = np.histogram(g, bins=256, density=True)
    hb, h_bins = np.histogram(b, bins=256, density=True)
    hist2 = np.array([hr, hg, hb]).ravel()

    diff = hist1 - hist2
    identic = np.sqrt(np.dot(diff, diff))
    return identic

def is_identic_histogram():
    imgs = get_files()
    len_imgs = len(imgs) - 1
    for i in range(len_imgs, 1, -1):
        imgs1 = imgs[i]
        for j in range(i - 1, 0, -1):
            imgs2 = imgs[j]
            if imgs1.size != imgs2.size or imgs1.getbands() != imgs1.getbands():
                continue

            identic = get_difference(imgs1, imgs2)
            if not identic:
                print('Img{0} is identic to img{1}'.format(imgs2.filename, imgs1.filename))
            elif identic < 0.095:
                print('Img{0} is similar to img{1}'.format(imgs2.filename, imgs1.filename))

if __name__ == '__main__':
    is_identic_histogram()




