import cmd
import shlex
from cowsay import cowsay


class CowCmd(cmd.Cmd):
    intro = 'Welcome to cowsay cmd!\n'
    prompt = 'cow says: '

    def cowsay(self, arg):
        '''
        arguments: 
            message: a string to wrap in the text bubble
            cow='default': the name of the cow (valid names from list_cows)
            eyes='oo': a custom eye string
            tongue=' ': a custom tongue string

        Output cow saying the message
        '''
        input_str = shlex.split(arg)
        params = {"message": input_str[0], "cow": "default", "eyes" : "oo", "tongue" : "  "}
        add_param = ''
        for param in input_str[1:]:
            if param.startswith("--") and (param[2:] in params):
                add_param = param[2:]
            elif len(add_param):
                params[add_param] = param
                add_param = ''
        print(cowsay(params['message'], cow=params['cow'], eyes=params['eyes'], tongue=params['tongue']))

    def exit(self, arg):
        'exit from cow cmd'
        print('Bye')
        return 1


if __name__ == '__main__':
    new_cmd = CowCmd()
    new_cmd.cmdloop()
