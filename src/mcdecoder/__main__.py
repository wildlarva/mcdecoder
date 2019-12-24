import sys

from mcdecoder import app


def main() -> int:
    return app.run_app(sys.argv)


if __name__ == '__main__':
    sys.exit(main())
