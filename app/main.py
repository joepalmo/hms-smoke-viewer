import gcsfs
from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, HTMLResponse
import geopandas as gpd
from datetime import datetime
import os
import tempfile
import shutil
import json

project_id = 'smoke-aq-viewer'

# Try using a local credentials.json if it exists
if os.path.exists('credentials.json'):
    with open('credentials.json') as f:
        token = json.load(f)
    fs = gcsfs.GCSFileSystem(project=project_id, token=token)
else:
    # Fallback to default credentials (for Cloud Run)
    fs = gcsfs.GCSFileSystem(project=project_id)

app = FastAPI()

# Serve static files (HTML, JS, CSS)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Correctly serve the index.html file from /static
@app.get("/")
async def get_index():
    with open("app/static/index.html", "r") as file:
        content = file.read()
    return HTMLResponse(content=content)


def fetch_shapefile_from_gcs(base_filename):
    """
    Fetches the full shapefile set (shp, shx, dbf, prj) from a Google Cloud Storage bucket.

    Args:
        bucket_name (str): The name of the GCS bucket.
        base_filename (str): The base name of the shapefile (without extension).
        local_dir (str): Local directory to store downloaded files (default is /tmp).

    Returns:
        List[str]: A list of local file paths for the downloaded shapefile components.
    """

    # Create a temporary directory
    with tempfile.TemporaryDirectory() as tmpdirname:
        print(base_filename)
        print(f"Temporary directory created at: {tmpdirname}")
        
        # List of shapefile extensions
        shapefile_extensions = ['.shp', '.shx', '.dbf', '.prj']
        
        # Download each component of the shapefile into the temporary directory
        for ext in shapefile_extensions:
            remote_path = f"noaa-hms/{base_filename}{ext}"
            local_path = f"{tmpdirname}/{base_filename.split('/')[-1]}{ext}"
            print(remote_path)
            with fs.open(remote_path, 'rb') as remote_file, open(local_path, 'wb') as local_file:
                shutil.copyfileobj(remote_file, local_file)
        
        # Once downloaded, load the shapefile using Geopandas
        gdf = gpd.read_file(f"{tmpdirname}/{base_filename.split('/')[-1]}.shp")

    return gdf


@app.get("/data/fire", response_class=JSONResponse)
def get_fire_data(date: str = Query(...)):
    date_str = date #'2024-10-23'  # Replace this with your actual date string
    formatted_date = datetime.strptime(date_str, '%Y-%m-%d').strftime('%Y%m%d')
    base_filename = f'fire/hms_fire{formatted_date}'
    gdf = fetch_shapefile_from_gcs(base_filename)
    gdf = gdf.to_crs(epsg=4326)
    gdf = gdf[(gdf['FRP'] > 50)] # Filter out fires with low FRP
    return JSONResponse(content=gdf.to_json())

@app.get("/data/smoke", response_class=JSONResponse)
def get_smoke_data(date: str = Query(...)):
    date_str = date  # Replace this with your actual date string
    formatted_date = datetime.strptime(date_str, '%Y-%m-%d').strftime('%Y%m%d')
    base_filename = f'smoke/hms_smoke{formatted_date}'
    # base_filename = f'smoke/hms_smoke20230731'
    gdf = fetch_shapefile_from_gcs(base_filename)
    # gdf = fetch_shapefile_from_gcs('smoke/hms_smoke20230731')
    gdf = gdf.to_crs(epsg=4326)
    return JSONResponse(content=gdf.to_json())