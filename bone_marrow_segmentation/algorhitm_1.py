import numpy as np 
import nibabel as nib
import numpy as np 
from scipy.ndimage import binary_dilation, binary_erosion
import os
import time


#Step 1: Load image and bone mask
def load_image_and_bone_mask(image_path, bone_mask_path):
    image = nib.load(image_path)
    image_array = image.get_fdata()
    bone_mask = nib.load(bone_mask_path)
    bone_mask_array = bone_mask.get_fdata()
    return image, bone_mask, image_array, bone_mask_array

#Step 2 Isolate bone on image
def isolate_bone_on_image(image_array, bone_mask_array):
    bone_array = image_array * bone_mask_array
    return bone_array

#Step 3 Threshold segmentation of bone marrow
def threshold_segmentation_of_bone_marrow(bone_array, threshold_up, threshold_down, bone_mask_array):
    bone_marrow_array_mask = np.zeros(bone_array.shape)
    bone_marrow_array_mask[bone_array < threshold_up] = 1
    bone_marrow_array_mask[bone_array <= threshold_down] = 0
    bone_marrow_array_mask = bone_marrow_array_mask * bone_mask_array
    return bone_marrow_array_mask

#Step 4 Zero-shot segmentation of bone marrow

#Step 5 Matching of bone marrow segmentations

#Step 6 Postprocessing

def opening3D(bone_marrow_array_mask, iterations):
    kernel = np.ones((5, 5, 5), np.uint8)
    eroded = binary_erosion(bone_marrow_array_mask, structure=kernel, iterations=iterations)
    opened = binary_dilation(eroded, structure=kernel, iterations=iterations)
    return opened



def connected_component_processing(bone_marrow_array_mask,bone_mask):
    connected_components = nib.Nifti1Image(bone_marrow_array_mask, affine=None, header=bone_mask.header)
    #print(connected_components.header)
  
    connected_components.header['pixdim']=bone_mask.header['pixdim']
    connected_components.header['xyzt_units']=bone_mask.header['xyzt_units']
    connected_components.header['qform_code']=bone_mask.header['qform_code']
    connected_components.header['sform_code']=bone_mask.header['sform_code']
    connected_components.header['quatern_b']=bone_mask.header['quatern_b']
    connected_components.header['quatern_c']=bone_mask.header['quatern_c']
    connected_components.header['quatern_d']=bone_mask.header['quatern_d']
    connected_components.header['qoffset_x']=bone_mask.header['qoffset_x']
    connected_components.header['qoffset_y']=bone_mask.header['qoffset_y']
    connected_components.header['qoffset_z']=bone_mask.header['qoffset_z']
    connected_components.header['srow_x']=bone_mask.header['srow_x']
    connected_components.header['srow_y']=bone_mask.header['srow_y']
    connected_components.header['srow_z']=bone_mask.header['srow_z']
    
    return connected_components

#Step 7 Saving masks
def save_masks(connected_components, output_path):
    nib.save(connected_components, output_path)

def full_pipeline(image_path, bone_mask_path, output_path, length):
    image, bone_mask, image_array, bone_mask_array = load_image_and_bone_mask(image_path, bone_mask_path)
    if image_array.shape != bone_mask_array.shape:
        if image_array.shape[-1] == 1:
            image_array = image_array[:, :, :, 0]
        else:
            raise ValueError('Image and mask have different shapes')
    bone_array = isolate_bone_on_image(image_array, bone_mask_array)
    bone_marrow_array_mask = threshold_segmentation_of_bone_marrow(bone_array, 350, -100, bone_mask_array)
    if np.shape(image_array)[0] >= 100 and np.shape(image_array)[1] >= 100 and np.shape(image_array)[2] >= 100:
        bone_marrow_array_mask = opening3D(bone_marrow_array_mask, 1)
    
    connected_components = connected_component_processing(bone_marrow_array_mask, bone_mask)
    save_masks(connected_components, output_path)
    return print(bone_mask_path[length:])

image_path_base = '/radraid/apps/personal/tfrigerio/marrow/UCLA_Lu_PSMA_trial_nifti_data/converted_series/converted_series_approved_'
bone_mask_path_base = '/radraid/apps/personal/tfrigerio/marrow/UCLA_Lu_PSMA_trial_nifti_data/useful_segmentations/merged/merged_segmentation_'
output_path_base = '/radraid/apps/personal/tfrigerio/marrow/UCLA_Lu_PSMA_trial_nifti_data/useful_segmentations/merged/merged_segmentation_'
length = len('/radraid/apps/personal/tfrigerio/marrow/UCLA_Lu_PSMA_trial_nifti_data/useful_segmentations/merged')

# segmentationlist=[]
# with open('/radraid/apps/personal/tfrigerio/marrow/text_lists/useful_segmentations.txt','r') as f:
#     for line in f:
#         segmentationlist.append(line[:-1])
# paths_to_non_ct_scans = []
# with open('/radraid/apps/personal/tfrigerio/non_ct_scans_path.txt','r') as f:
#     for line in f:
#         paths_to_non_ct_scans.append(line[:-1])
# print(paths_to_non_ct_scans)
for i in range(0,248):
    image_path = image_path_base+str(i)+'.nii.gz'
    bone_mask_path = bone_mask_path_base+str(i)+'.nii.gz'
    if not os.path.exists(bone_mask_path):
        continue
    output_path = output_path_base+str(i)+'_marrow.nii.gz'
    print('New Scan: '+str(i))
    t_0 = time.time()
    full_pipeline(image_path, bone_mask_path, output_path, length)

    t_1 = time.time()
    if t_1-t_0<=10:
        print('Time: '+str(t_1-t_0))

   