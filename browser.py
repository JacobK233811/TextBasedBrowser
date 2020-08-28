import sys
import os
from collections import deque
import requests
from bs4 import BeautifulSoup
from colorama import Fore


def create_directory():
    args = sys.argv
    try:
        directory = args[1]
        # create directory if there's arg and directory doesn't exist already
        if len(directory) > 0 and not os.path.exists(directory):
            os.mkdir(directory)
        return directory
    except IndexError:
        print("The script should be called with 1 argument - the name of directory")
        exit()


def check_validity(answer):
    return answer.find('.') != -1


valid_ext = ['.org', '.com', '.net', '.gov']


def truncate_filename(name):
    # name = name[:name.find(".")]  # get rid of .com, .org after .
    # return name
    # # or another way to truncate
    parts = name.split(".")  # split into two parts
    if len(parts) != 1:
        name = ".".join(parts[:-1])
    else:
        name = name
    return name


def display_file(path):
    try:
        with open(path) as file:
            print(file.read())
    except FileNotFoundError:
        print(f'File {path} does not exist')


def save_file(path, paragraphs):
    with open(path, 'w+') as out_file:
        for p in paragraphs:
            if p.name == 'a':
                out_file.write(Fore.BLUE + p.text + '\n')
            else:
                out_file.write(Fore.WHITE + p.text + '\n')
        print(path, " saved.")


def main():
    buttons = ['exit', 'back', 'quit', 'clear']
    history = deque()

    directory = create_directory()

    while True:
        choice = input("What do you like to search? Exit to quit.  ").lower()

        if choice in buttons:

            if (choice == "exit") or (choice == "quit"):
                exit()

        # if back, display prev page
            if choice == "back":
                try:
                    current_path = history.pop()
                    prev_path = f'{directory}/{history[-1]}.txt'
                    display_file(prev_path)
                    # history.append(prev_page)
                except IndexError:
                    print("History is clear.")
                    pass  # silent error

            if choice == 'clear':
                pass

        else:   # if not in buttons, must be webpage request
            path = f'{directory}/{choice}.txt'

            # if file already exists, then display contents
            if os.path.isfile(path):
                display_file(path)
                history.append(truncate_filename(choice))
            else:
                # if file doesn't exist, then check if it's a valid URL
                if check_validity(choice):
                    short_name = truncate_filename(choice)
                    path = f'{directory}/{short_name}.txt'

                    if "https://" in choice:
                        webpage = requests.get(choice)
                        soup = BeautifulSoup(webpage.content, 'html.parser')
                        save_file(path, soup.find_all(['title', "p", 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'ul', 'ol', 'li']))
                        display_file(path)
                    elif choice[-4:] in valid_ext:
                        webpage = requests.get("https://" + choice)
                        soup = BeautifulSoup(webpage.content, 'html.parser')
                        save_file(path, soup.find_all(['title', "p", 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'ul', 'ol', 'li']))
                        display_file(path)
                    else:
                        print("error 2 - URL does not exist")
                    # save webpage request into history, valid or not
                    history.append(short_name)
                # otherwise URL itself is not valid
                else:
                    print("error 1 - URL is not valid.  needs .")


if __name__ == '__main__':
    main()
