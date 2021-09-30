import os
import uuid
import random
import decimal
from datetime import datetime
from dateutil import tz
from AwsS3Resource import AwsS3Resource
from time import sleep
import threading

numberDevices = int(os.environ['DV_NUMBER'])
interval = int(os.environ['INTERVAL_SEC'])
maxAudios = int(os.environ['MAX_IMAGES'])
imagePath = os.environ['IMAGE_PATH']
imageFiles = os.listdir(imagePath)
awsS3Resource = AwsS3Resource()

def runDevice(num):
    deviceUUID = uuid.uuid4().__str__()
    print('Device "{}" and UUID "{}" Job started'.format(num, deviceUUID))
    now = datetime.now(tz=tz.tzutc())
    date_time = now.strftime("%Y-%m-%dT%H:%M:%S")
    devInfo = {
        'Metadata': {
            "id": deviceUUID,
            "location-lon": str(-float(decimal.Decimal(random.randrange(74030000, 74200000))/1000000)),
            "location-lat": str(float(decimal.Decimal(random.randrange(4590000, 4770000))/1000000)),
            "description": "Calle {} N. {}-{}".format(random.randint(1, 100),
                                                      random.randint(1, 100),
                                                      random.randint(1, 100)),
            "time": date_time,
            "index_name": "visual_result"
        }
    }

    for i in range(0, maxAudios):
        currentImageUUID = uuid.uuid4().__str__()
        imageAbsPath = imagePath+"/"+imageFiles[i]
        print('img path {}'.format(imageAbsPath))
        devInfo['Metadata']['data_uuid'] = currentImageUUID
        awsS3Resource.uploadData(imageAbsPath, currentImageUUID, devInfo)
        print('Device "{}" send Image number "{}" and UUID "{}"'.format(num, i, currentImageUUID))
        sleep(interval)

def main():
    threads = []
    for i in range(0, numberDevices):
        t = threading.Thread(target=runDevice, args=(i,))
        threads.append(t)
        t.start()

if __name__ == "__main__":
    main()