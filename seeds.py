from faker import Faker
import random

from configuration.db import session
from configuration.db_model import Group, Student, Lector, Subject, StudentMark


NUMB_STUDENTS = 50
NUMB_SUBJECTS = 8
NUMB_LECTORS = 5
NUMB_GROUPS = 3
NUMB_MARKS = 20


fake = Faker('uk-UA')


def insert_fake_students():
    for _ in range(NUMB_STUDENTS):
        student = Student(
            name=fake.name(),
            group_id=random.randint(1, NUMB_GROUPS)
        )
        session.add(student)


def insert_fake_subjects(numb_words=2):
    for _ in range(NUMB_SUBJECTS):
        subject = Subject(
            subject=fake.sentence(nb_words=numb_words),
            lector_id=random.randint(1, NUMB_LECTORS)
        )
        session.add(subject)


def insert_fake_lectors():
    for _ in range(NUMB_LECTORS):
        lector = Lector(
            name=fake.name()
        )
        session.add(lector)


def insert_fake_groups():
    for _ in range(NUMB_GROUPS):
        group = Group(
            name=f"{fake.word()}-{random.randint(10, 99)}"
        )
        session.add(group)


def insert_fake_marks(min, max):
    for student_id in range(1, NUMB_STUDENTS + 1):
        for subject_id in range(1, NUMB_SUBJECTS + 1):
            for _ in range(NUMB_MARKS):
                student_mark = StudentMark(
                    student_id=student_id,
                    subject_id=subject_id,
                    lecture_date=fake.date(),
                    mark=random.randint(min, max)
                )
                session.add(student_mark)


if __name__ == "__main__":
    try:
        insert_fake_groups()
        insert_fake_students()
        insert_fake_lectors()
        insert_fake_subjects()
        insert_fake_marks(1, 100)
        session.commit()
    except Exception as ex:
        print(ex)
        session.rollback()
    finally:
        session.close()
