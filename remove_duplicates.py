from imaging_interview import compare_frames_change_detection, preprocess_image_change_detection
import cv2, os, glob, shutil
from tqdm.auto import tqdm
from time import sleep
import numpy as np
from PIL import Image
from pathlib import Path, PureWindowsPath, PurePosixPath

from .helper import *

image_names = list()
images = list()
cameras = list()
cameras_and_names = dict()

dir = 'D:\Kopernikus\SimilarLookingImages\dataset-candidates-ml\dataset'

assert Path(dir).exists(), 'Invalid path!!'
dir = Path(dir)

assert Path.is_dir(dir), "directory not found!!"

results_dir = Path(PurePosixPath(dir).joinpath('results'))

if Path(results_dir).exists():
    delete_folder(results_dir)

Path.mkdir(results_dir)
    

valid_images_ext = [".jpg",".png",".jpeg"]

for file_name in Path.iterdir(dir):
    if PurePosixPath(file_name).suffixes:
        if PurePosixPath(file_name).suffixes[0] in valid_images_ext:
            image_names.append(file_name)
            if PureWindowsPath(file_name).name[:3][:3] not in cameras:
                cameras.append(PureWindowsPath(file_name).name[:3][:3]) 

            if PureWindowsPath(file_name).name[:3][:3] not in cameras_and_names.keys():
                cameras_and_names.update({PureWindowsPath(file_name).name[:3][:3]: [file_name]})
            else:
                cameras_and_names[PureWindowsPath(file_name).name[:3][:3]].append(file_name)
    

assert len(cameras) == len(cameras_and_names)



for cam, files in tqdm(cameras_and_names.items(), desc= 'Camera index', ncols=100):
    frame_score = {}
    for idx, next_frame_name in enumerate(tqdm(files, desc= 'Image frame', ncols= 100, position=1, leave=False)):
        try:
            if not cam in PureWindowsPath(next_frame_name).name:
                continue
            
            next_frame= cv2.imread(str(next_frame_name))
            next_frame= preprocess_image_change_detection(next_frame)

            if idx == 0:
                shutil.copy(str(next_frame_name), str(results_dir))
                prev_frame_name = next_frame_name
                prev_frame= next_frame.copy()
                continue

            score, res_cnts, thresh = compare_frames_change_detection(prev_frame, next_frame, 5000)

            prev_frame_name = next_frame_name
            prev_frame = next_frame.copy()
            frame_score.update({prev_frame_name: score})
        
        except:
            pass
            
    remove_images(frame_score)
        

# def compare_frames(prev_frame, next_frame):
#     next_frame= cv2.imread(str(next_frame))
#     prev_frame= cv2.imread(str(prev_frame))

#     next_frame= preprocess_image_change_detection(resize(next_frame))
#     prev_frame= preprocess_image_change_detection(resize(prev_frame))

#     return compare_frames_change_detection(prev_frame, next_frame, 5000)


# for cam in cameras:
#     frame_score = {}
#     for idx, next_frame in enumerate(image_names):
#         if not cam in PureWindowsPath(next_frame).name:
#             continue

#         if idx == 0:
#             prev_frame = next_frame
#             continue
        
#         temp_frame= next_frame
        
#         next_frame= cv2.imread(str(next_frame))
#         prev_frame= cv2.imread(str(prev_frame))

#         next_frame= preprocess_image_change_detection(resize(next_frame))
#         prev_frame= preprocess_image_change_detection(resize(prev_frame))

#         score, res_cnts, thresh = compare_frames_change_detection(prev_frame, next_frame, 1000)

#         prev_frame = temp_frame
#         frame_score.update({prev_frame: score})
    
#     sorted(frame_score.items(), key=lambda kv:(kv[1], kv[0]))
#     # print(frame_score)
#     print(idx)
#     for (k,v) in frame_score.items():
#          if v!=0:
#             shutil.copy(str(k), str(results_dir))








# for idx, next_frame in enumerate(image_names):
#     if idx == 0:
#         prev_frame = next_frame
#         continue
    
#     temp_frame= next_frame
    
#     next_frame= cv2.imread(str(next_frame))
#     prev_frame= cv2.imread(str(prev_frame))
    
#     next_frame= preprocess_image_change_detection(next_frame)
#     prev_frame= preprocess_image_change_detection(prev_frame)
    
#     break
    # print(prev_frame)
    # next_frame = preprocess_image_change_detection(cv2.imread(str(next_frame)))
    # prev_frame = preprocess_image_change_detection(cv2.imread(str(prev_frame)))

    # prev_frame = temp_frame

# images = list(map(Image.open, Path(dir).glob('*.png')))
# print(len(images))
# print(len(image_names))

# print('Total number of cameras are {} and they are {}'.format(len(cameras), cameras))

