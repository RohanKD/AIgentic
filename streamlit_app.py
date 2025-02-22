import streamlit as st
import time

# Optional: Set page layout and initial configurations
st.set_page_config(
    page_title="Sports & Music Performance Analyzer",
    layout="wide",
)

def main():
    st.title("Performance Analyzer for Sports and Music")
    st.write(
        "Upload a video of your sports performance or music practice, "
        "and receive personalized feedback on technique and form."
    )

    # Create two tabs: one for sports, one for music
    sports_tab, music_tab = st.tabs(["Sports", "Music"])

    with sports_tab:
        show_sports_analysis_ui()

    with music_tab:
        show_music_analysis_ui()


def show_sports_analysis_ui():
    st.header("Sports Performance Analysis")

    # Let the user pick from a dropdown OR type in a sport
    st.subheader("1. Select or Enter Your Sport")
    sport_options = ["Tennis", "Badminton", "Swimming", "Weightlifting", "Other"]
    chosen_sport = st.selectbox("Sport:", sport_options, index=0)
    
    # If user picks "Other," show a text input
    if chosen_sport == "Other":
        custom_sport = st.text_input("Enter your sport:")
        if custom_sport:
            chosen_sport = custom_sport  # override

    # File uploader
    st.subheader("2. Upload Your Sports Video")
    uploaded_file_sport = st.file_uploader(
        f"Upload a short clip of your {chosen_sport} performance",
        type=["mp4", "mov", "avi", "mkv"],
        key="sports_upload"
    )

    if uploaded_file_sport:
        st.video(uploaded_file_sport)

    # Analyze button
    if st.button("Analyze Sports Performance", key="sports_analyze"):
        if not uploaded_file_sport:
            st.warning("Please upload a sports video before analyzing.")
        else:
            with st.spinner("Analyzing sports performance..."):
                time.sleep(3)  # Simulate processing

                # Placeholder results
                sports_analysis = {
                    "activity": chosen_sport,
                    "overall_score": 85,
                    "main_issues": [
                        {"label": "Footwork", "description": "Feet too close together during pivot."},
                        {"label": "Shoulder Rotation", "description": "Limited rotation reducing power."}
                    ],
                    "recommendations": [
                        "Keep your feet a bit wider for better balance.",
                        "Focus on rotating your shoulders more on the follow-through."
                    ],
                    "reference_clips": [
                        {
                            "title": "Pro Example: Ideal Footwork",
                            "url": "https://youtu.be/dummy-footwork"
                        },
                        {
                            "title": "Increasing Shoulder Rotation",
                            "url": "https://youtu.be/dummy-shoulders"
                        }
                    ]
                }

            st.success("Sports analysis complete!")
            display_analysis_results(sports_analysis)


def show_music_analysis_ui():
    st.header("Music Performance Analysis")

    # Let the user pick from a dropdown or type in an instrument/activity
    st.subheader("1. Select or Enter Your Instrument")
    instrument_options = ["Guitar", "Piano", "Violin", "Drums", "Other"]
    chosen_instrument = st.selectbox("Instrument:", instrument_options, index=0)

    # If user picks "Other," show a text input
    if chosen_instrument == "Other":
        custom_instrument = st.text_input("Enter your instrument:")
        if custom_instrument:
            chosen_instrument = custom_instrument  # override

    st.subheader("2. Upload Your Music Performance Video")
    uploaded_file_music = st.file_uploader(
        f"Upload a short clip of your {chosen_instrument} performance",
        type=["mp4", "mov", "avi", "mkv"],
        key="music_upload"
    )

    if uploaded_file_music:
        st.video(uploaded_file_music)

    # Analyze button
    if st.button("Analyze Music Performance", key="music_analyze"):
        if not uploaded_file_music:
            st.warning("Please upload a music performance video before analyzing.")
        else:
            with st.spinner("Analyzing music performance..."):
                time.sleep(3)  # Simulate processing

                # Placeholder results
                music_analysis = {
                    "activity": chosen_instrument,
                    "overall_score": 90,
                    "main_issues": [
                        {"label": "Posture", "description": "Back is slouched while seated."},
                        {"label": "Hand Position", "description": "Wrist too bent, causing tension."}
                    ],
                    "recommendations": [
                        "Keep your back straight and relaxed for better breathing/control.",
                        "Try maintaining a neutral wrist angle to reduce strain."
                    ],
                    "reference_clips": [
                        {
                            "title": "Proper Seated Posture",
                            "url": "https://youtu.be/dummy-posture"
                        },
                        {
                            "title": "Correct Wrist Technique",
                            "url": "https://youtu.be/dummy-wrist"
                        }
                    ]
                }

            st.success("Music analysis complete!")
            display_analysis_results(music_analysis)


def display_analysis_results(results):
    """
    Displays analysis results in a user-friendly format.
    This function is reused for both sports and music tabs.
    """
    st.subheader("Analysis Results")

    activity_name = results.get("activity", "your activity")
    overall_score = results.get("overall_score", None)
    main_issues = results.get("main_issues", [])
    recommendations = results.get("recommendations", [])
    reference_clips = results.get("reference_clips", [])

    # Show the activity
    st.write(f"**Activity Analyzed:** {activity_name}")

    # Show overall score
    if overall_score is not None:
        st.metric(label="Overall Form Score", value=f"{overall_score}/100")

    # Show key issues
    if main_issues:
        st.write("### Key Issues Found:")
        for issue in main_issues:
            st.markdown(f"- **{issue['label']}**: {issue['description']}")

    # Show recommendations
    if recommendations:
        st.write("### Recommendations:")
        for rec in recommendations:
            st.markdown(f"- {rec}")

    # Show reference clips
    if reference_clips:
        st.write("### Suggested Reference Clips:")
        for clip in reference_clips:
            st.markdown(f"- **{clip['title']}**: [Watch here]({clip['url']})")

    st.write("---")
    st.write("Feel free to upload another video to track improvements!")


if __name__ == "__main__":
    main()
