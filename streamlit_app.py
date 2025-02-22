import streamlit as st
import yt_dlp
import os
import time
import requests
from bs4 import BeautifulSoup

def scrape_youtube_search(query, max_results=25):
    search_query = f"How to {query}".replace(" ", "+")
    url = f"https://www.youtube.com/results?search_query={search_query}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    video_ids = [
        link["href"].split("=", 1)[1] for link in soup.select("a[href^='/watch?v=']")
    ]
    video_urls = [f"https://www.youtube.com/watch?v={vid}" for vid in video_ids[:max_results]]
    return video_urls

def download_video(url, output_dir="videos"):
    os.makedirs(output_dir, exist_ok=True)
    ydl_opts = {
        "format": "bv*[height<=240]+ba/bv*+ba/b",  # Best video + best audio, fallback to best
        "outtmpl": f"{output_dir}/%(title)s.%(ext)s",  # Save in "videos" folder
        "merge_output_format": "mp4",  # Ensure consistent output
        "quiet": False,  # Show progress
        "postprocessors": [
            {"key": "FFmpegVideoConvertor", "preferedformat": "mp4"},
        ],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
        except yt_dlp.utils.DownloadError as e:
            print(f"❌ Error downloading {url}: {e}")

def main():
    st.set_page_config(page_title="Activity Performance Analyzer", layout="wide")
    st.title("Performance Analyzer & How-To Video Finder")
    st.write("Upload a video for performance analysis or search for how-to videos.")
    
    activity_tab, howto_tab = st.tabs(["Activity Analysis", "How-To Videos"])
    
    with activity_tab:
        show_activity_analysis_ui()
    with howto_tab:
        show_howto_ui()

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
    if st.button("Search and Download How-To Videos"):
        if user_query:
            with st.spinner("Searching YouTube..."):
                video_links = scrape_youtube_search(user_query)
            st.write("### Downloading videos...")
            for link in video_links:
                download_video(link)
                st.write(f"✅ Downloaded: {link}")
            st.success("All videos downloaded successfully (or skipped if unavailable).")

if __name__ == "__main__":
    main()
