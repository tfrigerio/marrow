# This agent was generated using core's "generate" tool.
#
# To start using your agent immediately, move it into the "python"
# directory in the root directory of core, and configure it to
# utilize the "local" runner.
#
# More generally, python agents do NOT need to be compiled into core for
# general use, however keep in mind that the runner the agent is
# matched with must be able to (1) find the script to start it, and (2)
# resolve any of your script's dependencies (i.e. environment management)
#
# If you think your agent would be broadly useful, please consider
# submitting it back to us via merge request!
#
# TODO: include link to complete python agent example
# https://gitlab.com/hoffman-lab/core/-/issues
# https://gitlab.com/hoffman-lab/core/-/merge_requests

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import asyncio
from core_utils import Agent, default_args, Log, AgentState

import traceback

class DicomUploader(Agent):
    
    def __init__(self, spec, bb):
        super().__init__(spec, bb)
        
    async def run(self):
        try:
            await self.log(Log.INFO,"Hello from DicomUploader")
            dir_path = str(self.attributes.value("dir_path"))
            dirlist = os.listdir(dir_path)
            
            filelist = []
            templist = []
            for i in dirlist:
                if i.endswith('.dcm'):
                    filelist.append(dir_path+i)
                else:
                    templist = os.listdir(i)
                    for j in templist:
                        if j.endswith('.dcm'):
                            filelist.append(dir_path+i+j)
                        else:
                            pass
            preprocessed_images = np.array([])
            for i in filelist:
                ds = dicom.dcmread(i, force=True)
                if ds.transfer_syntax == dicom.UID.ImplicitVRLittleEndian:
                    preprocessed_images = np.append(preprocessed_images, ds.pixel_array.astype(int))

            self.post_result('preprocessed_images', "list", data=str(preprocessed_images))
            # Your code HERE
            
        except Exception as e:
            await self.post_status_update(AgentState.ERROR, traceback.format_exc())
            print(traceback.format_exc())
        finally:
            self.stop()

if __name__=="__main__":    
    spec, bb = default_args("dicom_uploader.py")
    t = DicomUploader(spec, bb)
    t.launch()

