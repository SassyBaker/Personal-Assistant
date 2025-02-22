import functions


def run_command(command):
    commands = command.split("(")
    print(commands)

    func = getattr(functions, commands[0])
    func(commands[1])
