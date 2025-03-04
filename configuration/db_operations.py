from configuration.db import session
from configuration.db_model import Group, Student, Lector, Subject, StudentMark


class DBOperations:
    # операції роботи з БД
    @staticmethod
    def insert_item(item):
        session.add(item)
        session.commit()

    @staticmethod
    def list_items(table, columns):
        result = session.query(table).all()
        items = [
            dict(
                zip(
                    columns,
                    (getattr(item, col) for col in columns)
                )
            ) for item in result
        ]
        print(items)
        # for item in result:
        #   print(item)

    @staticmethod
    def remove_item(table, id):
        item = session.query(table).filter_by(id=id).first()
        if item:
            session.delete(item)
            session.commit()

    # операції з конктретними обєктами
    @staticmethod
    def insert_student(name, group_id):
        student = Student(name=name, group_id=group_id)
        DBOperations.insert_item(student)

    @staticmethod
    def update_student(id, name, group_id):
        item = session.query(Student).where(Student.id == id).first()
        if item:
            item.name = name
            item.group_id = group_id
            session.commit()

    @staticmethod
    def insert_subject(name, lector_id):
        subject = Subject(subject=name, lector_id=lector_id)
        DBOperations.insert_item(subject)

    @staticmethod
    def update_subject(id, name, lector_id):
        item = session.query(Subject).where(Subject.id == id).first()
        if item:
            item.subject = name
            item.lector_id = lector_id
            session.commit()

    @staticmethod
    def insert_lector(name):
        lector = Lector(name=name)
        DBOperations.insert_item(lector)

    @staticmethod
    def update_lector(id, name):
        item = session.query(Lector).where(Lector.id == id).first()
        if item:
            item.name = name
            session.commit()

    @staticmethod
    def insert_group(name):
        group = Group(name=name)
        DBOperations.insert_item(group)

    @staticmethod
    def update_group(id, name):
        item = session.query(Group).where(Group.id == id).first()
        if item:
            item.name = name
            session.commit()

    @staticmethod
    def insert_mark(date, subject_id, student_id, mark):
        student_mark = StudentMark(
            student_id=student_id,
            subject_id=subject_id,
            lecture_date=date,
            mark=mark
        )
        DBOperations.insert_item(student_mark)

    @staticmethod
    def update_mark(id, mark):
        item = session.query(StudentMark).where(StudentMark.id == id).first()
        if item:
            item.mark = mark
            session.commit()
