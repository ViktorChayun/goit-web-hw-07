from sqlalchemy import func, desc, select, and_
from sqlalchemy.orm import aliased
from configuration.db_model import Group, Student, Lector, Subject, StudentMark
from configuration.db import session


def select_01():
    """
    Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
    SELECT
        students.name
        ,AVG(student_marks.mark) as avg_mark
    FROM students
    INNER JOIN student_marks ON students.id = student_marks.student_id
    GROUP BY 
        students.name
    ORDER BY avg_mark DESC
    LIMIT 5
    """
    result = session.query(Student.name, func.round(func.avg(StudentMark.mark), 2).label("avg_mark")) \
        .select_from(Student) \
        .join(StudentMark) \
        .group_by(Student.name) \
        .order_by(desc('avg_mark')).all()
    return result


def select_02(subject_id):
    """
    Знайти студента із найвищим середнім балом з певного предмета.

    SELECT
        s.name,
        AVG(sm.mark) as avg_mark
    FROM students s
    INNER JOIN student_marks sm ON s.id = sm.student_id
    WHERE
        sm.subject_id = ?
    GROUP BY
        s.name
    ORDER BY
        avg_mark DESC
    LIMIT 1
    """
    result = session.query(Student.name, func.round(func.avg(StudentMark.mark), 2).label('avg_mark')) \
        .select_from(Student) \
        .join(StudentMark) \
        .where(StudentMark.subject_id == subject_id) \
        .group_by(Student.name) \
        .order_by(desc('avg_mark')) \
        .limit(1).all()
    return result


def select_03(subject_id):
    """
    Знайти середній бал у групах з певного предмета.

    SELECT
        g.name,
        AVG(sm.mark) as avg_mark
    FROM student_marks sm
    INNER JOIN students s ON s.id = sm.student_id
    INNER JOIN groups g on s.group_id =g.id
    WHERE
        sm.subject_id = ?
    GROUP BY
        g.name
    ORDER BY
        avg_mark DESC
    """
    result = session.query(Group.name, func.round(func.avg(StudentMark.mark), 2).label('avg_mark'))\
        .select_from(StudentMark)\
        .join(Student)\
        .join(Group)\
        .where(StudentMark.subject_id == subject_id)\
        .group_by(Group.name)\
        .order_by(desc('avg_mark')).all()
    return result


def select_04():
    """
    Знайти середній бал на потоці (по всій таблиці оцінок) 

    SELECT
        AVG(sm.mark) as avg_mark
    FROM student_marks sm
    """
    result = session.query(func.round(func.avg(StudentMark.mark), 2))\
        .select_from(StudentMark).all()
    return result


def select_05(lector_id):
    """
    Знайти які курси читає певний викладач.

    SELECT
        l.name as lector_name,
        sub.subject
    FROM subjects sub
    INNER JOIN lectors l on l.id = sub.lector_id
    WHERE
        l.id = ?
    ORDER BY
        subject
    """
    result = session.query(Lector.name, Subject.subject)\
        .select_from(Subject)\
        .join(Lector)\
        .where(Lector.id == lector_id)\
        .order_by('subject')\
        .all()
    return result


def select_06(group_id):
    """
    Знайти список студентів у певній групі.

    SELECT
        s.name as student_name
    FROM students s
    INNER JOIN groups g on g.id = s.group_id
    WHERE
        g.id = 1
    ORDER BY
        student_name
    """
    result = session.query(Student.name.label('student_name'))\
        .select_from(Student)\
        .join(Group)\
        .where(Group.id == group_id)\
        .order_by('student_name').all()
    return result


def select_07(group_id, subject_id):
    """
    Знайти оцінки студентів у окремій групі з певного предмета

    SELECT
        sub.subject
        ,g.name
        ,s.name as student_name
        ,sm.mark
    FROM students s
    INNER JOIN groups g on g.id = s.group_id
    INNER JOIN student_marks sm on sm.student_id  = s.id
    INNER JOIN subjects sub on sub.id  = sm.subject_id
    WHERE
        g.id = ?
        and sub.id = ?
    ORDER BY
        student_name
    """
    result = session.query(Subject.subject, Group.name, Student.name.label('student_name'), StudentMark.mark)\
        .select_from(Student)\
        .join(Group)\
        .join(StudentMark)\
        .join(Subject)\
        .where(and_(Group.id == group_id, Subject.id == subject_id))\
        .order_by('student_name').all()
    return result


def select_08(lector_id):
    """
    Знайти середній бал, який ставить певний викладач зі своїх предметів.

    SELECT
        l.name as lector,
        AVG(sm.mark) as avg_mark
    FROM student_marks sm
    INNER JOIN subjects sub on sub.id  = sm.subject_id
    INNER JOIN lectors l on l.id = sub.lector_id  
    WHERE
        l.id = ?
    GROUP BY
        l.name
    """
    result = session.query(Lector.name, func.round(func.avg(StudentMark.mark), 2).label('avg_mark'))\
        .select_from(StudentMark)\
        .join(Subject)\
        .join(Lector)\
        .where(Lector.id == lector_id)\
        .group_by(Lector.name).all()
    return result


