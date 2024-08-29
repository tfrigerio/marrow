import numpy as np
import nibabel as nib
import os

    
def histogram(img, mask, bins=100):
    max_val = np.max(img)
    min_val = np.min(img)
    hist = np.zeros(bins)
    for i in range(bins):
        for j in img[mask==1]:
            if min_val + (i+1) * (max_val - min_val) / bins >= j and j>= min_val + i * (max_val - min_val) / bins:
                hist[i] += 1
       # hist[i] = np.sum(min_val + (i+1) * (max_val - min_val) / bins >= img[mask==1] >= min_val + i * (max_val - min_val) / bins)

    return hist

def bone_tissue_hist(image_path, bone_mask_path):
    image = nib.load(image_path)
    image_array = image.get_fdata()
    bone_mask = nib.load(bone_mask_path)
    bone_mask_array = bone_mask.get_fdata()
    hist = histogram(image_array, bone_mask_array)
    return hist
mask_path = '/radraid/apps/personal/tfrigerio/marrow/UCLA_Lu_PSMA_trial_nifti_data/useful_segmentations/merged/merged_segmentation_0.nii.gz'
image_path = '/radraid/apps/personal/tfrigerio/marrow/UCLA_Lu_PSMA_trial_nifti_data/converted_series/converted_series_approved_0.nii.gz'
np.save('/radraid/apps/personal/tfrigerio/marrow/bone_tissue_hist.npy', bone_tissue_hist(image_path, mask_path))