#!/usr/bin/python3

import click
import socket
import threading
import os
import sys
name_list = []

'''
so the chat client will send the alive message every 15 seconds, 
the server should respond every time. 

every time the server responds you can reset the timer to 0 and start counting up to 30 again. 
If the server goes offline it will stop responding and the time should reach 30+ seconds 
and your client should time out
'''
sd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


@click.command()
@click.argument('name')
@click.argument('host')  # IP Address
@click.argument('port', type=click.INT)

def do_client(name, host, port):  # main

    try:
        print("opening connection to {}:{}".format(host, port))
        # TCP socket
        # connect to server
        sd.connect((host, port))
        # sd.settimeout(30)  # if the socket did not get anything back from server in 30s
        print("Connected")
        # get user name, send to server
        name = name + "\n"
        sd.send(name.encode())
        threading.Thread(target=send_mesg, args=(sd,)).start()
        threading.Thread(target=receive_mesg, args=(sd,)).start()
        # send alive message every 15s
        threading.Timer(15.0, send_alive_Mesg, args=[sd,]).start()
    except KeyboardInterrupt:
        print("Shutdown 1")
        sd.close()
        os._exit(0)
    except Exception as e:
        print("Client faixled 1: ")
        print(e)
        sd.close()
        os._exit(0)


'''
this function can be tested use nc -l 3333 locally
it won't show when connect to a real server because if the server left
its last empty message will tell the client "server left", and the client will also close. 
'''
def alive_timeout(_socket):
    try:
        raise Exception("Sever timeout, disconnect")
    except Exception as e:
        print(e)
        _socket.close()
        os._exit(0)


# thread
def send_alive_Mesg(_socket):
    try:
        _socket.send(b"alive:\n")
        global timeout_timer
        timeout_timer = threading.Timer(30.0, alive_timeout,args=[sd, ])
        timeout_timer.start()
    except RuntimeError:
        # thread only start once
        pass
    except KeyboardInterrupt:
        print("Shutdown 4")
        _socket.close()
        os._exit(0)
    except Exception as e:
        print("Client failed 4: ")
        print(e)
        _socket.close()
        os._exit(0)
    threading.Timer(15.0, send_alive_Mesg, args=[_socket]).start()

# thread
def send_mesg(_socket):
    # ===== same thing above=====
    # data from client to server
    # mess: message\n, alive:\n, whoisthere:\n
    try:
        while True:
            user_mesg = sys.stdin.readline()
            # when user enter something, send to server, otherwise, do not send anything
            if (user_mesg != "\n"):
                encoded_mesg = encode_mesg(user_mesg)
                _socket.send(encoded_mesg.encode())
    except KeyboardInterrupt:
        print("Shutdown 2")
        _socket.close()
        os._exit(0)
    except Exception as e:
        print("Client failed 2: ")
        print(e)
        _socket.close()
        os._exit(0)


# thread
def receive_mesg(_socket):
    # mesg from server to client
    try:
        while True:
            server_mesg = _socket.recv(2048)
            if not server_mesg:
                raise Exception ('Server Closed')
                # raise Exception # when no message come from server, break & stop
            else:
                decoded_mesg = decode_mesg(server_mesg.decode(), _socket)
                if decoded_mesg[:3] == "ali":
                    timeout_timer.cancel()
                elif decoded_mesg != 0:
                    print(decoded_mesg)
    except KeyboardInterrupt:
        print("Shutdown 3")
        _socket.close()
        os._exit(0)
    except Exception as e:
        if str(e) == 'Server Closed':
            print(e) # wait for timeout to close
        else:
            print("Client failed 3: ")
            print(e)
            _socket.close()
            os._exit(0)




def encode_mesg(_mesg):
    if _mesg == "/list\n":
        # check whoisthere:
        return "whoisthere:\n"  # return to the current alive user list
    else:
        return "mess: " + _mesg  # careful on \n


def decode_mesg(_mesg, _socket):
    # possible messages from server
    # joined: name\n, left: name\n, present: name\n, mess-name: message\n, alive:\n
    '''
    when the client sends the "whoisthere" message to the server,
    the server will respond with a present message for each name that is currently connected.
    once all names have been sent,
    the server will send "present:\n" (a present message with no name) indicating the end of the list.
    '''
    # mess-name: message\n
    if _mesg[0:4] == "mess":
        return _mesg[5:len(_mesg) - 1]  # mesg from other clients
    # joined: name\n
    elif _mesg[0:4] == "join":
        return _mesg[8:len(_mesg) - 1] + " joined"
    # left: name\n
    elif _mesg[0:4] == "left":
        return _mesg[6:len(_mesg) - 1] + " left"
    # present: name\n
    # present:\n
    elif _mesg[0:4] == "pres":
        present_list = _mesg.split("\n")
        for present_mesg in present_list:
            if len(present_mesg) == 8:
                message = "Present: " + ", ".join(name_list)
                del name_list[:] # name_list.clear()
                return message
            else:
                name = present_mesg[9:len(present_mesg)]
                name_list.append(name)
                return 0
    elif _mesg[0:5] == "alive":
        return "alive"
    else:
        return 0 # print nothing if does not fit format





if __name__ == "__main__":
    try:
        do_client()
    except KeyboardInterrupt:
        print("get keyboardInterrupt 0 ")
        # os._exit(0)
        exit(0)
    except Exception as e:
        print("Client failed 0: ")
        print(e)
        # os._exit(0)
        exit(0)

