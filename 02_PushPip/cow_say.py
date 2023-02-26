from cowsay import cowsay
import argparse
import sys


OPTIONALS = set("bdgpstwy")


def main(args):
    input_lines = []
    for line in sys.stdin:
        input_lines.append(line.strip())
    input_lines = "\n".join(input_lines)
    
    preset = None
    for option, value in args._get_kwargs():
        if option in OPTIONALS and value:
            preset = option
            break

    is_wrap = not args.n

    print(
        cowsay(
            message=input_lines,
            cow=args.f,
            preset=preset,
            eyes=args.e,
            tongue=args.T,
            width=args.W,
            wrap_text=is_wrap
        ), 
        file=sys.stdout
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='my cowsay wrapper')

    parser.add_argument("-e", type=str, default='oo', help="appearance of the cow's eyes")
    parser.add_argument("-f", type=str, default='default', help="a particular cow picture file to use")
    parser.add_argument("-l", action="store_true", help="list all cowfiles on the current COWPATH")
    parser.add_argument("-n", action="store_true", help="if specified, the given message will not be wrapped")
    parser.add_argument("-T", type=str, default='  ', help="appearance of the cow's tongue")
    parser.add_argument("-W", type=int, default=40, help="specifies where the message should be wrapped")

    for option in OPTIONALS:
        parser.add_argument(f"-{option}", action="store_true")
    
    args = parser.parse_args()
    main(args)
