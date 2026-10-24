
from primitive_db.engine import welcome


def main():
    try:
        welcome()
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из программы")


if __name__ == "__main__":
    main()
