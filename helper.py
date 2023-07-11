from pathlib import Path, WindowsPath
from typing import Dict
import cv2, shutil
import numpy as np


__all__ = ["delete_folder",
           "remove_images",
           "resize",
           "visualize_threshold_image",
           "visualize_contours"]



def delete_folder(pth: WindowsPath)-> None:
    """Deletes the folder or directory if already exists! Takes input as the path to the (results) directory 
    and checks if the directory already exists. If yes, this function iteratively deletes all the contents and
    also the directory itself.
    Args:
        pth (WindowsPath): (absolute) path to the folder or directory
    """
    for sub in pth.iterdir():
        if sub.is_dir():
            delete_folder(sub)
        else:
            sub.unlink()
    pth.rmdir()




def remove_images(frame_score: Dict, sim_threshold: int, results_dir: WindowsPath)->None:
    """Removes all the duplicate images or copies all the non-duplicate images to the results directory.

    Args:
        frame_score (dict): the similarity score of the current and the preceding frame
        sim_threshold (int): Similartiy threshold to classify as duplicate vs non-duplicate frame
        results_dir (WindowsPath): path to the results directory
    """
    sorted(frame_score.items(), key=lambda kv:(kv[1], kv[0]))
    for (k,v) in frame_score.items():
         if v>sim_threshold:
            shutil.copy(str(k), str(results_dir))




def resize(img_frame: np.ndarray)->np.ndarray:
    """Used to resize a given image

    Args:
        img_frame (numpy array): Takes a numpy image as argument

    Returns:
        numpy array: resized image
    """
    return cv2.resize(img_frame, (640,480))




def visualize_threshold_image(image: np.ndarray)->None:
    """To visualize threshold images

    Args:
        image (numpy array): a numpy array or cv2.imread() image
    """
    assert isinstance(image, np.ndarray)
    cv2.imshow('Threshold Image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



def visualize_contours(image: np.ndarray, cnts: list)->None:
    """Visualize contours contributing to final score.

    Args:
        image (numpy array): a numpy array or cv2.imread() image
        cnts (list): list containing contours 
    """
    assert isinstance(image, np.ndarray)
    cv2.drawContours(image, cnts, -1, (0, 255, 0), 3)
    cv2.imshow('Visualizing Contours', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()