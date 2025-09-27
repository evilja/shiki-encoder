import requests
import json

CLIENT_ID = ""
CLIENT_SECRET = ""
REFRESH_TOKEN = ""

UPLOAD_URL = "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart&supportsAllDrives=true"


def get_access_token():
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": REFRESH_TOKEN,
        "grant_type": "refresh_token",
    }
    r = requests.post(token_url, data=data)
    r.raise_for_status()
    return r.json()["access_token"]


def upload(filepath, parent_id="1I_yN2bvGiavbbPTIJb-ThwvDPdBsjLFY", mimetype="text/plain", outfilepath=None):
    access_token = get_access_token()
    headers = {"Authorization": f"Bearer {access_token}"}

    filename = filepath
    if outfilepath != None:
        metadatafilepath = f"{outfilepath}.mp4"
    else:
        metadatafilepath = filepath
    # Metadata
    metadata = {"name": metadatafilepath}
    if parent_id:
        metadata["parents"] = [parent_id]

    files = {
        "metadata": ("metadata", json.dumps(metadata), "application/json; charset=UTF-8"),
        "file": (filename, open(filepath, "rb"), mimetype),
    }
    try:
        response = requests.post(UPLOAD_URL, headers=headers, files=files)
        response.raise_for_status()
    except Exception as e:
        print(e)
        return False
    return f'https://drive.google.com/file/d/{response.json()["id"]}/view?usp=sharing'