import os
import logging
import warnings
import multiprocessing
from dotenv import load_dotenv

warnings.filterwarnings("ignore")
logging.getLogger("httpx").setLevel(logging.WARNING)

# Please enter your openai key
#os.environ["OPENAI_API_KEY"] = ""
load_dotenv()
print("loaded API Key")
from videorag._llm import *
from videorag import VideoRAG, QueryParam


if __name__ == '__main__':
    multiprocessing.set_start_method('spawn')

    # Please enter your video file path in this list; there is no limit on the length.
    # Here is an example; you can use your own videos instead.
    

    video_paths = [
        "video_db/How to Do the Worm ｜ B-Boying.mp4",
        "video_db/How to Do the Worm.mkv",
    ]
    videorag = VideoRAG(provider_in_use="gemini", working_dir=f"./videorag-workdir")
    videorag.insert_video(video_path_list=video_paths)
    
    print("Indexed Videos")

    #multiprocessing.set_start_method('spawn')

    query = 'How do I do the worm?'
    
    print("************************************************************************************")
    print(f"Query: \n{query}")
    print("************************************************************************************")
    
    param = QueryParam(mode="videorag")
    # if param.wo_reference = False, VideoRAG will add reference to video clips in the response
    param.wo_reference = False

    # videorag = VideoRAG(provider_in_use="openai", working_dir=f"./videorag-workdir")
    videorag.load_caption_model(debug=True)
    response = videorag.query(query=query, param=param)

    print("************************************************************************************")
    print(f"Response: \n{response}")
    print("************************************************************************************")
