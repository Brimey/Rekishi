import json
import os
import smtplib
import ssl
import getpass


def rename_file(cwd=os.getcwd()):
    # Make sure to set the file location of the downloaded chat to the same directory as this program.
    """
    Renames the arbitrary .json file name to a generic format
    that's easier to work with after the vod chat has been
    downloaded via TwitchDownloader.

    :param cwd: A string representing the current working directory.
    """
    for file in os.listdir(cwd):
        if file.endswith('.json') and file != 'downloaded_chat.json':
            os.rename(file, 'downloaded_chat.json')


def parse_json(keyword) -> dict:
    """
    Reads the JSON file and searches for keyword.

    :param keyword: The target word that should be searched for.
    :return: A dictionary containing the usernames of each user with a message that containing the keyword.
    """
    with open('downloaded_chat.json', 'r', encoding="utf-8") as file:
        contents = json.load(file)
        keyword_matches, chat_history = {}, contents['comments']

        for data in chat_history:
            phrase, time_sent, user_name = data['message']['body'].lower().strip().split(), data['created_at'].replace(
                'T', ' ').replace('Z', ' ').strip(), data['commenter']['display_name']
            if keyword.lower() in phrase and user_name not in keyword_matches:
                keyword_matches[user_name] = {time_sent: phrase}
            elif keyword.lower() in phrase and user_name in keyword_matches:
                keyword_matches[user_name] = {**keyword_matches[user_name], time_sent: phrase}

        return keyword_matches


def dump_matches(matches, file_name):
    """
    Writes all the matched users that sent a message
    containing the targeted keyword to a text file (created in the current directory),
    along with the time / date the message was sent.

    :param matches: Dictionary that contains all users that sent a message(s) containing the targeted keyword.
    :param file_name: The text file to write the information to.
    """
    with open(file_name, 'a') as file:
        for user, msg_data in matches.items():
            for time, txt in msg_data.items():
                file.write(f'Date: {time.replace(" ", ", Time: ")}\n{user} said: "{" ".join(txt)}".\n\n')


def send_email():
    port, password, connection = create_connection()
    with smtplib.SMTP_SSL('smtp.gmail.com', port, context=connection) as server:
        sender, recipients, message = input('Enter your Gmail username: '), input(
            'Address of recipient(s): ').split(), f'Subject: Requested chat data.\n\n Message Test.'
        server.login(sender, password)
        server.sendmail(sender, recipients, message)


def create_connection():
    """
    Creates a secure connection for sending emails.
    Prevents echoing your password while typing for privacy reasons.
    """
    port, password, connection = 465, getpass.getpass(
        prompt='Enter the password for your Gmail account: '), ssl.create_default_context()
    return port, password, connection


def main():
    # rename_file()
    # dump_matches(parse_json(input('Enter a keyword to search for: ')), 'matches.txt')  # Test attempt.
    option = input('Would you like to email the text file containing the data to a recipient(s) (enter "Y" or "N")?: ')
    if option.lower() == 'y':
        send_email()  # Test attempt.


main()
