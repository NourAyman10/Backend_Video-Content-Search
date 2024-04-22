from helper_functions import generate_input_dataset
from helper_functions import pull_kaggle_dataset
from helper_functions import update_kaggle_dataset
from helper_functions import pull_kaggle_notebook
from helper_functions import push_kaggle_notebook
from helper_functions import get_notebook_status
from helper_functions import get_notebook_output
from helper_functions import get_timestamps
from helper_drive.helper_drive import get_preview_link

from flask import Flask, request

output_preview = "C:/Users/noura/OneDrive/Desktop/GP-Project/Backend-Video-Content-Search/video/output/output_video.mp4"

# for audio
audio_project_path = "C:/Users/noura/OneDrive/Desktop/GP-Project/Backend-Video-Content-Search/audio"
audio_nb_id = "nourayman10102002/asr-fastwhisper-deployment"

# for video
video_project_path = "C:/Users/noura/OneDrive/Desktop/GP-Project/Backend-Video-Content-Search-Backend/video"
video_nb_id = "ruqaiyahmohammed/refvos-deployment"

app = Flask(__name__)


@app.route("/vos", methods=["POST"])
def vos():
    data = request.get_json()
    videoLink = data["videoLink"]
    textQuery = data["textQuery"]
    searchStatus = data["searchStatus"]
    notebookStatusComplete = ""
    videoPreviewLink = ""
    timestamps = []

    if searchStatus == 'audio':
        pull_kaggle_dataset(audio_project_path)
        generate_input_dataset(videoLink, textQuery, "audio")
        update_kaggle_dataset(audio_project_path)
        pull_kaggle_notebook(audio_project_path, audio_nb_id)
        push_kaggle_notebook(audio_project_path)
        while(str(get_notebook_status(audio_nb_id)).__contains__("running")):
            print("loading...")
        print(str(get_notebook_status(audio_nb_id)).__contains__("complete"))
        notebookStatusComplete = str(get_notebook_status(audio_nb_id)).__contains__("complete")
        get_notebook_output(audio_project_path, audio_nb_id)
        videoPreviewLink = videoLink
        timestamps = get_timestamps()
        
        
    elif searchStatus == 'video':
        pull_kaggle_dataset(video_project_path)
        generate_input_dataset(videoLink, textQuery,"video")
        update_kaggle_dataset(video_project_path)
        pull_kaggle_notebook(video_project_path, video_nb_id)
        push_kaggle_notebook(video_project_path)
        while(str(get_notebook_status(video_nb_id)).__contains__("running")):
            print("loading...")
        print(str(get_notebook_status(video_nb_id)).__contains__("complete"))
        notebookStatusComplete = str(get_notebook_status(video_nb_id)).__contains__("complete")
        get_notebook_output(video_project_path, video_nb_id)
        
        preview_link = get_preview_link(output_preview)
        videoPreviewLink = preview_link
        
        timestamps = []

        

    response = {
        "message": "Text received and processed successfully",
        "videoLink": videoLink,
        "textQuery": textQuery,
        "searchStatus": searchStatus,
        "notebookStatusComplete": notebookStatusComplete,
        "videoPreviewLink": videoPreviewLink,
        "timestamps": timestamps,
    }

    return response


if __name__ == "__main__":
    app.run(debug=True)
