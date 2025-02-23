import os
import argparse
from google import genai
from google.genai import types
from PIL import Image

# Set your API key
os.environ["GOOGLE_API_KEY"] = "your_api_key_here"

def generate_coaching_prompt(client, activity, additional_info=""):
    """
    Generates a coaching prompt and determines the coaching tone
    based on the activity and any additional information provided.

    Args:
        client (genai.Client): The initialized GenAI client.
        activity (str): The name of the activity (e.g., "worm dance", "squat").
        additional_info (str, optional): Additional user information. Defaults to "".

    Returns:
        tuple: A tuple containing the generated prompt (str) and coaching tone (str).
    """
    prompt = (
        f"Create a coaching prompt for the activity: {activity}."
        f" Additional information: {additional_info}."
        " Provide the prompt and suggest an appropriate coaching tone."
    )

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[prompt],
            temperature=0.7,
            max_output_tokens=1024
        )
        generated_text = response.result
        # Placeholder parsing logic
        generated_prompt = generated_text
        coaching_tone = "helpful and direct"
        return generated_prompt, coaching_tone

    except Exception as e:
        print(f"Error generating coaching prompt: {e}")
        fallback_prompt = f"Analyze my {activity} and provide feedback that is helpful and direct."
        if additional_info:
            fallback_prompt += f" Consider the following: {additional_info}"
        return fallback_prompt, "helpful and direct"

def gemini_flash(client, instructional_videos, user_video, prompt, coaching_tone):
    """
    Processes instructional videos and a user video with Gemini 2.0 Flash
    to provide personalized coaching feedback.

    Args:
        client (genai.Client): The initialized GenAI client.
        instructional_videos (list): Paths to instructional video files.
        user_video (str): Path to the user's video file.
        prompt (str): The coaching prompt.
        coaching_tone (str): The desired coaching tone.

    Returns:
        str: Generated coaching feedback.
    """
    try:
        contents = [prompt, coaching_tone]
        for video_path in instructional_videos + [user_video]:
            with open(video_path, 'rb') as video_file:
                contents.append(video_file.read())

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=contents,
            temperature=0.7,
            max_output_tokens=1024
        )
        feedback = response.result
        return feedback

    except Exception as e:
        print(f"Error processing videos with Gemini 2.0 Flash: {e}")
        return "An error occurred while processing the videos. Please try again later."

def main():
    parser = argparse.ArgumentParser(
        description="Process instructional videos and a user video with Gemini 2.0 Flash to provide personalized coaching feedback."
    )
    parser.add_argument(
        "--instructional-dir",
        required=True,
        help="Directory containing instructional video files (e.g., .mp4, .avi, .mov, .mkv)"
    )
    parser.add_argument(
        "--user-video",
        required=True,
        help="Path to the user's video file to analyze."
    )
    parser.add_argument(
        "--activity",
        required=True,
        help="The name of the activity/exercise (e.g., 'worm dance', 'squat')."
    )
    parser.add_argument(
        "--additional-info",
        default="",
        help="Optional additional information (e.g., 'I have knee problems', 'I'm a beginner')."
    )

    args = parser.parse_args()

    instructional_videos = [
        os.path.join(args.instructional-dir, f)
        for f in os.listdir(args.instructional-dir)
        if f.lower().endswith(('.mp4', '.avi', '.mov', '.mkv'))
    ]

    client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])

    prompt, coaching_tone = generate_coaching_prompt(client, args.activity, args.additional_info)

    feedback = gemini_flash(client, instructional_videos, args.user_video, prompt, coaching_tone)

    print("Coaching feedback from Gemini 2.0 Flash:")
    print(feedback)

if __name__ == "__main__":
    main()
