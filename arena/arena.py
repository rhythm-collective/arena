# -*- coding: utf-8 -*-


from tinydb import TinyDB


def main():
    from os.path import join, dirname
    from dotenv import load_dotenv
    import sys
    dotenv_path = join(dirname(sys.argv[0]), '.env')
    load_dotenv(dotenv_path=dotenv_path, verbose=True)


def mongo():
    main()
    import os
    data = {
        "secret_key": os.getenv("SECRET_KEY"),
        "sample_uri": os.getenv("SAMPLE_URI")
    }
    print("Your authentication information should show up here properly:")
    print(f"secretkey:{data['secret_key']}, uri:{data['sample_uri']}")

    import arena.core.sample as Sample
    Sample.hello_mongo(data['sample_uri'])


def nng():
    main()
    import arena.core.sample as Sample
    Sample.hello_nng()


def registration():
    import os
    print(sys.executable)
    if os.path.basename(sys.executable) == "__main__.exe":
        try:
            from winreg import ConnectRegistry, HKEY_CLASSES_ROOT, \
                CreateKeyEx, SetValueEx, REG_SZ, KEY_ALL_ACCESS, KEY_SET_VALUE

            root = ConnectRegistry(None, HKEY_CLASSES_ROOT)
            policy_key = CreateKeyEx(
                root, r"rhythmcollective", 0, KEY_SET_VALUE)
            SetValueEx(policy_key, None, 0, REG_SZ, "URL:rhythmcollective")
            SetValueEx(policy_key, "URL Protocol", 0, REG_SZ, "")

            policy_key = CreateKeyEx(
                root, r"rhythmcollective\DefaultIcon", 0, KEY_SET_VALUE)
            SetValueEx(policy_key, None, 0, REG_SZ, "\"Arena.exe,1\"")

            policy_key = CreateKeyEx(
                root, r"rhythmcollective\shell\open\command", 0, KEY_ALL_ACCESS)

            SetValueEx(policy_key, None, 0, REG_SZ,
                       f"\"{sys.executable}\" --from-url \"%1\"")
            print("registered")

        except OSError as an_error:
            print(f"unable to open registry {an_error}")


def discord():
    code_verifier = create_code_verifier()
    code_challenge = create_code_challenge(code_verifier)

    tiny_db = open_database(database_location)
    tiny_db.purge_table('auth')
    auth = tiny_db.table('auth')
    auth.insert({'name': 'verifier', 'value': code_verifier})

    code_challenge_method = 'S256'
    client_id = '666012842775937034'
    redirect_uri = 'rhythmcollective://authorize'
    state_fingerprint = 'alfudioashdiofauh'
    discord_scopes = 'identify guilds.join rpc.api messages.read'
    
    from webbrowser import open_new_tab
    open_new_tab(
        "https://discordapp.com/api/oauth2/authorize"
        "?response_type=code"
        f"&client_id={client_id}"
        f"&scope={url_encode(discord_scopes)}"
        f"&state={state_fingerprint}"
        f"&redirect_uri={url_encode(redirect_uri)}"
        f"&code_challenge={code_challenge}"
        f"&code_challenge_method={code_challenge_method}")


def build_basic_popup(top_string: str, action_hint: str, positive_button_action: str) -> list:
    import PySimpleGUI as sg
    sg.theme('DarkAmber')  # Add a touch of color
    layout = [[sg.Text(top_string)],
              [sg.Text(action_hint)],
              [sg.Button(positive_button_action), sg.Button('Quit')]]
    return layout


def simplegui():
    import PySimpleGUI as sg
    sg.theme('DarkAmber')  # Add a touch of color

    import emoji
    layout = [[sg.Text(f'You are not authenticated. {emoji.emojize(":frowning2:")}')],
              [sg.Text('Press Refresh to retry.')],
              [sg.Button('Refresh'), sg.Button('Quit!')]]

    # Create the Window
    window = sg.Window('Window Title', layout)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read(timeout=0)
        if event in (None, 'Quit'):  # if user closes window or clicks cancel
            break
        elif event in (None, 'Ok'):
            window.Element('texttop').Update(values[0])
    window.close()


