import requests
 
# URL of the server (replace with your actual server's IP or hostname)
server_url = 'http://192.168.0.233:5000/ask'
 
# The image to send
image_path = 'download.jpeg'
 
# The question to ask
question = 'Describe this image in detail?'
 
# Re-open the image and send it as part of a POST request with streaming
with open(image_path, 'rb') as img_file:
    files = {'image': img_file}
    data = {'question': question}
    # Send the POST request to the server
    response = requests.post(server_url, files=files, data=data, stream=True)
 
    # Check if the request was successful
    if response.status_code == 200:
        print("Streaming response:")
 
        # Initialize an empty string to accumulate and print chunks progressively
        previous_chunk = ""  # To store previously printed chunks and avoid duplication
 
        # Process the stream as it arrives
        for chunk in response.iter_content(decode_unicode=True):
            if chunk:
                # Check if the chunk is new and not repeated
                if chunk != previous_chunk:
                    print(chunk, end="", flush=True)  # Print the new chunk
                    previous_chunk = chunk  # Update the previous chunk to avoid reprinting
 
        print("\nDone!")  # Ensure there's a final newline at the end
 
    else:
        print(f"Failed to get response: {response.status_code}")