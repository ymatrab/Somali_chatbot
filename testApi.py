import requests

# Base URL of the API
base_url = "http://127.0.0.1:8000"

def test_ocr_api(user_id,image_links):
    payload = {
        "image_link": image_links,
        "user_id": user_id
    }
    response = requests.post(f"{base_url}/ocr/", json=payload)
    print("OCR API Response:", response.json())

def test_chat_api(text, image_links, user_id, conversation_id):
    payload = {
        "text": text,
        "image_link": image_links,
        "user_id": user_id,
        "conversation_id": conversation_id
    }

    # Make the POST request
    response = requests.post(f"{base_url}/chat", json=payload)

    # Print the response
    print("Chat API Response:", response.json())

def test_chat_with_image_api(text, image_links, user_id, conversation_id):
    # Prepare the payload
    payload = {
        "text": text,
        "image_link": image_links,
        "user_id": user_id,
        "conversation_id": conversation_id
    }

    # Make the POST request
    response = requests.post(f"{base_url}/chat_with_image", json=payload)

    # Print the response
    print("Chat with Image API Response:", response.json())

file= "https://veranomedical.com/4982/calcium-500-mg-vitamine-d3-sans-sucre-30-comprimes.jpg"
file2="https://firebasestorage.googleapis.com/v0/b/med-assistant-296af.appspot.com/o/users%2FkYDlYuqRLOYM7UkFdSdPVLOk47A3%2Fuploads%2F1721318469567772.jpg?alt=media&token=c9c21472-9dd5-48f6-884e-884e06a766c8"
files=[file,file2]

text = "describe the following image"
user_id='kYDlYuqRLOYM7UkFdSdPVLOk47A3'
conversation_id='2TdtrmLK4wXdCa2SEWjr'

# Test the APIs
test_ocr_api(user_id,files)
test_chat_api(text, files, user_id, conversation_id)
#test_chat_with_image_api(text, files, user_id, conversation_id)
