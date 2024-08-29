import os
import SimpleITK as sitk
import pydicom as dcm
longlist = []
converted_series = []
#test
def convert_dicom_to_nifti(input_dir, output_dir):
    beta = 0
    for root, dirs, files in os.walk(input_dir):
        
        for file in files:
    
            if file.endswith(".dcm"):
                
                dicom_path = os.path.abspath(root)
                if dcm.read_file(os.path.join(dicom_path, file)).Modality != "CT":
                    continue
                else:
                #print(dicom_path)
                    if dcm.read_file(os.path.join(dicom_path, file)).SeriesInstanceUID in converted_series:
                        continue
                    else:
                        series_id = sitk.ImageSeriesReader_GetGDCMSeriesFileNames(dicom_path)
                        #print(series_id)
                        series_reader = sitk.ImageSeriesReader()
                        series_reader.SetFileNames(sitk.ImageSeriesReader.GetGDCMSeriesFileNames(dicom_path))
                        image = series_reader.Execute()
                        output_path = os.path.join(dicom_path, f"converted_series_approved_{beta}.nii.gz")
                        beta += 1
                        sitk.WriteImage(image, output_path)
                        print(f"Converted {dicom_path} to {output_path}")
                        longlist.append(output_path)
                        # with open("outputlist.txt", "a") as file:
                        #     file.write(f"{output_path} , {dicom_path}\n")
                        converted_series.append(dcm.read_file(os.path.join(dicom_path, file)).SeriesInstanceUID)
                    # Write each element of longlist to a txt file

# Example usage
input_dir = "/radraid/apps/personal/tfrigerio/MedSAM_sandbox/UCLA_Lu_PSMA_trial/data"
output_dir = "/radraid/apps/personal/tfrigerio/marrow/UCLA_Lu_nifti_2"
convert_dicom_to_nifti(input_dir, output_dir)