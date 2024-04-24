# Video Creation Automation

This project automates the creation of a video by fetching content from the Reddit subreddit `AmItheAsshole`, generating speech from the text, speeding up the audio, editing a video file, adding subtitles, and exporting the final video with embedded subtitles.

## Prerequisites

Before running the script, make sure you have Python installed on your system. The script requires the following Python libraries:
- moviepy
- gTTS
- python-dotenv
- assemblyai
- pysrt
- pydub
- praw

You will also need to have FFmpeg installed, as it is used by `moviepy` for video processing.

## Installation

1. Clone the repository or download the source code.
2. Navigate to the directory containing the project files.
3. Create a virtual environment (optional but recommended):
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
4. Install the required Python libraries by running:
    pip install -r requirements.txt

## Configuration
- Rename .env.example to .env.
- Fill in the required API keys and other configuration settings in the .env file:
CLIENT_ID, CLIENT_SECRET, and USER_AGENT for Reddit API access.
ASSEMBLYAI_API_KEY for using AssemblyAI's transcription services.
- Both the AssemblyAI API and Reddit API are free, only requires account creation

## Usage
### Run the script with:
- python video_creator.py

### The script will:
1. Fetch the most recent post from the selected subreddit.
2. Generate speech from the post content using Google's Text-to-Speech service.
3. Edit the video by adjusting speed, applying a crop, and setting the audio.
4. Automatically generate subtitles and embed them into the video.
5. Export the final video to a specified directory.

### Output
The script saves the final video along with intermediate files in the generated directory. Ensure to check this directory for all generated content.
