import argparse
from api.scripts.add_user import add_user

if __name__ == "__main__":
    print("Moderator control panel")
    print("=======================")

    # config_to_environ()

    # Configuration options.
    parser = argparse.ArgumentParser(description="Moderator control panel.")
    parser.add_argument(
        "--command", metavar="c", type=str, nargs=1, default="User", help="Command "
    )

    args = parser.parse_args()
    program_command = args.command[0]
    # program_file = args.file[0]

    if program_command == None:
        program_command = "User"

    command = None
    prompt = ""
    continue_execution = True
    command_heading = ""

    if program_command == "U":
        command = add_user
        prompt = "Do you wish to continue adding users?" + " (Y/N) "
        command_heading = "Adding a user"

    print(command_heading)
    print("====================================")

    # Execute command in a loop until the user is done
    while continue_execution:
        command()
        confirmation = input(prompt)
        if confirmation == "N":
            continue_execution = False
