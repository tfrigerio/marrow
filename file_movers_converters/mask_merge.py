import numpy as np
import nibabel as nib
import os

def load_nifti_files_without_keywords(root_dir, keyword_1, keyword_2):
    nifti_files = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if keyword_1 not in file and keyword_2 not in file and file.endswith('.nii.gz'):
                file_path = os.path.join(root, file)
                try:
                    nifti = nib.load(file_path).get_fdata()
                    nifti_header = nib.load(file_path).header
                    nifti_files.append(nifti)
                except Exception as e:
                    print(f"Error loading file: {file_path}")
                    print(e)
    return nifti_files, nifti_header 

def merge_nifti_files(nifti_files):
    merged_nifti = np.zeros_like(nifti_files[0])
    for nifti in nifti_files:
        merged_nifti = np.logical_or(merged_nifti,nifti)
    return merged_nifti

root_dir = '/radraid/apps/personal/tfrigerio/marrow/UCLA_Lu_PSMA_trial_nifti_data/useful_segmentations/segmentation_folder/segmentations_'
keyword_1 = 'iliac'
keyword_2 = 'marrow'


for i in range(248):
    if os.path.isdir(root_dir+str(i)):
        print(f"Processing folder {i}")
        nifti_files, last_nifti_header = load_nifti_files_without_keywords(root_dir+str(i), keyword_1, keyword_2)
        merged_nifti = merge_nifti_files(nifti_files)
        print(f"Shape of merged nifti: {type(merged_nifti)}")
        #Save the merged nifti file
        output_path = '/radraid/apps/personal/tfrigerio/marrow/UCLA_Lu_PSMA_trial_nifti_data/useful_segmentations/merged/merged_segmentation_'+str(i)+'.nii.gz'
        nifti = nib.Nifti1Image(merged_nifti, affine = None, header = last_nifti_header)
        print(f"Shape of nifti: {nifti.shape}")
        nib.save(nifti, output_path)