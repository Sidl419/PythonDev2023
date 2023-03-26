import cmd
import threading
import readline
import socket


lock = threading.Lock()


class CowClient(cmd.Cmd):

    def do_who(self, args):
        s.send("who\n".encode())


def messenger(cmdline):
    while True:
        with lock:
            msg = s.recv(1024).decode()
        if msg:
            print(msg.strip())
            print(f"{cmdline.prompt}{readline.get_line_buffer()}", end="", flush=True)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(('0.0.0.0', 1337))
    cmdline = CowClient()
    chat = threading.Thread(target=messenger, args=(cmdline,))
    chat.start()
    cmdline.cmdloop()
