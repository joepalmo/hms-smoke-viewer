import requests, zipfile, io
from datetime import datetime, timedelta
import gcsfs
import os
import json
import tempfile

# Set up GCS
BUCKET_NAME = 'noaa-hms'
SMOKE_PREFIX = 'smoke'
FIRE_PREFIX = 'fire'

#read the dictionary from the credential json file -- hms_creds.json
with open('credentials.json') as f:
    token = json.load(f)

fs = gcsfs.GCSFileSystem(project='smoke-aq-viewer', token=token)

def upload_to_gcs(local_path, gcs_path):
    """Upload a file to GCS using gcsfs."""
    fs.put_file(local_path, gcs_path)
    print(f'Uploaded {local_path} to {gcs_path}')


# Function to loop through dates
def get_dates_in_range(start_date, end_date):
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    return [start + timedelta(days=i) for i in range((end - start).days + 1)]

# Set today's date
# today = datetime.today()
# date_range = get_dates_in_range((today - timedelta(days=1)).strftime('%Y-%m-%d'), today.strftime('%Y-%m-%d'))

# Backfill from 2024-12-21 to yesterday
start_date = '2025-03-30'
end_date = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
# end_date = '2025-01-06'
date_range = get_dates_in_range(start_date, end_date)

smoke_zip_file_url = 'https://satepsanone.nesdis.noaa.gov/pub/FIRE/web/HMS/Smoke_Polygons/Shapefile/{}/{}/hms_smoke{}.zip'
fire_zip_file_url = 'https://satepsanone.nesdis.noaa.gov/pub/FIRE/web/HMS/Fire_Points/Shapefile/{}/{}/hms_fire{}.zip'

with tempfile.TemporaryDirectory() as temp_dir:

    for day in date_range:
        year = day.strftime("%Y")
        month = day.strftime("%m")
        fulldate = day.strftime("%Y%m%d")
        
        smoke_url = smoke_zip_file_url.format(year, month, fulldate)
        fire_url = fire_zip_file_url.format(year, month, fulldate)
        
        # smoke
        try:
            r = requests.get(smoke_url)
            z = zipfile.ZipFile(io.BytesIO(r.content))
            z.extractall(temp_dir)
            for file_name in z.namelist():
                local_path = os.path.join(temp_dir, file_name)
                gcs_path = f'{BUCKET_NAME}/{SMOKE_PREFIX}/{file_name}'
                upload_to_gcs(local_path, gcs_path)
            print(f'Uploaded {fulldate} smoke files')
        except:
            print(f'No smoke files for {fulldate}')

        # fire
        try:
            r = requests.get(fire_url)
            z = zipfile.ZipFile(io.BytesIO(r.content))
            z.extractall(temp_dir)
            for file_name in z.namelist():
                local_path = os.path.join(temp_dir, file_name)
                gcs_path = f'{BUCKET_NAME}/{FIRE_PREFIX}/{file_name}'
                upload_to_gcs(local_path, gcs_path)
            print(f'Uploaded {fulldate} fire files')
        except:
            print(f'No fire files for {fulldate}')
