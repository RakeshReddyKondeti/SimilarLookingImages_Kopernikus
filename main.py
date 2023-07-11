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

    # To visualize threshold images and contours. Do not change it to 'True' if you care about your time and computer.
    visualize_thresh = False

    # outer loop to iterate over cameras and their corresponding images
    for cam, files in tqdm(cameras_and_names.items(), desc= 'Camera index', ncols=100):
        frame_score = {}    # a dict to contain scores
        # inner loop to iterate through all the corresponding images for every camera
        for idx, next_frame_name in enumerate(tqdm(files, desc= 'Image frame', ncols= 100, position=1, leave=False)):
            try:
                # a simple (non-essential) sanity check
                if not cam in PureWindowsPath(next_frame_name).name:
                    continue
                
                next_frame= cv2.imread(str(next_frame_name))
                next_frame= preprocess_image_change_detection(next_frame, gaussian_blur_radius_list=[5])
                next_frame= resize(next_frame)     # resizing all the frames here

                if idx == 0:
                    shutil.copy(str(next_frame_name), str(results_dir))   # copy first image of every camera to the results folder
                    prev_frame_name = next_frame_name                     # after first image of the camera is copied to results, the first image becomes prev_frame 
                    prev_frame= next_frame.copy()
                    continue
                

                score, res_cnts, thresh = compare_frames_change_detection(prev_frame, next_frame, min_cntr_area)
                
                # visualizing threshold image and contours 
                if visualize_thresh:
                    visualize_threshold_image(thresh)  
                    visualize_contours(next_frame.copy(), res_cnts)

                # next frame is the prev_frame for next iteration
                prev_frame_name = next_frame_name
                prev_frame = next_frame.copy()

                frame_score.update({prev_frame_name: score})

            except:
                pass
        
        # copy all the non-duplicate or dissimilar images to results folder
        remove_images(frame_score, sim_thres, results_dir)


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

