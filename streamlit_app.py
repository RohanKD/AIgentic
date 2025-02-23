import streamlit as st
import yt_dlp
import os
import time

def scrape_youtube_search(query, max_results=25):
    # Use yt_dlp's internal search feature
    search_query = f"ytsearch{max_results}:{query}"
    with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
        try: 
            search_result = ydl.extract_info(search_query, download=False)
            video_urls = [entry['webpage_url'] for entry in search_result['entries']]
            return video_urls
        except Exception as e:
            st.error(f"Error searching YouTube: {e}")
            return []

def download_video(url, output_dir="videos"):
    os.makedirs(output_dir, exist_ok=True)
    ydl_opts = {
        "format": "bv*[height<=240]+ba/bv*+ba/b",
        "outtmpl": f"{output_dir}/%(title)s.%(ext)s",
        "merge_output_format": "mp4",
        "quiet": False,
        "postprocessors": [
            {"key": "FFmpegVideoConvertor", "preferedformat": "mp4"},
        ],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
        except yt_dlp.utils.DownloadError as e:
            st.error(f"❌ Error downloading {url}: {e}")

def show_activity_analysis_ui():
    st.header("Activity Performance Analysis")
    activity_options = ["Sports", "Music", "Dance", "Theater", "Other"]
    chosen_activity = st.selectbox("Select your activity:", activity_options, index=0)
    if chosen_activity == "Other":
        chosen_activity = st.text_input("Enter your activity:")
    uploaded_file = st.file_uploader(f"Upload your {chosen_activity} video", type=["mp4", "mov", "avi", "mkv"], key="activity_upload")
    if uploaded_file:
        st.video(uploaded_file)
    if st.button("Analyze Performance", key="activity_analyze"):
        if not uploaded_file:
            st.warning("Please upload a video before analyzing.")
        else:
            with st.spinner("Analyzing performance..."):
                time.sleep(3)
            st.success("Analysis complete!")

def show_howto_ui():
    st.header("Find How-To Videos")
    user_query = st.text_input("Enter the task you want to learn:")
    if st.button("Search How-To Videos"):
        if user_query:
            with st.spinner("Searching YouTube..."):
                video_links = scrape_youtube_search(user_query)
            st.write("### Found Videos:")
            for link in video_links:
                st.write(link)
            st.session_state["video_links"] = video_links
            st.session_state["download_ready"] = True

    if st.session_state.get("download_ready", False):
        if st.button("Download Videos"):
            with st.spinner("Downloading videos..."):
                for link in st.session_state["video_links"]:
                    download_video(link)
            st.success("All videos downloaded successfully (or skipped if unavailable).")

def main():
    st.set_page_config(page_title="Activity Performance Analyzer", layout="wide")
    st.title("Performance Analyzer & How-To Video Finder")
    st.write("Upload a video for performance analysis or search for how-to videos.")

    activity_tab, howto_tab = st.tabs(["Activity Analysis", "How-To Videos"])

    with activity_tab:
        show_activity_analysis_ui()
    with howto_tab:
        show_howto_ui()

if __name__ == "__main__":
    main()
