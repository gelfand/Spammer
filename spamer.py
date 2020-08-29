import easygui_qt as easy
import discum
import os
import time
import random



def _send(bot, chat_ID, msgs, delay, delay_b):


    while True:

        # print(len(msgs))
        
        msg = msgs[random.randint(0, len(msgs)-1)]

        id_ = bot.sendMessage(chat_ID, msg).json()["id"]
        
        time.sleep(delay_b)

        bot.deleteMessage(chat_ID, id_)
        time.sleep(delay)

    main()


def is_credits(filename="credits.ini"):
    if os.path.isfile(filename):
        with open(filename, "r") as f:
            email, password = f.read().split()

        return email, password

    labels = ["Email", "Password"]

    masks = [False, True]
    
    credits_ = easy.get_many_strings(labels=labels, masks=masks, title="Credits")

    with open(filename, "w") as f:
        f.write(credits_["Email"] + " " + credits_["Password"])
    
    return credits_["Email"], credits_["Password"]
    

def is_settings(filename="settings.ini"):
    if os.path.isfile(filename):
        choice = easy.get_yes_or_no(title="ID and Delays", message="Wanna change ID and Delays?")
        if choice:

            labels = ["Chat_ID", "Delay", "Delay between delete"]

            settings = easy.get_many_strings(labels=labels, title="Credits")

            chat_ID, delay, delay_b = settings["Chat_ID"], settings["Delay"], settings["Delay between delete"]

            with open(filename, "w") as f:
                f.truncate(0)
                f.write(settings["Chat_ID"] + " " + settings["Delay"] + " " + settings["Delay between delete"])

            return chat_ID, float(delay), float(delay_b)

        else:
            with open(filename, "r") as f:
                chat_ID, delay, delay_b = f.read().split()

            return chat_ID, float(delay), float(delay_b)
    
    else:

        labels = ["Chat_ID", "Delay", "Delay between delete"]

        settings = easy.get_many_strings(labels=labels, title="Credits")

        chat_ID, delay, delay_b = settings["Chat_ID"], settings["Delay"], settings["Delay between delete"]

        with open(filename, "w") as f:
            f.truncate(0)
            f.write(settings["Chat_ID"] + " " + settings["Delay"] + " " + settings["Delay between delete"])

        return chat_ID, float(delay), float(delay_b)


def import_pastes(filename="pastes.ini"):

    pastes = []

    with open(filename, "r", encoding="utf8") as f:
        for line in f:
            pastes.append(line)

    return pastes


def main():

    email, password = is_credits()

    bot = discum.Client(email, password)


    chat_ID, delay, delay_b = is_settings()

    msgs = import_pastes()


    _send(bot, chat_ID, msgs, delay, delay_b)


if __name__ == "__main__":
    main()