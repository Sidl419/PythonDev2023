import cmd
import shlex
from cowsay import cowsay, list_cows, cowthink, make_bubble, THOUGHT_OPTIONS


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

    def list_cows(self, arg):
        '''
        arguments: 
            cow_path work_dir: path with .cow files

        Lists all cow file names in the given directory
        '''
        input_str = shlex.split(arg)
        if len(arg) == 0:
            print(list_cows())
        else:
            print(list_cows(input_str[0]))

    def cowthink(self, arg):
        '''
        arguments: 
            message: a string to wrap in the text bubble
            cow='default': the name of the cow (valid names from list_cows)
            eyes='oo': a custom eye string
            tongue=' ': a custom tongue string

        Output cow thinking the message
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
        print(cowthink(params['message'], cow=params['cow'], eyes=params['eyes'], tongue=params['tongue']))

    def make_bubble(self, arg):
        '''
        arguments: 
            wrap_text=True: wraps text if is true
            width=40: wrapper width
            brackets=THOUGHT_OPTIONS["cowsay"]: bubble type

        Pads text and sets inside a bubble. This is the text that appears above the cows
        '''
        input_str = shlex.split(arg)
        params = {"message": input_str[0], "brackets": THOUGHT_OPTIONS['cowsay'], "width" : 40, "wrap_text" : False}
        add_param = ''
        for param in input_str[1:]:
            if param.startswith("--") and (param[2:] in params):
                add_param = param[2:]
            elif len(add_param):
                if add_param == 'brackets':
                    params[add_param] = THOUGHT_OPTIONS[param]
                elif add_param == 'wrap_text':
                    params[add_param] = param == "true"
                else:
                    params[add_param] = param
                add_param = ''
        print(make_bubble(params['message'], brackets=params['brackets'], width=params['width'], wrap_text=params['wrap_text']))

    def exit(self, arg):
        'exit from cow cmd'
        print('Bye')
        return 1


if __name__ == '__main__':
    new_cmd = CowCmd()
    new_cmd.cmdloop()
