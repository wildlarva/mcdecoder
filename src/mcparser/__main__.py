import sys
from mcparser import generator

def main():
    if len(sys.argv) < 2:
        print('Please add an argument to specify MC description file path.')
        return

    generator.generate(sys.argv[1])
    print('Generated MC parsers.')


if __name__ == '__main__':
    main()
