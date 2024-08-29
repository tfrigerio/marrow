import nibabel as nib
from totalsegmentator.python_api import totalsegmentator
import os 

input_path = "/radraid/apps/personal/tfrigerio/marro/UCLA_Lu_PSMA_trial_nifti_data/converted_series_approved_0.nii.gz"
output_path = "/radraid/apps/personal/tfrigerio/marrow/UCLA_Lu_PSMA_trial_nifti_data/output/"
if __name__ == "__main__":
    # option 1: provide input and output as file paths
    for i in range (248):
        input_path = "/radraid/apps/personal/tfrigerio/marrow/UCLA_Lu_PSMA_trial_nifti_data/converted_series_approved_"+str(i)+".nii.gz"
        output_path = "/radraid/apps/personal/tfrigerio/marrow/UCLA_Lu_PSMA_trial_nifti_data/output_"+str(i)+".nii.gz"
        if not os.path.exists(output_path):




            roi = totalsegmentator(input_path,
                output = output_path,
                #roi_subset = organs,
                #device = 'gpu',
                ml = True, 
                quiet = True
                ) # Will create a multilabel array following the Totalsegmentator labels








    # option 2: provide input and output as nifti image objects
    input_img = nib.load(input_path)
    output_img = totalsegmentator(input_img)
    nib.save(output_img, output_path)