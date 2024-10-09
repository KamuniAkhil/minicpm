import streamlit as st
import requests
 
# Streamlit App Title
st.title("Image and Question Analyzer")
 
# Upload image
uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
 
# Enter a question using a text area
question = st.text_area("Enter your question:", height=100)
 
# Button to submit the request
if st.button("Submit"):
 
    if uploaded_image is not None and question != "":
        # Display the image on the Streamlit app
        st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)
 
        # Prepare the files and data for the POST request
        files = {'image': uploaded_image.getvalue()}  # Send image as bytes
        data = {'question': question}
 
        # Server URL (replace with your server's actual URL)
        server_url = 'http://127.0.0.1:5000/ask'
 
        # Send the request to the server
        response = requests.post(server_url, files={'image': uploaded_image}, data=data, stream=True)
 
        # Check if the response was successful
        if response.status_code == 200:
            st.write("Response (streaming):")
           
            result = ""  # Initialize an empty string to accumulate and display chunks progressively
            previous_chunk = ""  # To store previously printed chunks and avoid duplication
           
            # Create a Streamlit placeholder to update the result progressively
            result_placeholder = st.empty()
 
            # Process the streaming response
            for chunk in response.iter_content(decode_unicode=True):
                if chunk:
                    # Check if the chunk is new and not repeated
                    if chunk != previous_chunk:
                        result += chunk  # Accumulate new chunks
                        result_placeholder.text_area("Result", result, height=200)  # Update the result dynamically
                        previous_chunk = chunk  # Update the previous chunk to avoid reprinting
 
        else:
            st.error(f"Failed to get a response from the server: {response.status_code}")
    else:
        st.warning("Please upload an image and enter a question.")
 