def select_09(student_id):
    """
    Знайти список курсів, які відвідує студент

    SELECT DISTINCT
        s.name as student_name
        ,sub.subject
    FROM students s
    INNER JOIN student_marks sm on sm.student_id  = s.id
    INNER JOIN subjects sub on sub.id  = sm.subject_id
    WHERE
        s.id = ?
    ORDER BY
        subject
    """
    result = session.query(Student.name.label('student_name'), Subject.subject)\
        .select_from(Student)\
        .join(StudentMark)\
        .join(Subject)\
        .where(Student.id == student_id)\
        .distinct()\
        .order_by('subject').all()
    return result


def select_10(student_id, lector_id):
    """
    Список курсів, які певному студенту читає певний викладач.

    SELECT DISTINCT
        s.name as student_name
        ,l.name as lector
        ,sub.subject
    FROM students s
    INNER JOIN student_marks sm on sm.student_id  = s.id
    INNER JOIN subjects sub on sub.id  = sm.subject_id
    INNER JOIN lectors l on l.id = sub.lector_id
    WHERE
        s.id = ?    # student id
        and l.id = ? # lector id
    ORDER BY
        subject
    """
    result = session.query(Student.name.label('student_name'), Lector.name.label('lector'), Subject.subject)\
        .select_from(Student)\
        .join(StudentMark)\
        .join(Subject)\
        .join(Lector)\
        .where(and_(Student.id == student_id, Lector.id == lector_id))\
        .distinct()\
        .order_by('subject').all()
    return result


def select_11(student_id, lector_id):
    """
    Середній бал, який певний викладач ставить певному студентові.

    SELECT
        s.name as student_name,
        l.name as lector,
        AVG(sm.mark) as avg_mark
    FROM students s
    INNER JOIN student_marks sm on sm.student_id  = s.id
    INNER JOIN subjects sub on sub.id  = sm.subject_id
    INNER JOIN lectors l on l.id = sub.lector_id
    WHERE
        s.id = ? # student id
        and l.id = ? # lector id
    GROUP BY
        s.name,
        l.name
    """
    result = session.query(
        Student.name.label('student_name'),
        Lector.name.label('lector'),
        func.round(func.avg(StudentMark.mark), 2).label('avg_mark')
        ).select_from(Student)\
        .join(StudentMark)\
        .join(Subject)\
        .join(Lector)\
        .where(and_(Student.id == student_id, Lector.id == lector_id))\
        .group_by(Student.name, Lector.name).all()
    return result


def select_12(group_id, subject_id):
    """
    Оцінки студентів у певній групі з певного предмета на останньому занятті.

    SELECT
        g.group_name,
        s.name as student_name,
        sub.subject as subject,
        sm.mark
    FROM students s
    INNER JOIN groups g on g.id = s.group_id 
    INNER JOIN student_marks sm on sm.student_id  = s.id
    INNER JOIN subjects sub on sub.id  = sm.subject_id
    WHERE
        g.id = ? # group id
        and sub.id = ? # subject id
        # останнє заняття студента по даному преедмету
        # пошук останьої дати лекції по даному студенту і предмету
        and sm.date = (
            SELECT
                MAX(DATE)
            FROM student_marks sm2
            WHERE
                sm2.student_id = sm.student_id
                and sm2.subject_id = sm.subject_id
        )
    ORDER BY
        student_name,
        subject
    """
    sm2 = aliased(StudentMark)
    sub_query = (
        session.query(func.max(sm2.lecture_date))\
            .select_from(sm2)\
            .where(
                and_(sm2.student_id == StudentMark.student_id,
                     sm2.subject_id == StudentMark.subject_id)
                )\
            .correlate(StudentMark)\
            .scalar_subquery()
        )

    result = session.query(
            Group.name,
            Student.name.label('student_name'),
            Subject.subject.label('subject'),
            StudentMark.mark
        )\
        .select_from(Student)\
        .join(Group)\
        .join(StudentMark)\
        .join(Subject)\
        .where(and_(Group.id == group_id, Subject.id == subject_id, StudentMark.lecture_date == sub_query))\
        .order_by('student_name', 'subject').all()
    return result


if __name__ == "__main__":
    print(select_01())
    print(select_02(1))
    print(select_03(2))
    print(select_04())
    print(select_05(4))
    print(select_06(1))
    print(select_07(1, 3))
    print(select_08(2))
    print(select_09(2))
    print(select_10(3, 2))
    print(select_11(1, 2))
    print(select_12(1, 2))
