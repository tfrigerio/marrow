import csv
import nibabel as nib
import numpy as np
from sklearn.metrics import jaccard_score

def dice_score(y_true, y_pred):
    intersection = np.sum(y_true * y_pred)
    return (2. * intersection) / (np.sum(y_true) + np.sum(y_pred))

def read_nifti_file(filepath):
    return nib.load(filepath).get_fdata()

def main(csv_path):
    with open(csv_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            path1, path2 = row
            img1 = read_nifti_file(path1)
            img2 = read_nifti_file(path2)
            score = dice_score(img1, img2)
            print(f'Dice score between {path1} and {path2}: {score}')

if __name__ == "__main__":
    csv_path = 'path_to_your_csv_file.csv'  # Replace with your CSV file path
    main(csv_path)