import cv2
from pdf2image import convert_from_path
from fpdf import FPDF
import sys
import os
import glob
import argparse

def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-fp', '--file-path', type=str, default='input.pdf', help='path of the pdf file')
    parser.add_argument('-if', '--image-format', type=str, default='jpg', help='image format for converting the pdf file')
    parser.add_argument('-pp', '--poppler-path', type=str, default='None', help='path of poppler')
    args = parser.parse_args()

    return args

def mkdir(path):
    if os.path.exists(path):
        import shutil
        shutil.rmtree(path, ignore_errors = True)
    os.makedirs(path)

def PDF2IMG(args):
    image_format = args.image_format
    if image_format not in ['jpg', 'png']:
        print('Invalid image format')
        return None
    if args.poppler_path == 'None':
        print('Please enter the path to poppler')
        return None
    
    print('Converting pdf to image')
    img_path = './imgs'
    mkdir(img_path)
    pages = convert_from_path(args.file_path, poppler_path = args.poppler_path)
    for i, page in enumerate(pages):
        img_name = img_path + '/%04d.' % i + image_format
        page.save(img_name, image_format)

def Whitening(args):
    print('Whitening')
    img_path_list = glob.glob("./imgs/*." + args.image_format)
    for path in img_path_list:
        img = cv2.imread(path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, img = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY)
        
        contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contour = contours[0]
        x,y,w,h = cv2.boundingRect(contour)
        crop = img[y:y+h,x:x+w]
        cv2.imwrite(path, crop)

def IMG2PDF(args):
    pdf = FPDF()
    img_path_list = glob.glob("./imgs/*." + args.image_format)
    for path in img_path_list:
        pdf.add_page()
        pdf.image(path, 0, 0, 210, 297)
    pdf.output(args.file_path[:-4] + '_whitened.pdf', "F")

def Run(args):
    #PDF2IMG(args)
    #Whitening(args)
    IMG2PDF(args)

if __name__ == '__main__':
    args = arg_parse()
    Run(args)