#!/bin/bash

# Directory to delete files from
directory="/radraid/apps/personal/tfrigerio/marrow/UCLA_Lu_PSMA_trial_nifti_data/useful_segmentations/segmentation_folder/segmentations_"

# File containing the list of useful segmentations
useful_segmentations_file="/radraid/apps/personal/tfrigerio/marrow/text_lists/useful_segmentations.txt"

# Loop through all files in the directory
for ((i=0; i<=247; i++)); do
    directory_name="$directory$i"
    for file in "$directory_name"/*; do
        # Check if the file is listed in useful_segmentations.txt
        if ! grep -q "$(basename "$file")" "$useful_segmentations_file"; then
            # Delete the file
            rm "$file"
            echo "Deleted file: $file"
        fi
    done
done