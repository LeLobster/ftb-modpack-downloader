#!/usr/bin/env python3

import argparse
import pathlib
import sys
import textwrap
from pprint import pprint

from utils import (
    is_valid_path,
    get_full_path
)


def validate_args(arguments: dict) -> dict:
    """
    List the available modpacks and exit, or
    Check if a target directory is specified and if it is valid

    :param arguments:   The arguments
    :return:            The updated and checked arguments
    """
    if arguments["list_packs"]:
        list_available_packs()

    if arguments["directory"] is not None:
        target_dir = get_full_path(arguments["directory"])
    else:
        if arguments["verbose"]:
            print("Download directory not specified, using current working directory")
        target_dir = pathlib.Path.cwd()

    if not is_valid_path(target_dir):
        if arguments["verbose"]:
            print("Download directory does not exist, creating")
        target_dir.mkdir(parents=True)

    arguments["directory"] = target_dir

    return arguments


def list_available_packs():
    """
    Displays a list of all the known and available modpacks
    Sadly, the undocumented API doesn't provide a method to
     request a full list, so this has to be kept uptodate manually
    Keep an eye on this issue for possible changes in the future
    https://github.com/FTBTeam/FTB-App/issues/103#issuecomment-615226637

    :return:    Nothing
    """
    known_packs = {
        "FTB Interactions": 5
    }
    print("Listing available packs\n=======================")
    for k, v in known_packs.items():
        print(f"{k} : {v}")
    sys.exit()


def init_argparse() -> argparse.ArgumentParser:
    """
    Initialize an argparser with arguments

    :return:    The argparser
    """
    # noinspection PyTypeChecker
    parser = argparse.ArgumentParser(description="An alternative Minecraft FTB modpack downloader",
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--id",
                        action="store", type=int, required=False, default=None,
                        help=f"the modpack id")
    parser.add_argument("--list-packs", "-l",
                        action="store_true", required=False, default=False,
                        help="display a list of the available modpacks and their ids")
    parser.add_argument("--directory", "-d",
                        action="store", type=str, required=False, default=None,
                        help=textwrap.dedent("""the desired download location
if omitted this will be the current working directory
downloaded files are automatically placed in their approriate sub-directories""")
                        )
    parser.add_argument("--include-forge", "-f",
                        action="store_true", required=False, default=False,
                        help=textwrap.dedent("""also download the required forge installer
will be placed in the same dir as --directory""")
                        )
    parser.add_argument("--verbose", "-v",
                        action="store_true", required=False, default=False,
                        help="increase verbosity")
    return parser


def main():
    args: dict = validate_args(
        vars(init_argparse().parse_args())
    )
    # modpack_info: dict = parse_manifest(args["manifest"])
    #
    # print(f"Starting download of: {modpack_info['name']} [{modpack_info['mod_count']} mods]")

    if args["verbose"]:
        pprint(args)
        # pprint(modpack_info)


if __name__ == "__main__":
    main()
