import sys, shutil, cv2
from pathlib import Path, PurePosixPath, PureWindowsPath
from tqdm.auto import tqdm
from helper import *
from imaging_interview import preprocess_image_change_detection, compare_frames_change_detection


def main(in_dir, results_dir, min_cntr_area, sim_thres):
    image_names = list()            # initializing list to hold image_names
    cameras = list()                # initializing list to hold cameras indexes. e.g: ['c10', 'c21', 'c22', 'c23']
    cameras_and_names = dict()      # initializing dictionary to hold camera indexes as keys and corresponding images as keys. e.g: {'c10':[x.png, y.png, ....], 'c20':[p.png, q.png, ...]}

    valid_images_ext = [".jpg",".png",".jpeg"]      # Allowed extensions for image files. Further possible externsions can be added or deleted here


    # iterating through the image directory
    for file_name in Path.iterdir(in_dir):
        if PurePosixPath(file_name).suffixes:
            if PurePosixPath(file_name).suffixes[0] in valid_images_ext:
                image_names.append(file_name)
                if PureWindowsPath(file_name).name[:3][:3] not in cameras:
                    cameras.append(PureWindowsPath(file_name).name[:3][:3]) 

                if PureWindowsPath(file_name).name[:3][:3] not in cameras_and_names.keys():
                    cameras_and_names.update({PureWindowsPath(file_name).name[:3][:3]: [file_name]})
                else:
                    cameras_and_names[PureWindowsPath(file_name).name[:3][:3]].append(file_name)
    

    # just a simple sanity check
    assert len(cameras) == len(cameras_and_names)

    for cam, files in tqdm(cameras_and_names.items(), desc= 'Camera index', ncols=100):
        prev_frames= []
        try:
            for frame_ix, fixed_frame_name in enumerate(tqdm(files, desc= 'Image frame', ncols= 100, position=1, leave=False)):
                fixed_frame= cv2.imread(str(fixed_frame_name))
                fixed_frame= preprocess_image_change_detection(fixed_frame, gaussian_blur_radius_list=[5])
                fixed_frame= resize(fixed_frame) 

                if frame_ix == 0:
                    shutil.copy(str(fixed_frame_name), str(results_dir))
                    prev_frames.append(fixed_frame.copy())
                    continue
                
                scores_this_frame = []
                
                for _, prev_frame in enumerate(tqdm(prev_frames, desc= 'Prev frames', ncols= 100, position=2, leave=False)):

                    score, _, _ = compare_frames_change_detection(prev_frame, fixed_frame, min_cntr_area)
                    scores_this_frame.append(score)

                prev_frames.append(fixed_frame.copy())

                to_copy_images = [float(sc)>float(sim_thres) for sc in scores_this_frame]

                if all(to_copy_images):
                    shutil.copy(str(fixed_frame_name), str(results_dir))
            
        except:
            pass        


if __name__ == "__main__":
    image_dir = sys.argv[1]
    assert Path(image_dir).exists(), 'Invalid path!!'
    image_dir = Path(image_dir)

    assert Path.is_dir(image_dir), "Invalid directory or directory not found!!"

    results_dir = sys.argv[2]
    results_dir = Path(results_dir)

    if Path(results_dir).exists():
        delete_folder(results_dir)

    Path.mkdir(results_dir)

    minimum_contour_area = int(sys.argv[3])
    similarity_score_threshold = int(sys.argv[4])

    main(image_dir, results_dir, minimum_contour_area, similarity_score_threshold)
    print('Done!!! All the similar images are identified in directory- {} and unique images copied to {}'.format(sys.argv[1], sys.argv[2]))

