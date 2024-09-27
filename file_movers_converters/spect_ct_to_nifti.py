import os
import subprocess
import shutil
import SimpleITK as sitk
import pydicom as dcm


longlist = []
converted_series = []
save_name = ""
beta = 0
dicom_path = ""
def convert_dicom_to_nifti(input_dir, output_dir, save_name, beta):
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Recursively search for DICOM files in the input directory
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.dcm') and dcm.read_file(os.path.join(root, file)).SeriesInstanceUID not in converted_series:
                dicom_path = os.path.join(root, file)

                # Convert DICOM to NIfTI using dcm2niix
                nifti_filename = file.replace('.dcm', '.nii.gz')
                nifti_path = os.path.join(output_dir, nifti_filename)
                series_id = sitk.ImageSeriesReader_GetGDCMSeriesFileNames(os.path.abspath(root))
                        #print(series_id)
                series_reader = sitk.ImageSeriesReader()
                series_reader.SetFileNames(sitk.ImageSeriesReader.GetGDCMSeriesFileNames(os.path.abspath(root)))
                image = series_reader.Execute()
                if dcm.read_file(dicom_path).Modality == "CT":
                    save_name = f"CT_{beta}.nii.gz"
                    beta += 1
                elif dcm.read_file(dicom_path).Modality == "PT":
                    save_name = f"PT_{beta}.nii.gz"
                    beta += 1
                elif dcm.read_file(dicom_path).Modality == "MR":
                    save_name = f"MR_{beta}.nii.gz"
                    beta += 1
                elif dcm.read_file(dicom_path).Modality == "NM":
                    save_name = f"NM_{beta}.nii.gz"
                    beta += 1
                
                if dcm.read_file(dicom_path).StudyID not in longlist:
                    os.makedirs(os.path.join(output_dir, dcm.read_file(dicom_path).StudyID), exist_ok=True)                
                
                output_path = os.path.join(output_dir, dcm.read_file(dicom_path).StudyID, save_name)
                sitk.WriteImage(image, output_path)
                print(f"Converted {dicom_path} to {output_path}")
                longlist.append(dcm.read_file(dicom_path).StudyID)
                # with open("outputlist.txt", "a
                #subprocess.run(['dcm2niix', '-z', 'y', '-o', output_dir, dicom_path])
                converted_series.append(dcm.read_file(os.path.join(root, file)).SeriesInstanceUID)

                # Move the converted NIfTI file to the corresponding directory in the output directory
                # output_subdir = os.path.relpath(root, input_dir)
                # output_subdir_path = os.path.join(output_dir, output_subdir)
                # os.makedirs(output_subdir_path, exist_ok=True)
                #shutil.move(nifti_path, os.path.join(output_subdir_path, nifti_filename))

# Example usage
input_dir = '/radraid/apps/personal/tfrigerio/MedSAM_sandbox/UCLA_Lu_PSMA_trial/data'
output_dir = '/radraid/apps/personal/tfrigerio/marrow/UCLA_Lu_nifti_4'
convert_dicom_to_nifti(input_dir, output_dir, save_name, beta)