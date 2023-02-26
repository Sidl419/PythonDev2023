import argparse


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='my cowsay wrapper')
    parser.add_argument("-e", type=str, default='oo', help="appearance of the cow's eyes")
    parser.add_argument("-f", type=str, default='default', help="a particular cow picture file to use")
    parser.add_argument("-l", action="store_true", help="list all cowfiles on the current COWPATH")
    parser.add_argument("-n", action="store_true", help="if specified, the given message will not be wrapped")
    parser.add_argument("-T", type=str, default='  ', help="appearance of the cow's tongue")
    parser.add_argument("-W", type=int, default=40, help="specifies where the message should be wrapped")
    
    args = parser.parse_args()
    print(args)
