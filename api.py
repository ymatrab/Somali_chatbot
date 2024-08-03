from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from typing import Optional,Union, List
import os
from gpt_vision import gpt_ocr, get_output,chat_with_image

app = FastAPI()

class ChatInput(BaseModel):
    text: Optional[str] = None
    image_link: Optional[Union[str, List[str]]] = None
    user_id: str
    conversation_id: str

class OCRInput(BaseModel):
    image_link: Union[str, List[str]]
    user_id: str

if not os.path.exists('temp_files'):
    os.makedirs('temp_files')

from fastapi.responses import JSONResponse

@app.post("/ocr/")
async def ocr_from_url(input: OCRInput):
    image_link = input.image_link
    user_id = input.user_id
    result = gpt_ocr(user_id,image_link)
    return JSONResponse(content={"text": result})

@app.post("/chat")
async def chat(input: ChatInput):
    if input.image_link:
        result = get_output(input.text, input.user_id, input.conversation_id,input.image_link)
        return {"response": result}
    if input.text:
        # Generate response using the combined input
        result = get_output(input.text, input.user_id, input.conversation_id)
        return {"response": result}
    else:
        return {"response": "No text provided"}

@app.post("/chat_with_image")
async def chat_with_images_endpoint(input: ChatInput):
    if input.image_link:
        result = chat_with_image(input.text, input.user_id, input.image_link)
        return {"response": result}

    else:
        return {"response": "No images provided"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
