from transitions.extensions import GraphMachine

from utils import send_text_message, push_text_message, send_audio_message, push_image_message, push_audio_message

import os
import spotify_api
import json
from user_info_manage import user_is_exists, init_user_info, delete_user_info

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
    '''
    condition function
    '''
    def is_going_to_state_login(self, event):
        text = event.message.text
        return text.lower() == "spotify account login"

    def artist_founded(self, event):
        if self.state == "state_find_artist":
            results = spotify_api.get_artist_info(event.source.user_id, event.message.text)
            print(results)
            if results == "error in get data":
                push_text_message(event, "there was an error in get data\nplease check you account info")
                return False
            if results:
                with open('artist_info/'+event.message.text+'.json', 'w') as fp:
                    json.dump(results, fp, indent=2)
                current_artist_info = {
                    "artist_name": event.message.text,
                    "album_name": ""
                }
                with open('user_info/current_artist.json', 'w') as f:
                    json.dump(current_artist_info, f, indent=2)
                push_image_message(event, results['artists']['items'][0]['images'][1]['url'])
            else:
                push_text_message(event, "can no find artist: "+event.message.text)
                push_text_message(event, "enter artist name")
            if os.path.exists('artist_info/' + event.message.text + '.json'):
                return True
            else:
                return False
        return False

    def album_founded(self, event):
        if self.state == "state_find_album":
            data = json.load(open('user_info/current_artist.json'))
            album_info = spotify_api.get_album_info(event.source.user_id, event.message.text)
            if album_info == "error in get data":
                push_text_message(event, "there was an error in get data\nplease check you account info")
                return False
            if album_info:
                data = json.load(open('user_info/current_artist.json'))
                current_artist_info = {
                    "artist_name": data["artist_name"],
                    "album_name": event.message.text
                }
                # update current artist value
                with open('user_info/current_artist.json', 'w') as f:
                    json.dump(current_artist_info, f, indent=2)
                # create new album json file
                with open("artist_info/" + data['artist_name'] + '_' +  event.message.text + ".json", "w") as outfile:
                    json.dump(album_info, outfile , indent=2)
                push_image_message(event, album_info['images'][1]['url'])
            else:
                push_text_message(event, "can not find album: "+event.message.text)
                push_text_message(event, "enter album name")    
            if os.path.exists("artist_info/" + data['artist_name'] + '_' +  event.message.text + ".json"):
                return True
            else:
                return False
        else:
            return False

    def track_exist(self, event):
        if self.state != "state_find_track":
            return False
        track_info = spotify_api.get_track_info(event.source.user_id, event.message.text)
        if track_info:
            return True
        else:
            push_text_message(event, "can not find track: "+event.message.text)
            push_text_message(event, "enter track name")
            return False

    def is_account_message(self, event):
        if self.state == "state_login":
            text = event.message.text
            account_messages = text.split("\n")
            if len(account_messages) == 2:
                parsed_id = account_messages[0].split(":")
                parsed_secret = account_messages[1].split(":")
                dictionary = {
                    "id": event.source.user_id,
                    "client_id": parsed_id[1],
                    "client_secret": parsed_secret[1]
                }
                with open("user_info/" + event.source.user_id + ".json", "w") as outfile:
                    json.dump(dictionary, outfile, indent=2)
                return True
            else:
                return False
        else:
            return False

    def is_check_account_info(self, event):
        text = event.message.text
        return text.lower() == "check account info"

    def is_find_artist(self, event):
        if self.state != "state_login":
            return False
        text = event.message.text
        return text.lower() == "search"

    def is_going_back_to_menu(self, event):
        text = event.message.text
        return text.lower() == "back to menu"
    '''
    def is_going_to_state_showSongList(self, event):
        text = event.message.text
        return text.lower() == "show song list"
    '''
    def is_delete_user_info(self, event):
        text = event.message.text
        return text.lower() == "delete account info"

    '''
    change to help
    '''
    def on_enter_state_help_in_user(self, event):
        push_text_message(event, "1.go to this link https://developer.spotify.com\n2.go to Dashboard\n3.login with your spotify account\n4.create a new app\n5.enter spotify account login to login")
        self.go_back(event)
    
    def on_enter_state_help_in_login(self, event):
        push_text_message(event, "1.use the format below to add your account information\nclient_id:XXXXXXXXXX\nclient_secret:XXXXXXXXXX\n2.enter check account info to check your account info\n3.enter delete account info to delete recorded info\n4.entr search to start searching")
        self.go_back(event)

    def on_enter_state_help_in_find_artist(self, event):
        push_text_message(event, "enter artist name to get artist information")
        self.go_back(event)

    def on_enter_state_help_in_find_album(self, event):
        push_text_message(event, "enter (show albums) will list all albums")
        self.go_back(event)

    def on_enter_state_help_in_find_track(self, event):
        push_text_message(event, "enter (show tracks) will list all tracks")
        self.go_back(event)
    '''
    change to states
    '''
    def on_enter_state_find_artist(self, event):
        push_text_message(event, "enter artist name you want to find")
        
    def on_enter_state_find_album(self, event):
        push_text_message(event, "enter album name you want to find")
     
    def on_enter_state_find_track(self, event):
        push_text_message(event, "enter track name")
    
    def on_enter_state_delete_info(self, event):
        delete_user_info(event.source.user_id)
        self.go_back(event)

    def on_enter_state_input_account(self, event):
        push_text_message(event, "account is successfully logined")
        self.go_back(event)

    def on_enter_state_login(self, event):
        reply_token = event.reply_token
        # if user id already has a json account file
        if user_is_exists(event.source.user_id):
            reply_message = "Welcome"
        else:
            init_user_info(event.source.user_id)
            reply_message = "use the format below to add your account information\nclient_id:XXXXXXXXXX\nclient_secret:XXXXXXXXXX\nif there is any question enter: help"
        send_text_message(reply_token, reply_message)

    def on_enter_state_check_account_info(self, event):
        data = json.load(open('user_info/'+event.source.user_id+'.json'))
        push_text_message(event, "client_id:"+data['client_id']+'\n'+'client_secret:'+data['client_secret'])
        self.go_back(event)
    '''
    def on_enter_state_showSongList(self, event):
        offset = 0
        song_list = ""
        reply_messages = []
        while True:
            # call spotify api
            results = spotify_api.show_my_song_list(limit=50, offset=offset, user_id=event.source.user_id)
            # if account info has something error can not get song list
            if(results == None):
                song_list = "There is something wrong in your spotify account info"
                break
            added_list = '\n'.join(item['track']['artists'][0]['name']+ " - "+ item['track']['name'] for item in results['items'])
            # 5000 is the limit of char in a message in Line
            if len(added_list)+len(song_list) > 5000:
                reply_messages.append(song_list)
                song_list = ""

            song_list += added_list
            
            if len(results['items']) < 50:
                break
            else:
                offset += 50
        reply_messages.append(song_list)
        reply_token = event.reply_token
        send_text_message(reply_token, reply_messages)
        # go back to login state
        self.go_back(event)
    '''
    def on_enter_user(self, event):
        # delete all artists info
        dir = 'artist_info/'
        for f in os.listdir(dir):
            os.remove(os.path.join(dir, f))
        if os.path.exists('user_info/current_artist.json'):
            os.remove('user_info/current_artist.json')
        push_text_message(event, "Back to menu")
    
    def on_enter_state_track_founded(self, event):
        track_info = spotify_api.get_track_info(event.source.user_id, event.message.text)
        push_text_message(event, "30secs preview")
        push_audio_message(event, track_info['preview_url'])
        push_text_message(event, 'full version on:\n'+track_info['external_urls']['spotify'])
        self.go_back(event)