import os
import time
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Set the environment variable to the path of your service account key file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "GOOGLE_APPLICATION_CREDENTIALS"

# Load the API key from the environment variables
api_key = os.getenv("GOGGLE_API_KEY")
genai.configure(api_key=api_key)

MEDIA_FOLDER = "media"

def save_uploaded_file(file_path, file_data):
    """Save the uploaded file to the media folder and return the file path."""
    if not os.path.exists(MEDIA_FOLDER):
        os.makedirs(MEDIA_FOLDER)
    with open(file_path, 'wb') as f:
        f.write(file_data)
    return file_path

def get_insights(video_path):
    """Extract insights from the video using Gemini Flash."""
    print(f"Processing video: {video_path}")

    print("Uploading file...")
    video_file = genai.upload_file(path=video_path)
    print(f"Completed upload: {video_file.uri}")

    print('Waiting for video to be processed...')
    while video_file.state.name == "PROCESSING":
        time.sleep(10)
        video_file = genai.get_file(video_file.name)

    if video_file.state.name == "FAILED":
        print("Video processing failed.")
        raise ValueError(video_file.state.name)

    prompt = "Only include the narration. This is a cricket video. Create a short voiceover script in the style of a sports commentator and make it slightly emotional."

    model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

    print("Making LLM inference request...")
    response = model.generate_content([prompt, video_file],
                                      request_options={"timeout": 600})

    print("Video processing complete.")
    print("Insights:")
    print(response.text)

    genai.delete_file(video_file.name)
    # Optionally, delete the video file after processing
    os.remove(video_path)

def main():
    # Example usage: Replace 'video_file.mp4' with your actual file path
    video_file_path = 'C:/trial/veio/media/videoplayback.mp4'
    
    # Assuming the video file is already available, otherwise, you would load it here
    with open(video_file_path, 'rb') as f:
        file_data = f.read()

    file_path = save_uploaded_file(video_file_path, file_data)
    get_insights(file_path)


if __name__ == "__main__":
    main()