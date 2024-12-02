import os
import requests
from requests.auth import HTTPBasicAuth

# GitHub credentials
GITHUB_TOKEN = ""
REPO_OWNER = "ChialingWei"
REPO_NAME = "SRP_turbine"
BRANCH = "main"  # e.g., "main"
FOLDER_PATH = "damage_detection_system"  # e.g., "src/code"
DESTINATION_PATH = f"Desktop/{FOLDER_PATH}"

os.makedirs(FOLDER_PATH, exist_ok=True)

# GitHub API base URL
API_URL= f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FOLDER_PATH}?ref={BRANCH}"

response = requests.get(API_URL, auth=HTTPBasicAuth(REPO_OWNER, GITHUB_TOKEN))
response.raise_for_status()  # Raise an error for bad status codes

# Headers for authentication
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

def download_file(file_url, local_path):
    response = requests.get(file_url, headers=HEADERS)
    response.raise_for_status()  # Raise error for bad status codes
    with open(local_path, 'wb') as file:
        file.write(response.content)
    print(f"Downloaded {local_path}")

def download_folder(folder_url, destination_path):
    response = requests.get(folder_url, headers=HEADERS)
    response.raise_for_status()
    contents = response.json()

    if not os.path.exists(destination_path):
        os.makedirs(destination_path)

    for item in contents:
        item_name = item['name']
        item_path = os.path.join(destination_path, item_name)

        if item['type'] == 'file':
            download_file(item['download_url'], item_path)
        elif item['type'] == 'dir':
            download_folder(item['url'], item_path)

if __name__ == "__main__":
    download_folder(API_URL, DESTINATION_PATH)


