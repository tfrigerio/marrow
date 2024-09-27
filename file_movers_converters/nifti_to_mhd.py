import SimpleITK as sitk
import sys
import os

def convert_nifti_to_mhd(nifti_file, output_dir):
    # Read the NIfTI file
    image = sitk.ReadImage(nifti_file)
    
    # Create the output file path
    base_name = os.path.basename(nifti_file)
    output_file = os.path.join(output_dir, os.path.splitext(base_name)[0] + '.mhd')
    
    # Write the image to the MetaImage format
    sitk.WriteImage(image, output_file)
    print(f"Converted {nifti_file} to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python nifti_to_mhd.py <input_nifti_file> <output_directory>")
        sys.exit(1)
    
    nifti_file = sys.argv[1]
    output_dir = sys.argv[2]
    
    if not os.path.exists(nifti_file):
        print(f"Error: The file {nifti_file} does not exist.")
        sys.exit(1)
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    convert_nifti_to_mhd(nifti_file, output_dir)