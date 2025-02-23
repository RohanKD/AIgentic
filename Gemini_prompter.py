import os
import google.generativeai as genai
from anthropic import Anthropic


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

    # Initialize the Anthropics client using your API key.
    client = Anthropic(
        api_key=""
    )

    try:
        # Updated message creation for Anthropic
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
        print(generated_prompt)
        return generated_prompt, coaching_tone
    except Exception as e:
        print(f"Error generating coaching prompt with Anthropics: {e}")
        fallback_prompt = f"Analyze my {activity} and provide feedback that is helpful and direct."
        if accommodations:
            fallback_prompt += f" Consider the following: {accommodations}"
        return fallback_prompt, "helpful and direct"


def gemini_flash(model, instructional_videos, user_video, prompt, coaching_tone):
    """Processes videos with Gemini 2.0 Flash for coaching feedback."""
    try:
        # Upload files using the File API
        contents = [prompt, coaching_tone]

        # Upload and process instructional videos
        for video_path in instructional_videos:
            video_file = genai.upload_file(video_path)
            contents.append(video_file)

        # Upload and process user video
        user_video_file = genai.upload_file(user_video)
        contents.append(user_video_file)

        response = model.generate_content(
            contents=contents,
            generation_config=genai.GenerationConfig(
                temperature=0.7,
                max_output_tokens=1024
            )
        )
        feedback = response.text
        return feedback
    except Exception as e:
        print(f"Error processing videos with Gemini 2.0 Flash: {e}")
        return "An error occurred while processing the videos. Please try again later."


def main():
    # Instead of command line arguments, prompt the user for input.
    instructional_dir = "/Users/rohan/PycharmProjects/DoAI/VideoRAG/videos"
    user_video = "/Users/rohan/Downloads/20250222_205205.mp4"
    activity = "Self defense"
    accommodations = "Torn ACL"

    # Configure the Gemini model
    genai.configure(api_key="")
    model = genai.GenerativeModel("gemini-2.0-flash")  # Changed to pro-vision model

    # Get list of instructional videos
    instructional_videos = [
        os.path.join(instructional_dir, f)
        for f in os.listdir(instructional_dir)
        if f.lower().endswith(('.mp4', '.avi', '.mov', '.mkv'))
    ]

    # Generate the coaching prompt using Anthropics' Claude Haiku.
    prompt, coaching_tone = generate_coaching_prompt_anthropic(activity, accommodations)

    # Send the generated prompt and videos to Gemini for coaching feedback.
    feedback = gemini_flash(model, instructional_videos, user_video, prompt, coaching_tone)

    print("Coaching feedback from Gemini:")
    print(feedback)


if __name__ == "__main__":
    main()
