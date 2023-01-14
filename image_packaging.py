# -*- coding: utf-8 -*-
"""
Created on Mon Jan  2 14:02:15 2023

@author: Vardhan Harsh (Vanderbilt University)
"""
import cv2
import glob,os

print(os.getcwd())

def chunkify(lst,n):
    return [lst[i*5:(i+1)*5] for i in range(n)]



images = []; name=[]
print(images)
for file in glob.glob('*.png'):
   im= cv2.imread(file)
   
   print(im.shape)
   im=im[250:500, 400:900]
   #cv2.imshow('image',im)
   #cv2.waitKey(0)
   images.append(im)
   name.append(file)


print('Len of images:',len(images),'name is:',name)

split_name=chunkify(name, 5)
split_images=chunkify(images, 5)
print(len(split_name))
im_name=['v10','v1','v25','v5','v75']
for k in range(len(split_images)):
   myorder = [0,2,4,1,3]
   split_name[k] = [split_name[k][i] for i in myorder]
   split_images[k] = [split_images[k][i] for i in myorder]
   im_name[k]=cv2.hconcat(split_images[k]) 
   cv2.imshow('image',im_name[k])
   cv2.waitKey(0)
print(split_name)
print(len(split_images))
final_img=cv2.vconcat([im_name[0],im_name[4],im_name[3],im_name[2],im_name[1]])
cv2.imshow('image',final_img)
cv2.waitKey(0)
cv2.imwrite('sim_out.png', final_img)
   