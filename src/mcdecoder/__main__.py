import sys

from . import app


def main() -> int:
    """
    Entry point for mcdecoder

    :return: Exit code of mcdecoder
    """
    return app.run_app(sys.argv)


if __name__ == '__main__':  # pragma: no cover
    sys.exit(main())
