import os
import json


def rename_file(cwd=os.getcwd()):
    # Make sure to set the file location of the downloaded chat to the same directory as this program.
    """
    Renames the arbitrary .json file name to a generic format
    that's easier to work with after the vod chat has been
    downloaded via TwitchDownloader.

    Keyword Arguments:
        cwd - A string representing the current working directory.
    """
    for file in os.listdir(cwd):
        if file.endswith('.json'):
            os.rename(file, 'downloaded_chat.json')


def parse_json():
    """
    Reads the JSON file and cleans up the data.
    """
    with open('downloaded_chat.json', 'r', encoding="utf-8") as file:
        contents = json.load(file)
        chat_history, user_comments = contents['comments'], {}
        for data in chat_history:
            print(data, end='\n\n')  # Separating with a new lines to get a better visual on data. Temporary code.


def main():
    rename_file()
    parse_json()


main()
