import sys

from mcdecoder import app


def main() -> None:
    sys.exit(app.run_app(sys.argv))


if __name__ == '__main__':
    main()
