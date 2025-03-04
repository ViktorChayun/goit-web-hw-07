from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    students = relationship('Student', back_populates='group')


class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    group_id = Column(Integer, ForeignKey('groups.id', ondelete='CASCADE', onupdate='CASCADE'))
    group = relationship('Group', back_populates='students')
    marks = relationship('StudentMark', back_populates='student')


class Lector(Base):
    __tablename__ = 'lectors'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    subjects = relationship('Subject', back_populates='lector')


class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True)
    subject = Column(String(255), nullable=False)
    lector_id = Column(Integer, ForeignKey('lectors.id', ondelete='SET NULL', onupdate='CASCADE'))
    lector = relationship('Lector', back_populates='subjects')
    marks = relationship('StudentMark', back_populates='subject')


class StudentMark(Base):
    __tablename__ = 'student_marks'
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id', ondelete='CASCADE', onupdate='CASCADE'))
    subject_id = Column(Integer, ForeignKey('subjects.id', ondelete='CASCADE', onupdate='CASCADE'))
    lecture_date = Column(Date, nullable=False)
    mark = Column(Integer)
    student = relationship('Student', back_populates='marks')
    subject = relationship('Subject', back_populates='marks')
