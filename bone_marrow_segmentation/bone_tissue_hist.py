import numpy as np
import nibabel as nib
import os
import pandas as pd
    
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


def get_min_max(image_path, mask_path):
    image = nib.load(image_path)
    image_array = image.get_fdata()
    mask = nib.load(mask_path)
    mask_array = mask.get_fdata()
    values = image_array[mask_array==1]
    fifth_percentile = np.percentile(values, 5)
    ninety_fifth_percentile = np.percentile(values, 95)
    return fifth_percentile, ninety_fifth_percentile

def get_percentiles(image_path, mask_path, percentile_list):
    image = nib.load(image_path)
    image_array = image.get_fdata()
    mask = nib.load(mask_path)
    mask_array = mask.get_fdata()
    if np.array_equal(mask_array, np.zeros(np.shape(mask_array))) == True:
        return [0,0,0,0,0,0,0,0]
    else:
        values = image_array[mask_array==1]
        percentiles = []
        print(image_path)
        print(mask_path)
        for item in percentile_list:
            print(item)
            percentiles.append(np.percentile(values, item))    
        return percentiles

min_max_values  = []

percentile_list = [1,3,5,10,90,95,97,99]

dir = '/radraid/apps/personal/tfrigerio/marrow/UCLA_Lu_nifti_3D_data'
biglist = os.listdir(dir)
studylist = [s for s in biglist if '.py' not in s and '.csv' not in s]
study_CT_segmentation = ''
bonelist = []
percentile_df = pd.DataFrame(columns = ['bone', '1','3','5','10','90','95','97','99'])
bone = ''
percentile_output = []
csv_path = ''
for i in range(len(studylist)):
    study_path = os.path.join(dir, studylist[i])
    study = os.listdir(study_path)
    study_CTs = [s for s in study if 'CT' in s and '.nii.gz' in s]
    for j in range(len(study_CTs)):
        study_CT_segmentation = study_CTs[j].replace('.nii.gz', '_segmentation')
        seg_path = os.path.join(study_path, study_CT_segmentation)
        big_segmentation_list = os.listdir(seg_path)
        segmentation_list = [s for s in big_segmentation_list if 'marrow' not in s]
        for k in segmentation_list:
            image_path = os.path.join(study_path, study_CTs[j])
            mask_path = os.path.join(seg_path, k)
            bone = k.replace('.nii.gz', '')
            percentile_output = get_percentiles(image_path, mask_path, percentile_list)
            new_row = {'bone': bone, '1': percentile_output[0], '3': percentile_output[1], '5': percentile_output[2], '10': percentile_output[3], '90': percentile_output[4], '95': percentile_output[5], '97': percentile_output[6], '99': percentile_output[7]}
            percentile_df.loc[len(percentile_df)] = new_row
        csv_path = os.path.join(seg_path + '_percentiles.csv')
        percentile_df.to_csv(csv_path  , index=False)
        percentile_df = pd.DataFrame(columns = ['bone', '1','3','5','10','90','95','97','99'])




# for i in range(248):
#     if os.path.exists(f'/radraid/apps/personal/tfrigerio/marrow/UCLA_Lu_PSMA_trial_nifti_data/useful_segmentations/merged/merged_segmentation_{i}.nii.gz'):
#         mask_path = f'/radraid/apps/personal/tfrigerio/marrow/UCLA_Lu_PSMA_trial_nifti_data/useful_segmentations/merged/merged_segmentation_{i}.nii.gz'
#         image_path = f'/radraid/apps/personal/tfrigerio/marrow/UCLA_Lu_PSMA_trial_nifti_data/converted_series/converted_series_approved_{i}.nii.gz'
#         # np.save(f'/radraid/apps/personal/tfrigerio/marrow/bone_tissue_hist_{i}.npy', bone_tissue_hist(image_path, mask_path))
#         print(f'bone_tissue_hist_{i}.npy')
#         min_max_values.append([get_min_max(image_path, mask_path), i , np.shape(nib.load(image_path).get_fdata())])
#         print(get_min_max(image_path, mask_path))
#         print('----------------------------------')
# np.save('/radraid/apps/personal/tfrigerio/marrow/min_max_values.npy', min_max_values)
# mask_path = '/radraid/apps/personal/tfrigerio/marrow/UCLA_Lu_PSMA_trial_nifti_data/useful_segmentations/merged/merged_segmentation_0.nii.gz'
# image_path = '/radraid/apps/personal/tfrigerio/marrow/UCLA_Lu_PSMA_trial_nifti_data/converted_series/converted_series_approved_0.nii.gz'
# np.save('/radraid/apps/personal/tfrigerio/marrow/bone_tissue_hist.npy', bone_tissue_hist(image_path, mask_path))