import nibabel as nib
import numpy as np

def get_voxel_values(image_path, mask_path):
    # Load the NIfTI image and mask
    image = nib.load(image_path)
    mask = nib.load(mask_path)
    
    # Get the data from the image and mask
    image_data = image.get_fdata()
    mask_data = mask.get_fdata()
    
    # Apply the mask to the image data
    masked_voxels = image_data[mask_data > 0]
    
    # Sort the voxel values
    sorted_voxels = np.sort(masked_voxels, axis=None)
    
    return sorted_voxels

# Example usage
if __name__ == "__main__":
    image_path = 'path_to_your_image.nii'
    mask_path = 'path_to_your_mask.nii'
    voxel_values = get_voxel_values(image_path, mask_path)
    voxel_high = np.percentile(voxel_values, 95)
    voxel_low = np.percentile(voxel_values, 5)
    print(voxel_values)