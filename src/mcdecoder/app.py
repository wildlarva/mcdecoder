from typing import List
from mcdecoder import generator


def run_app(argv: List[str]):
    if len(argv) < 2:
        print('Please add an argument to specify MC description file path.')
        return

    result = generator.generate(argv[1])
    if result:
        print('Generated MC decoders.')
    else:
        print('Error occurred on generation.')
