from argparse import ArgumentParser
from configuration.db import session
from command_handler import command_handler


def setup_parser_commands() -> ArgumentParser:
    parser = ArgumentParser()
    # Аргумент для вибору дії
    parser.add_argument(
        "-a", "--action",
        required=True,
        choices=["create", "list", "update", "remove"],
        help="CRUD операція"
    )
    parser.add_argument(
        "-m", "--model",
        required=True,
        choices=["Group", "Student", "Lector", "Subject", "StudentMark"],
        help="Назва таблиці, яку змінюємо"
    )
    parser.add_argument(
        "-n", "--name",
        required=False,
        help="Назва запису"
    )
    parser.add_argument(
        "--id",
        required=False,
        help="Id - запису"
    )
    parser.add_argument(
        "-gid", "--groupid",
        required=False,
        help="Group Id - запису"
    )
    parser.add_argument(
            "-lid", "--lectorid",
            required=False,
            help="Lector Id - запису"
    )
    parser.add_argument(
        "-subid", "--subjectid",
        required=False,
        help="Subject Id - запису"
    )
    parser.add_argument(
        "-stid", "--studentid",
        required=False,
        help="Student Id - запису"
    )
    parser.add_argument(
        "-d", "--date",
        required=False,
        help="Date of mark"
    )
    parser.add_argument(
        "-mk", "--mark",
        required=False,
        help="student mark"
    )

    return parser


if __name__ == "__main__":
    parser = setup_parser_commands()
    try:
        args = parser.parse_args()
        command_handler(args)
    except Exception as e:
        print(f"Command execution error: {e}")
    finally:
        session.close()
