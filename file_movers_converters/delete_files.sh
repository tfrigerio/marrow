#!/bin/bash

# Directory to delete files from
directory="/radraid/apps/personal/tfrigerio/marrow/UCLA_Lu_nifti_3D_data"

# File containing the list of useful segmentations
useful_segmentations_file="/radraid/apps/personal/tfrigerio/marrow/text_lists/useful_segmentations.txt"
cd "$directory" || exit
echo "Current directory: $(pwd)"
# Loop through all files in the directory
for dir in *; do

    cd "$dir" || exit
    # Print the current directory
    echo "Current directory: $(pwd)"
    for subdir in *segmentation; do
        # Check if subdirectory includes word segmentation
        cd "$subdir" || exit
        for file in ./*.nii.gz; do
            echo "Processing file: $file"
            if [[ "$file" == *marrow* ]]; then
                echo "Deleting file: $file"
                rm "$file"
            fi
        done
        cd ..
    done
    cd ..
done