import os
import nibabel as nib
import numpy as np
import shutil

def load_nifti_files(root_dir, keyword):
    nifti_files = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if keyword in file and file.endswith('.nii.gz'):
                file_path = os.path.join(root, file)
                try:
                    nifti = nib.load(file_path).get_fdata()
                    nifti_files.append(nifti)
                except Exception as e:
                    print(f"Error loading file: {file_path}")
                    print(e)
    return nifti_files

root_dir = '/radraid/apps/personal/tfrigerio/marrow/UCLA_Lu_PSMA_trial_nifti_data/converted_series'
keyword = 'marrow'
nifti_files = load_nifti_files(root_dir, keyword)

# Do something with the loaded NIfTI files
#for nifti in nifti_files:
    # Process each NIfTI file here
 #   countzero 
    #pass
'''
list_of_files = os.listdir(root_dir)
nifti_files = []
for file in list_of_files:
    if file.endswith('.nii.gz'):
        file_path = os.path.join(root_dir, file)
        try:
            nifti = nib.load(file_path).get_fdata()
            nifti_files.append(np.shape(nifti))
            if np.shape(nifti)[0] <= 10 or np.shape(nifti)[1] <= 10 or np.shape(nifti)[2] <= 10:
                with open('/radraid/apps/personal/tfrigerio/wierd_shapes.txt', 'a') as f:
                    f.write(f"{file_path} {np.shape(nifti)}\n")
        except Exception as e:
            print(f"Error loading file: {file_path}")
            print(e)
'''
with open('/radraid/apps/personal/tfrigerio/non_ct_scans_numbers.txt', 'r') as f:
    lines = f.readlines()

#with open('/radraid/apps/personal/tfrigerio/wierd_shapes.txt', 'w') as f:
 ##   for line in lines:
   #     f.write('/radraid/apps/personal/tfrigerio/UCLA_Lu_PSMA_trial_nifti_data/converted_series/converted_series_approved_' + line+'.nii.gz\n')

# for i in lines:
#     file_path = '/radraid/apps/personal/tfrigerio/UCLA_Lu_PSMA_trial_nifti_data/converted_series/converted_series_approved_' + i[:-1] + '.nii.gz'
#     if os.path.exists(file_path):
#         os.remove(file_path)
#     else:
#         print(f"File {file_path} does not exist.")
        
#     shutil.rmtree('/radraid/apps/personal/tfrigerio/UCLA_Lu_PSMA_trial_nifti_data/useful_segmentations/segmentation_folder/segmentations_' + i[:-1]) 
nifti = nib.load('/radraid/apps/personal/tfrigerio/UCLA_Lu_PSMA_trial_nifti_data/converted_series/converted_series_approved_14.nii.gz').get_fdata()
print(np.shape(nifti))