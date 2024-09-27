import os

def save_nii_gz_paths(root_dir, output_file):
    with open(output_file, 'w') as f:
        for dirpath, _, filenames in os.walk(root_dir):
            for filename in filenames:
                if filename.endswith('.nii.gz') and "segmentation" not in dirpath:
                    file_path = os.path.join(dirpath, filename)
                    f.write(file_path + '\n')

if __name__ == "__main__":
    root_directory = '/radraid/apps/personal/tfrigerio/marrow/UCLA_Lu_nifti_3D_data'  # Change this to your root directory
    output_txt_file = '/radraid/apps/personal/tfrigerio/marrow/registration/file.txt'  # Change this to your desired output file path
    save_nii_gz_paths(root_directory, output_txt_file)