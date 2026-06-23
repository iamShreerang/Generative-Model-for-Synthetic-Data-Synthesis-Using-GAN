"""
Test upload functionality
"""
import requests
import os

API_URL = "http://localhost:9000"

print("Testing API connection...")
try:
    response = requests.get(f"{API_URL}/")
    print(f"OK - API is running: {response.json()}")
except Exception as e:
    print(f"ERROR - Cannot connect to API: {e}")
    print("Make sure API is running on port 8080")
    exit(1)

print("\nTesting dataset listing...")
try:
    response = requests.get(f"{API_URL}/datasets/")
    print(f"OK - Found {len(response.json()['datasets'])} datasets")
    for ds in response.json()['datasets']:
        print(f"  - {ds['name']}: {ds['image_count']} images")
except Exception as e:
    print(f"ERROR: {e}")

print("\nTesting file upload...")
# Check if we have a test image
test_image_path = None
if os.path.exists("Dataset/glioma"):
    files = [f for f in os.listdir("Dataset/glioma") if f.endswith(('.jpg', '.jpeg', '.png'))]
    if files:
        test_image_path = os.path.join("Dataset/glioma", files[0])

if test_image_path and os.path.exists(test_image_path):
    try:
        with open(test_image_path, 'rb') as f:
            files = {'files': (os.path.basename(test_image_path), f, 'image/jpeg')}
            response = requests.post(f"{API_URL}/upload-dataset/?dataset_name=test_upload", files=files)
            if response.status_code == 200:
                print(f"OK - Upload successful: {response.json()['message']}")
            else:
                print(f"ERROR - Upload failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"ERROR - Upload exception: {e}")
else:
    print("SKIP - No test image found in Dataset/glioma/")

print("\n" + "="*50)
print("Test complete!")
