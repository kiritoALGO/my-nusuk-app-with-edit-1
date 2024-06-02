import requests

MEQR_API_KEY = 'YOUR_MEQR_API_KEY'

def upload_image_to_meqr(image_path):
    url = "https://api.me-qr.com/upload"
    files = {'file': open(image_path, 'rb')}
    headers = {'Authorization': f'Bearer {MEQR_API_KEY}'}

    response = requests.post(url, files=files, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

def generate_qr_code_for_image(image_url):
    url = "https://api.me-qr.com/create"
    headers = {'Authorization': f'Bearer {MEQR_API_KEY}'}
    data = {
        "type": "url",
        "url": image_url
    }

    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()
