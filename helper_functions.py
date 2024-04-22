import subprocess
import json


def generate_input_dataset(video_link, query, type):
    api = {"link": video_link, "query": query}
    json_object = json.dumps(api, indent=4)
    with open(type + "/input/video_link.json", "w") as outfile:
        outfile.write(json_object)
        

def time_string_to_seconds(time_str):
    parts = time_str.split(':')
    hours = int(parts[0])
    minutes = int(parts[1])
    
    seconds_parts = parts[2].split('.')
    seconds = int(seconds_parts[0])
    milliseconds = int(seconds_parts[1]) if len(seconds_parts) > 1 else 0
    
    # Calculate total seconds
    total_seconds = (hours * 3600) + (minutes * 60) + seconds + (milliseconds / 1000)
    
    return int(total_seconds)


def get_timestamps():
    f = open('./audio/output/start_timestamps.json')
    data = json.load(f)
    timestamps = data['timestamps']
    f.close()
    # return timestamps
    return list(map(lambda x: time_string_to_seconds(x), timestamps))

# kaggle api


def execute_terminal_command(command):
    result = subprocess.run(command, shell=True, capture_output=True)
    return result.stdout


def pull_kaggle_dataset(project_path):
    str_command = (
        "kaggle datasets metadata -p "
        + project_path.replace("/", "\\")
        + "\input nourayman10102002/youtube-links"
    )
    command = rf"{str_command}"
    return execute_terminal_command(command)


def update_kaggle_dataset(project_path):
    str_command = (
        "kaggle datasets version -p "
        + project_path.replace("/", "\\")
        + '\input -m "Updated dataset using kaggle API" -r tar'
    )
    command = rf"{str_command}"
    return execute_terminal_command(command)


def pull_kaggle_notebook(project_path, nb_id):
    command = rf"kaggle kernels pull {nb_id} -p {project_path}/notebook -m"
    return execute_terminal_command(command)


def push_kaggle_notebook(project_path):
    command = rf"kaggle kernels push -p {project_path}/notebook"
    return execute_terminal_command(command)


def get_notebook_status(nb_id):
    command = rf"kaggle kernels status {nb_id}"
    return execute_terminal_command(command)


def get_notebook_output(project_path, nb_id):
    command = rf"kaggle kernels output {nb_id} -p {project_path}/output"
    return execute_terminal_command(command)

