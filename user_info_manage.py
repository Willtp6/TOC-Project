import json
import os

def user_is_exists(user_id):
    # if user info file is not exist
    if not os.path.exists('user_info/' + user_id + '.json'):
        return False
    return True

def init_user_info(user_id):
    dictionary = {
        "id": user_id,
        "client_id": "",
        "client_secret": ""
    }
    with open("user_info/" + user_id + ".json", "w") as outfile:
        json.dump(dictionary, outfile)
    return

def delete_user_info(user_id):
    file_path = 'user_info/' + user_id + '.json'
    if os.path.isfile(file_path):
        os.remove(file_path)
        print("File has been deleted")
    else:
        print("File does not exist")
