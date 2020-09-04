import os

from utilities.wincommons import purge_desktop_links


def main():
    purge_desktop_links("Lan")
    print("")


if __name__ == "__main__":
    main()
    input("Press any key to continue...")
