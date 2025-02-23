import os
import argparse
import google.generativeai as genai
from anthropic import Anthropic
import time

from VideoRag.videorag._llm import *
from VideoRag.videorag import VideoRag, QueryParam

def generate_coaching_prompt_anthropic(activity, accommodations=""):
    """
    Generates a coaching prompt using Anthropics' Claude Haiku.
    This function only takes in the activity and accommodations.
    """
    # Build the prompt for Claude Haiku.
    prompt = f"Create a coaching prompt for the activity: {activity}."
    if accommodations:
        prompt += f" Consider the following accommodations: {accommodations}."
    prompt += " Provide a concise, clear coaching prompt."

    # Initialize the Anthropic client using your API key.
    anthropic_api_key = ""
    if not anthropic_api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set.")

    client = Anthropic(api_key=anthropic_api_key)

    try:
        # Updated message creation for Anthropics
        message = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1024,
            temperature=0.7,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        generated_prompt = message.content[0].text
        coaching_tone = "helpful and direct"
        return generated_prompt, coaching_tone
    except Exception as e:
        print(f"Error generating coaching prompt with Anthropics: {e}")
        fallback_prompt = f"Analyze my {activity} and provide feedback that is helpful and direct."
        if accommodations:
            fallback_prompt += f" Consider the following: {accommodations}"
        return fallback_prompt, "helpful and direct"
    
def generate_coaching_prompt(model, activity, additional_info="", anthropic_prompt=""):
    
    # Combine the Anthropics prompt with any additional info.
    combined_info = ""
    if anthropic_prompt:
        combined_info += f"Anthropic guidance: {anthropic_prompt}"
    if additional_info:
        if combined_info:
            combined_info += " | "
        combined_info += f"Additional info: {additional_info}"

    prompt = (
        f"Use the instructional video to help correct my {activity}. "
        f"Give feedback based on the user's attempt at the {activity}"
        f"Use specific information from the downloaded tutorial videos"
        f"Using the following guidance: {combined_info}. "
        "and how they could help me. Remember to be more gentle and take the perspective of a coach or personal trainer"
    )
    try:
        response = model.generate_content(
            contents=prompt,
            generation_config=genai.GenerationConfig(temperature=0.7, max_output_tokens=1024)
        )
        generated_text = response.text
        # Placeholder parsing logic; adjust as needed.
        generated_prompt = generated_text
        coaching_tone = "helpful and direct"
        return generated_prompt, coaching_tone
    except Exception as e:
        print(f"Error generating coaching prompt: {e}")
        fallback_prompt = f"Analyze my {activity} and provide feedback that is helpful and direct."
        if combined_info:
            fallback_prompt += f" Consider the following: {combined_info}"
        return fallback_prompt, "helpful and direct"

def gemini_flash(model, instructional_videos, user_video, prompt, coaching_tone):
    """Processes videos with Gemini 2.0 Flash for coaching feedback."""
    try:
        video_paths = []
        contents = [prompt, coaching_tone]
        for video_path in instructional_videos + [user_video]:
            video_paths.append(video_path)
            with open(video_path, 'rb') as video_file:
                contents.append({"mime_type": "video/mp4", "data": video_file.read()})

        videorag = VideoRAG(provider_in_use="gemini", working_dir=f"./videorag-workdir")
        videorag.insert_video(video_path_list=video_paths)

        query = prompt

        vrag_response = videorag.query(query=query, param=QueryParam(mode="videorag"))

        contents = [vrag_response + contents[0], contents[1]]

        response = model.generate_content(
            contents=contents,
            generation_config=genai.GenerationConfig(temperature=0.7, max_output_tokens=1024)
        )
        feedback = response.text
        return feedback
    except Exception as e:
        print(f"Error processing videos with Gemini 2.0 Flash: {e}")
        return "An error occurred while processing the videos. Please try again later."

def main():
    parser = argparse.ArgumentParser(description="Process videos with Gemini 2.0 Flash for coaching.")
    parser.add_argument("--instructional-dir", required=True, help="Instructional video directory.")
    parser.add_argument("--user-video", required=True, help="User video file.")
    parser.add_argument("--activity", required=True, help="Activity name.")
    parser.add_argument("--additional-info", default="", help="Optional info.")
    args = parser.parse_args()

    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    model = genai.GenerativeModel("gemini-2.0-flash") # or gemini-1.5-pro, or gemini-pro-vision depending on your needs.

    instructional_videos = [
        os.path.join(args.instructional_dir, f)
        for f in os.listdir(args.instructional_dir)
        if f.lower().endswith(('.mp4', '.avi', '.mov', '.mkv'))
    ]
    
    # Generate a prompt using Anthropics
    anthropic_prompt, anthropic_tone = generate_coaching_prompt_anthropic(args.activity, args.additional_info)
    # Use the Anthropics prompt as guidance when generating the Gemini coaching prompt.
    prompt, coaching_tone = generate_coaching_prompt(model, args.activity, additional_info=args.additional_info, anthropic_prompt=anthropic_prompt)
    
    feedback = gemini_flash(model, instructional_videos, args.user_video, prompt, coaching_tone)
    print("Coaching feedback from Gemini:")
    print(feedback)

if __name__ == "__main__":
    main()
