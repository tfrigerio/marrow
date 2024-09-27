import os
import csv
import pydicom

def search_dicom_files(directory):
    scan_dates = []
    root_list = []
    for root, dirs, files in os.walk(directory):
        

        for file in files:
            print(f"File: {file}")
            if file.endswith(".dcm") and root not in root_list:
                file_path = os.path.join(root, file)
                try:
                    dicom_data = pydicom.dcmread(file_path)
                    scan_date = dicom_data.SeriesDate
                    scan_dates.append([scan_date,file_path])
                    print(f"Scan Date: {scan_date}, File Path: {file_path}")
                    root_list.append(root)
                except pydicom.errors.InvalidDicomError:
                    print(f"Error reading file: {file_path}")
                    pass
    return scan_dates

def write_to_csv(scan_dates, output_file):
    with open(output_file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Scan Date", "File Path"])
        for i in range(len(scan_dates)):
            writer.writerow([scan_dates[i][0], scan_dates[i][1]])
            print(f"Scan Date: {scan_dates[0]}, File Path: {scan_dates[1]}")
        csvfile.close()

# Replace "directory_path" with the path to the directory containing the DICOM files
directory_path = "/radraid/apps/personal/tfrigerio/MedSAM_sandbox/UCLA_Lu_PSMA_trial"
output_file = "/radraid/apps/personal/tfrigerio/marrow/scan_dates.csv"

scan_dates = search_dicom_files(directory_path)
write_to_csv(scan_dates, output_file)