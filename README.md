# SimilarLookingImages_Kopernikus
Identifies similar images in a given folder and copies all the unique images to the results folder.

Given a folder path containing multiple similar images (like images clicked with a CC camera in a parking lot at different intervals), this code copies all the unique frames to the results folder. However, it is important that all the images in the folder are readable. This code does not handle such cases and hence all the non-readable or corrupted image frames are safely ignored with the _try-except_ block. 

## 0. Install required dependencies
Open the terminal and enter the following commands to install additional libraries to execute the code.
```
pip install pathlib
pip install tqdm
```

## 1. Run code
```
python ./main.py <path_to_image_directory> <path_to_results_directory> <minimum_contour_area> <similarity_score_threshold>
```

For example, if the path to the image directory and result directory are _D:\dataset-candidates-ml\dataset_ and _D:\dataset-candidates-ml\dataset\results_ respectively. The minimum contour area to contribute to the overall score is _5000_ and the threshold value of the score is _50000_. Then the _main.py_ can be executed as:

```
python ./main.py D:\dataset-candidates-ml\dataset D:\dataset-candidates-ml\dataset\results 5000 50000
```
