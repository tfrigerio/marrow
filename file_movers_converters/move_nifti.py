import os
import shutil
import pandas as pd

list_dicom = []
list_nifti = []
def move_nifti_files(source_dir, destination_dir):
    for root, dirs, files in os.walk(source_dir):
        
        #print(files)
        for file in files:
            if file.endswith('.nii') or file.endswith('.nii.gz') and 'converted_series_approved' in file:
                source_path = os.path.join(root, file)
                destination_path = os.path.join(destination_dir, file)
                shutil.move(source_path, destination_path)
                list_nifti.append(destination_path)
                list_dicom.append(root)

# Example usage
source_directory = '/radraid/apps/personal/tfrigerio/MedSAM_sandbox/UCLA_Lu_PSMA_trial'
destination_directory = '/radraid/apps/personal/tfrigerio/marrow/UCLA_Lu_nifti_2'

move_nifti_files(source_directory, destination_directory)

df = pd.DataFrame(list(zip(list_dicom, list_nifti)), columns = ['dicom_path', 'nifti_path'])
df.to_csv('/radraid/apps/personal/tfrigerio/dicom_to_nifti.csv', index=False)
