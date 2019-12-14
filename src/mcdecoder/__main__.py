import sys
from mcdecoder import generator


def main() -> None:
    if len(sys.argv) < 2:
        print('Please add an argument to specify MC description file path.')
        return

    result = generator.generate(sys.argv[1])
    if result:
        print('Generated MC decoders.')
    else:
        print('Error occurred on generation.')


if __name__ == '__main__':
    main()
