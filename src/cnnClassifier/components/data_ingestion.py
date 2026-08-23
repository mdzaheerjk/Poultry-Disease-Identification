import os
import urllib.request as request
import zipfile
import shutil
from cnnClassifier import logger
from cnnClassifier.utils.common import get_size
from cnnClassifier.entity.config_entity import DataIngestionConfig
from pathlib import Path

class DataIngestion:
    def __init__(self,config:DataIngestionConfig):
        self.config=config

    def download_file(self):
        if not os.path.exists(self.config.local_data_file):
            try:
                filename,headers=request.urlretrieve(
                    url=self.config.source_URL,
                    filename=self.config.local_data_file
                )
                logger.info(f"{filename} download with following info : \n {headers}")
            except Exception as e:
                logger.warning(f"Download failed: {e}. Attempting fallback from local data directory.")
                local_backup = os.path.join("data", "Chicken-fecal-images.zip")
                if os.path.exists(local_backup):
                    shutil.copy(local_backup, self.config.local_data_file)
                    logger.info(f"Copied local backup file from {local_backup} to {self.config.local_data_file}")
                else:
                    raise e
        else:
            logger.info(f"File already exists of size : {get_size(Path(self.config.local_data_file))}")


    def extract_zip_file(self):
        unzip_path=self.config.unzip_dir
        os.makedirs(unzip_path,exist_ok=True)
        with zipfile.ZipFile(self.config.local_data_file,'r') as zip_ref:
            zip_ref.extractall(unzip_path)
