from argparse import ArgumentParser
from configuration.db_operations import DBOperations as dbo
from configuration.db_model import Group, Student, Lector, Subject, StudentMark


def command_handler(args: ArgumentParser):
    if args.model == "Group":
        if args.action == "create":
            dbo.insert_group(args.name)
        elif args.action == "list":
            dbo.list_items(Group, ["id", "name"])
        elif args.action == "update":
            dbo.update_group(args.id, args.name)
        elif args.action == "remove":
            dbo.remove_item(Group, args.id)
    elif args.model == "Lector":
        if args.action == "create":
            dbo.insert_lector(args.name)
        elif args.action == "list":
            dbo.list_items(Lector, ["id", "name"])
        elif args.action == "update":
            dbo.update_lector(args.id, args.name)
        elif args.action == "remove":
            dbo.remove_item(Lector, args.id)
    elif args.model == "Student":
        if args.action == "create":
            dbo.insert_student(args.name, args.groupid)
        elif args.action == "list":
            dbo.list_items(Student, ["id", "name", "group_id"])
        elif args.action == "update":
            dbo.update_student(args.id, args.name, args.groupid)
        elif args.action == "remove":
            dbo.remove_item(Student, args.id)
    elif args.model == "Subject":
        if args.action == "create":
            dbo.insert_subject(args.name, args.lectorid)
        elif args.action == "list":
            dbo.list_items(Subject, ["id", "subject", "lector_id"])
        elif args.action == "update":
            dbo.update_subject(args.id, args.name, args.lectorid)
        elif args.action == "remove":
            dbo.remove_item(Subject, args.id)
    elif args.model == "StudentMark":
        if args.action == "create":
            dbo.insert_mark(args.date, args.subjectid, args.studentid, args.mark)
        elif args.action == "list":
            dbo.list_items(StudentMark, ["id", "student_id", "subject_id", "lecture_date", "mark"])
        elif args.action == "update":
            dbo.update_mark(args.id, args.mark)
        elif args.action == "remove":
            dbo.remove_item(StudentMark, args.id)
