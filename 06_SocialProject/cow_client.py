import cmd
import threading
import time
import readline


class CowClient(cmd.Cmd):

    def do_echo(self, arg):
        print(arg)


def spam(cmdline, timeout, count):
    for i in range(count):
        time.sleep(timeout)
        print(f"\nI'm a message № {i}!\n{cmdline.prompt}{readline.get_line_buffer()}", end="", flush=True)


cmdline = CowClient()
timer = threading.Thread(target=spam, args=(cmdline, 3, 10))
timer.start()
cmdline.cmdloop()
