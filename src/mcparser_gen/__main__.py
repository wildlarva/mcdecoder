import sys
from mcparser_gen import generator


def main():
    if len(sys.argv) < 2:
        print('Please add an argument to specify MC description file path.')
        return

    result: bool = generator.generate(sys.argv[1])
    if result:
        print('Generated MC parsers.')
    else:
        print('Error occurred on generation.')

if __name__ == '__main__':
    main()
