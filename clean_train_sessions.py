import os
import shutil

train_session_folders = ["models/train_sessions/", "logs/train_sessions/"]
for folder in train_session_folders:
    for contents in os.listdir(folder):
        shutil.rmtree(folder + contents)
