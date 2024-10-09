import torch
from PIL import Image
from transformers import AutoModel, AutoTokenizer
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import StreamingResponse
import os
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
import asyncio

app = FastAPI()

# Load the new model and tokenizer
model = AutoModel.from_pretrained('openbmb/MiniCPM-V-2_6-int4', trust_remote_code=True)
model = model.to(device='cuda')
tokenizer = AutoTokenizer.from_pretrained('openbmb/MiniCPM-V-2_6-int4', trust_remote_code=True)
model.eval()

# Initialize a ThreadPoolExecutor for parallel processing
executor = ThreadPoolExecutor(max_workers=50)  # Adjust max_workers based on hardware capacity

# Function to process image and question and stream response with intelligent buffering
def process_image_and_question_stream(image_path: str, question: str):
    try:
        # Load the image
        image = Image.open(image_path).convert('RGB')

        # Example question (you could pass the real question from the client here)
        question = "What is the object in the image?"

        # Prepare the message
        msgs = [{'role': 'user', 'content': [image, question]}]

        # Stream model response
        res = model.chat(
            image=None,
            msgs=msgs,
            tokenizer=tokenizer,
            sampling=True,
            temperature=0.7,
            stream=True
        )

        # Accumulate text to avoid sending too small chunks
        buffer = ""
        min_chunk_size = 20  # Minimum chunk size to send (adjust as needed)
        for new_text in res:
            buffer += new_text  # Accumulate new text in the buffer
            
            # Only send the chunk if it's larger than the minimum chunk size or ends with a period
            if len(buffer) > min_chunk_size or buffer.endswith("."):
                # Print the chunk for debugging purposes
                print(f"Sending chunk: {buffer}")
                yield buffer
                buffer = ""  # Clear the buffer after sending the chunk

            time.sleep(0.05)  # Optional delay to simulate real-time typing (can be removed)

        # Send any remaining text in the buffer after the loop
        if buffer:
            print(f"Sending remaining chunk: {buffer}")
            yield buffer

    except Exception as e:
        yield f"Error: {str(e)}\n"

@app.post("/ask")
async def ask(
    image: UploadFile = File(...),
    question: str = Form(...)
):
    # Save the image temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
        image_path = temp_file.name
        temp_file.write(await image.read())

    # Submit the blocking task to the executor for parallel processing
    loop = asyncio.get_running_loop()
    response_generator = await loop.run_in_executor(
        executor, process_image_and_question_stream, image_path, question
    )

    # Return the StreamingResponse to stream the response back to the client
    return StreamingResponse(response_generator, media_type="text/plain")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, port=5000)