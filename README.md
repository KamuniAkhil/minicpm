# FastAPI Image Processing and Question Answering with MiniCPM Model

This project provides a FastAPI server for processing images and answering questions about them using the `openbmb/MiniCPM-V-2_6-int4` model.

## Requirements

Make sure you have Python 3.8 or higher installed on your machine. You will also need to install the required packages listed in `requirements.txt`.

## Installation

1. Clone this repository or download the files to your local machine.
2. Navigate to the project directory in your terminal or command prompt.
3. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   ```
4. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
5. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Server

1. Navigate to the directory where `server.py` is located.
2. Run the server:
   ```bash
   python server.py
   ```
3. The server will start running at `http://192.168.0.233:5000`.

## Running the Client

1. Open another terminal or command prompt window.
2. Navigate to the directory where `client.py` is located.
3. Ensure that you have an image file named `download.jpeg` in the same directory or update the `image_path` variable in `client.py` to point to your desired image.
4. Run the client:
   ```bash
   streamlit run client.py
   ```
5. The client will send the image and question to the server and print the streamed response.

## Example Usage

You can replace the `image_path` and `question` variables in `client.py` with any image file and question of your choice to test the application.

## Notes

- Ensure that the server is running before starting the client.
- Adjust the server IP and port in `client.py` if you're running the server on a different machine or port.
