import os
import json


def rename_file(cwd=os.getcwd()):
    """
    Renames the arbitrary .json file name to a generic format
    after the vod chat has been downloaded via TwitchDownloader.

    Keyword Arguments:
        cwd - A string representing the current working directory.
    """
    for file in os.listdir(cwd):
        if file.endswith('.json'):
            os.rename(file, 'downloaded_chat.json')


def parse_json():
    """
    Reads JSON file and cleans up the data.
    """
    with open('downloaded_chat.json', 'r', encoding="utf-8") as file:
        contents = json.load(file)


def main():
    rename_file()


main()
