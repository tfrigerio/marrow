import itk
import SimpleITK as sitk


scan1_path = '/radraid/apps/personal/tfrigerio/marrow/UCLA_Lu_nifti_3D_data/305476983/CT_393.nii.gz'
scan2_path = '/radraid/apps/personal/tfrigerio/marrow/UCLA_Lu_nifti_3D_data/305476983/NM_391.nii.gz'
fixed_image = itk.imread(scan1_path)
moving_image = itk.imread(scan2_path)
resultImage, params  = itk.elastix_registration_method(fixed_image, moving_image)
print(params)
print(resultImage.GetSpacing())
print(resultImage.GetOrigin())
registered_scan_path = '/radraid/apps/personal/tfrigerio/marrow/registration/registered_scan.nii.gz'
itk.imwrite(resultImage, registered_scan_path)