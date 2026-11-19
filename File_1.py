from ast import List

import psycopg2
from sqlalchemy.util.preloaded import engine_cursor
from sqlalchemy import create_engine, text
from sqlalchemy import String

from sqlalchemy import ForeignKey, String, create_engine, select, text, Integer, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship

DATABASE_URL = 'postgresql+psycopg2://postgres:postgres@localhost:5432/postgres'
engine = create_engine(DATABASE_URL, echo=True)


class Base(DeclarativeBase):
    pass


class Course(Base):
    __tablename__ = "Course"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    price: Mapped[int] = mapped_column(Integer)
    # email: Mapped[str | None] = mapped_column(String(255), unique=True)
    # posts: Mapped[list["Post"]] = relationship(back_populates="author")

    lessons: Mapped[List["Lesson"]] = relationship(back_populates="course")
    enrollments: Mapped[List["Enrollment"]] = relationship(back_populates="course")
    teachers: Mapped[List["Teacher"]] = relationship(
        secondary="course_teacher", back_populates="courses"
    )

class Course_teacher(Base):
    __tablename__ = "Course_teacher"
    teacher_id: Mapped[int] = mapped_column(Integer)
    course_id: Mapped[int] = mapped_column(Integer)


class Enrollment(Base):
    __tablename__ = "enrollment"
    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(Integer)
    course_id: Mapped[int] = mapped_column(Integer)
    price: Mapped[int] = mapped_column(Integer)
    enrollment_date: Mapped[int] = mapped_column(DateTime)

class Lesson(Base):
    __tablename__ = "Lesson"
    id: Mapped[int] = mapped_column(primary_key=True)
    number_lesson: Mapped[int] = mapped_column(Integer)
    theme_lesson: Mapped[int] = mapped_column(String(50))
    course_id: Mapped[int] = mapped_column(Integer)

    course: Mapped[int] = relationship(back_populates="lessons")
    homework: Mapped[int] = relationship(back_populates="lesson")

class Teacher(Base):
    __tablename__ = "Teacher"
    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(50))

    course : mapped_column(Mapped[int]) = relationship(
        secondary="course_teacher", back_populates="teachers"
    )
    homework: Mapped[int] = relationship(back_populates="teacher")

class Student:
    __tablename__ = "Student"
    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(50))

    enrollment: mapped_column(Mapped[int]) = relationship(back_populates="student")
    homeworks: Mapped[List["Homework"]] = relationship(back_populates="student")

class Homework(Base):
    __tablename__ = "Homework"
    id: Mapped[int] = mapped_column(primary_key=True)
    score: Mapped[int] = mapped_column(Integer)
    lesson_id: Mapped[int] = mapped_column(Integer)
    student_id: Mapped[int] = mapped_column(Integer)
    teacher_id: Mapped[int] = mapped_column(Integer)

    lesson: Mapped[int] = relationship(
        back_populates="homeworks"
    )
    student: Mapped[int] = relationship(
        back_populates='homeworks'
    )
    teacher: Mapped[int] = relationship(
        back_populates="homeworks"
    )
