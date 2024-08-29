#!/bin/bash

source_dir="/radraid/apps/personal/tfrigerio/marrow/UCLA_Lu_PSMA_trial_nifti_data"
target_dir="/radraid/apps/personal/tfrigerio/marrow/UCLA_Lu_PSMA_trial_nifti_data/converted_series"

# Move folders starting with "segmentations_" to the target directory
find "$source_dir" -type f -name "converted_series_approved*" -exec mv -t "$target_dir" {} +