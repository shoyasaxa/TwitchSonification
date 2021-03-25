import socket
import sys
import re
import time 
import json
from datetime import timedelta


USERNAME = "your_username_here"
PASSWORD = "your_oauth_here"  # retrieve from https://twitchapps.com/tmi/
JOIN_USERNAME = "twitch_channel_to_join" # twitch channel's name  to join 


# USERNAME = "pokelingual"
# PASSWORD = "oauth:sd7aihstoh7c25szy9mxfmh3rs3t85"

# USERNAME = "magrayy"
# PASSWORD = "oauth:asd522tzkyqrhkjc3kl5v6kz193cf3" 
# JOIN_USERNAME = "noelmiller"

TIME_TO_SLEEP = 2 

class TwitchBot:
    
    def __init__(self):
        self.set_socket_object()
        self.socket_retry_count = 0
        
    def check_login_status(self, data):
        if not re.match(r'^:(testserver\.local|tmi\.twitch\.tv) NOTICE \* :Login unsuccessful\r\n$', data): return True

    def set_socket_object(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock = sock

        sock.settimeout(10)

        server = 'irc.twitch.tv'
        port = 6667

        try:
            sock.connect((server, port))
        except:
            pp('Error connecting to IRC server. (%s:%i) (%i)' % (server, port, self.socket_retry_count + 1), 'error')

            if self.socket_retry_count < 2:
                self.socket_retry_count += 1
                return self.set_socket_object()
            else:
                sys.exit()

        sock.settimeout(None)

        sock.send(('USER %s\r\n' % USERNAME).encode())
        sock.send(('PASS %s\r\n' % PASSWORD).encode())
        sock.send(('NICK %s\r\n' % USERNAME).encode())

        if not self.check_login_status(self.sock.recv(1024).decode()):
            print('Invalid login.', 'error')
            sys.exit()
        else:
            print('=== Login successful! ===')

        sock.send(('JOIN #%s\r\n' % JOIN_USERNAME).encode())
        print('Joined #%s' % JOIN_USERNAME)

    def get_user_and_message(self,line):
        line_split = line.split(":",2)
        user = line_split[1].split("!",1)[0]

        try:
            msg = line_split[2]
        except Exception as e:
            print(e)
            msg = ""

        return user, msg 

    def run(self):
        print("=== Starting to Read Chat === ")
        i = 0 
        try:
            while True:
                i+=1 
                try:
                    time.sleep(TIME_TO_SLEEP)
                    readbuffer = self.sock.recv(16384).decode()
                except KeyboardInterrupt:
                    print('Ctrl+C Pressed')
                    self.sock.close()
                    break
                except Exception:
                    readbuffer = ""
    
                for line in readbuffer.split("\r\n"):
                    try:
                        if line == "":
                            continue
                        elif "PING" in line:
                            # print('=========ponging back===========')
                            msg = "PONG tmi.twitch.tv\r\n".encode()
                            self.sock.send(msg)
                        else:
                            user,message = self.get_user_and_message(line)
                            print("{}:{}".format(user,message))

                            # TODO: do stuff with messages here 

                    except Exception as e:
                        print(e)
                        print("failed on line: {}".format(line))

        except KeyboardInterrupt:
            print("Ctrl+C-ed")
        finally:
            self.sock.close()
                    
if __name__ == '__main__':
    bot = TwitchBot()
    bot.run()
