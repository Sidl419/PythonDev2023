import cmd
import threading
import readline
import socket
import select


lock = threading.Lock()


class CowClient(cmd.Cmd):

    def do_who(self, args):
        'list active cows from the server'
        s.send("who\n".encode())

    def do_exit(self, args):
        'exit from cow client'
        s.send("exit\n".encode())
        return 1
    
    def do_cows(self, args):
        'list available cows from the server'
        s.send("cows\n".encode())

    def do_yield(self, args):
        'send message to every user'
        s.send(f"yield {args}\n".encode())

    def do_login(self, args):
        'login by some cow name'
        s.send(f"login {args}\n".encode())

    def complete_login(self, pfx, line, beg, end):
        with lock:
            s.send("cows\n".encode())
            msg = recv(None).strip().split(': ')[1]
            cows = msg.split(', ')
            return [s for s in cows if s.startswith(pfx)]
        
    def do_say(self, args):
        'send message to some conrete user'
        s.send(f"say {args}\n".encode())

    def complete_say(self, pfx, line, beg, end):
        with lock:
            if len(pfx.split()) <= 1:
                s.send("who\n".encode())
                msg = recv(None).strip().split(': ')[1]
                who = msg.split(', ')
                return [s for s in who if s.startswith(pfx)]
        

def recv(timeout=0.):
    readable, _, _ = select.select([s], [], [], timeout)

    for soc in readable:
        msg = soc.recv(1024).decode()
        return msg


def messenger(cmdline):
    try:
        while True:
            with lock:
                msg = recv()
            if msg:
                print(f"\n{msg.strip()}")
                print(f"{cmdline.prompt}{readline.get_line_buffer()}", end="", flush=True)
    except ValueError as e:
        print("your session is closed")


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(('0.0.0.0', 1337))
    s.setblocking(False)
    cmdline = CowClient()
    chat = threading.Thread(target=messenger, args=(cmdline,))
    chat.start()
    cmdline.cmdloop()
