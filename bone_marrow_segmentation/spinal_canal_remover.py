import numpy as np
import nibabel as nib
import os

def load_image_and_spinal_canal(image_path, bone_mask_path):
    image = nib.load(image_path)
    image_array = image.get_fdata()
    bone_mask = nib.load(bone_mask_path)
    bone_mask_array = bone_mask.get_fdata()
    return image, bone_mask, image_array, bone_mask_array

def subtract_spinal_canal(image_array, spinal_array):
    non_spinal_canal = np.ones(np.shape(spinal_array))-spinal_array
    bone_marrow = image_array*non_spinal_canal
    return bone_marrow

def save_masks(connected_components, output_path):
    nib.save(connected_components, output_path)

dir = '/radraid/apps/personal/tfrigerio/marrow/UCLA_Lu_nifti_3D_data'
biglist = os.listdir(dir)
studylist = [s for s in biglist if '.py' not in s and '.csv' not in s]
for i in range(len(studylist)):
    study_path = os.path.join(dir, studylist[i])
    study = os.listdir(study_path)
    print(study)
    study_seg = [s for s in study if 'segmentation' in s]
    for j in range(len(study_seg)):
        for num in ['180', '200', '220']:
            seg_path = os.path.join(study_path, study_seg[j])
            marrow_path = os.path.join(seg_path, 'assembled_segmentation_marrow_sub' + num + '.nii.gz')
            spinal_path = os.path.join(seg_path, 'spinal_cord.nii.gz')
            output_path = os.path.join(seg_path, 'assembled_segmentation_marrow_sub' + num + '_no_spinal.nii.gz')
            if os.path.exists(marrow_path) != True:
                print('No marrow segmentation found')
                continue
            marrow, spinal, marrow_array, spinal_array = load_image_and_spinal_canal(marrow_path, spinal_path)
            bone_marrow = subtract_spinal_canal(marrow_array, spinal_array)
            marrow_spine_removed = nib.Nifti1Image(bone_marrow, marrow.affine)
            save_masks(marrow_spine_removed, output_path)
            print('DONE: ' + output_path)
