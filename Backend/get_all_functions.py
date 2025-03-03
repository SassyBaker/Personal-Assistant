from inspect import getmembers, isfunction
import functions


def get_list_of_functions():
    list_of_functions = []

    get_functions = getmembers(functions, isfunction)
    for item in get_functions:
        list_of_functions.append(f"{item[0]}()")

    return ', '.join(map(str, list_of_functions))


if __name__ == "__main__":
    print(get_list_of_functions())
