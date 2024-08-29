import os
segmentationlist=[]

with open('/radraid/apps/personal/tfrigerio/marrow/text_lists/useful_segmentations.txt','r') as f:
    for line in f:
        segmentationlist.append(line[:-1])

print(segmentationlist)