def checkAuthentication() -> bool:
    return False


def tokens_are_valid():
    return False


def database_exists(file: str) -> bool:
    import os
    return os.path.isfile(file)


def create_database(name: str) -> TinyDB:
    database_file = open(name, "w+")
    database_file.close()
    return open_database(name)


def open_database(name: str) -> TinyDB:
    return TinyDB(name)


def authorize(code: str, verifier: str) -> str:
    api_endpoint = 'https://discordapp.com/api/v6'
    client_id = '666012842775937034'
    client_secret = '921nKl7su2DG-8O4IqhhM2BqCVecHRgC'
    discord_scopes = 'identify guilds.join rpc.api messages.read'
    redirect_uri = 'rhythmcollective://authorize'
    data = {
        'client_id': client_id,
        'grant_type': 'authorization_code',
        'redirect_uri': redirect_uri,
        'code': code,
        'code_verifier': verifier,
        'scope': discord_scopes
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    import requests
    req = requests.post(f'{api_endpoint}/oauth2/token',
                        data=data, headers=headers)
    req.raise_for_status()
    return req.json()


def url_encode(url: str) -> str:
    from urllib.parse import quote
    return quote(url)


def create_code_verifier():
    from base64 import urlsafe_b64encode
    from re import sub
    code_verifier = urlsafe_b64encode(os.urandom(40)).decode('utf-8')
    code_verifier = sub('[^a-zA-Z0-9]+', '', code_verifier)
    return code_verifier

def create_code_challenge(code_verifier: str):
    from base64 import urlsafe_b64encode
    from hashlib import sha256
    code_challenge = sha256(code_verifier.encode('utf-8')).digest()
    code_challenge = urlsafe_b64encode(code_challenge).decode('utf-8')
    code_challenge = code_challenge.replace('=', '')
    return code_challenge

def sha256(buffer):
    import hashlib
    m = hashlib.sha256()
    m.update(buffer)
    return m.digest()

if __name__ == "__main__":
    main()  # Make sure our environment variables are present.

    import os
    database_location = f"{os.path.expanduser('~')}\db.json"
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == '--from-url':
        registration()  # Make sure the URI is registered.
        if tokens_are_valid():
            pass
        else:
            # Tokens are not valid, or do not exist, so we need to authenticate.
            import regex
            CODE_REGEX = regex.compile(r'.*code=(.*)&', regex.IGNORECASE)
            STATE_REGEX = regex.compile(r'.*state=(.*)', regex.IGNORECASE)
            code = CODE_REGEX.match(sys.argv[2])
            state = STATE_REGEX.match(sys.argv[2])

            tiny_db = None
            if database_exists(database_location):
                tiny_db = open_database(database_location)
                auth = tiny_db.table('auth')
                auth.insert({'name': 'code', 'value': code[1]})
            else:
                tiny_db = create_database(database_location)
                auth = tiny_db.table('auth')
                auth.insert({'name': 'code', 'value': code[1]})

    else:
        from tinydb.database import Table
        from tinydb import where
        tiny_db = open_database(database_location)
        auth_table = tiny_db.table('auth')
        if len(auth_table.all()) > 0:
            if False:
                code = auth_table.search(where('name') == 'code')
                verifier = auth_table.search(where('name') == 'verifier')
                auth_json = authorize(code[0]['value'], verifier[0]['value'])
                print(auth_json)
                #simplegui()
            else:
                import discord

                class MyClient(discord.Client):
                    async def on_ready(self):
                        print('Connected!')
                        print('Username: {0.name}\nID: {0.id}'.format(self.user))

                    async def on_message(self, message):
                        # don't respond to ourselves
                        if message.author == self.user:
                            return

                        await message.channel.send('pong')

                try:
                    client = MyClient()
                    client.run('pBpvZJKitk2jATl3uWMJz3HrmvcMF9', bot=False)
                except Exception as e:
                    print(e)

        else:
            discord()
        

        #simplegui()
