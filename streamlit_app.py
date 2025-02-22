import streamlit as st
import time

# Set page configuration as the first Streamlit command
st.set_page_config(
    page_title="Activity Performance Analyzer",
    layout="wide",
)

# Optional: Add some custom CSS for improved styling
st.markdown(
    """
    <style>
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
    }
    .header {
        font-size: 2.5em;
        font-weight: bold;
        margin-bottom: 0.5em;
    }
    .subheader {
        font-size: 1.5em;
        margin-top: 1em;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def main():
    st.markdown("<div class='header'>Activity Performance Analyzer</div>", unsafe_allow_html=True)
    st.write(
        "Upload a video of your performance in any activity, and receive personalized feedback on your technique and form."
    )
    st.markdown("---")
    show_activity_analysis_ui()

def show_activity_analysis_ui():
    st.markdown("<div class='subheader'>Step 1: Select or Enter Your Activity</div>", unsafe_allow_html=True)
    activity_options = ["Sports", "Music", "Dance", "Theater", "Other"]
    chosen_activity = st.selectbox("Activity Type:", activity_options)
    
    if chosen_activity == "Other":
        custom_activity = st.text_input("Enter your activity:")
        if custom_activity:
            chosen_activity = custom_activity

    st.markdown("---")
    st.markdown("<div class='subheader'>Step 2: Upload Your Performance Video</div>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        f"Upload a short clip of your {chosen_activity} performance",
        type=["mp4", "mov", "avi", "mkv"]
    )

    if uploaded_file:
        st.video(uploaded_file)

    st.markdown("---")
    if st.button("Analyze Performance"):
        if not uploaded_file:
            st.warning("Please upload a video before analyzing.")
        else:
            with st.spinner("Analyzing performance..."):
                time.sleep(3)  # Simulate processing time

                # Placeholder analysis results
                analysis_results = {
                    "activity": chosen_activity,
                    "overall_score": 88,
                    "main_issues": [
                        {"label": "Technique", "description": "Minor inconsistencies in movement execution."},
                        {"label": "Timing", "description": "Slight delays in transition phases."}
                    ],
                    "recommendations": [
                        "Focus on maintaining consistency throughout your performance.",
                        "Work on smoother transitions between segments."
                    ],
                    "reference_clips": [
                        {
                            "title": "Technique Mastery Example",
                            "url": "https://youtu.be/dummy-technique"
                        },
                        {
                            "title": "Timing and Rhythm Guidance",
                            "url": "https://youtu.be/dummy-timing"
                        }
                    ]
                }
            st.success("Analysis complete!")
            display_analysis_results(analysis_results)

def display_analysis_results(results):
    st.markdown("<div class='subheader'>Analysis Results</div>", unsafe_allow_html=True)
    activity_name = results.get("activity", "Your activity")
    overall_score = results.get("overall_score", None)
    main_issues = results.get("main_issues", [])
    recommendations = results.get("recommendations", [])
    reference_clips = results.get("reference_clips", [])

    st.write(f"**Activity Analyzed:** {activity_name}")

    if overall_score is not None:
        st.metric(label="Overall Performance Score", value=f"{overall_score}/100")

    if main_issues:
        st.write("### Key Issues Identified:")
        for issue in main_issues:
            st.markdown(f"- **{issue['label']}**: {issue['description']}")

    if recommendations:
        st.write("### Recommendations:")
        for rec in recommendations:
            st.markdown(f"- {rec}")

    if reference_clips:
        st.write("### Reference Clips:")
        for clip in reference_clips:
            st.markdown(f"- **{clip['title']}**: [Watch here]({clip['url']})")

    st.markdown("---")
    st.write("Feel free to upload another video to track your progress!")

if __name__ == "__main__":
    main()
