import os
import pydicom
import nibabel as nib

def process_dicom_files(root_dir, output_file):
    with open(output_file, 'w') as f:
        for root, dirs, files in os.walk(root_dir):
            for file in files:
                if file.endswith('.dcm'):
                    file_path = os.path.join(root, file)
                    try:
                        ds = pydicom.dcmread(file_path)
                        if ds.Modality == 'NM':
                            if ds.pixel_array.shape[0] >= 5 and len(ds.pixel_array.shape) == 3 and ds.pixel_array.shape[2] >= 5:
                                f.write(str(ds.pixel_array.shape) + ', ')
                                f.write(file_path + '\n')
                                print(ds.pixel_array.shape)
                                print(file_path)
                    except pydicom.errors.InvalidDicomError:
                        pass

def process_nifti_files(root_dir):
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.nii') or file.endswith('.nii.gz'):
                file_path = os.path.join(root, file)
                try:
                    img = nib.load(file_path)
                    shape = img.shape
                    print(shape)
                    if len(shape) == 4:
                        print("again")
                        img_3d = img.slicer[:, :, :, 0]
                        nib.save(img_3d, file_path)
                        img = nib.load(file_path)
                        shape = img.shape
                        print(shape)
                    if any(dim < 5 for dim in shape) or len(shape) == 2:
                        os.remove(file_path)
                except nib.filebasedimages.ImageFileError:
                    pass
# Usage example
# root_dir = '/radraid/apps/personal/tfrigerio/MedSAM_sandbox/UCLA_Lu_PSMA_trial'
# output_file = '/radraid/apps/personal/tfrigerio/marrow/text_lists/3d_SPECT_scans.txt'
root_dir = '/radraid/apps/personal/tfrigerio/marrow/UCLA_Lu_nifti_3D_data'
process_nifti_files(root_dir)