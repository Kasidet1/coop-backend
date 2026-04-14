from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from .database import Base


# ======================
# USER
# ======================

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    password = Column(String)
    role = Column(String)


# ======================
# STUDENT
# ======================

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    faculty = Column(String)
    major = Column(String)

    password = Column(String)

    teacher_id = Column(Integer, ForeignKey("teachers.id"))

    # relationship
    teacher = relationship("Teacher", back_populates="students")
    applications = relationship("Application", back_populates="student")
    supervisions = relationship("Supervision", back_populates="student")


# ======================
# COMPANY
# ======================

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String)
    address = Column(String)
    industry = Column(String)

    applications = relationship("Application", back_populates="company")


# ======================
# APPLICATION
# ======================

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)

    student_id = Column(Integer, ForeignKey("students.id"))
    company_id = Column(Integer, ForeignKey("companies.id"))

    status = Column(String, default="pending")

    # upload pdf
    file = Column(String)

    student = relationship("Student", back_populates="applications")
    company = relationship("Company", back_populates="applications")


# ======================
# TEACHER
# ======================

class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    faculty = Column(String)

    students = relationship("Student", back_populates="teacher")
    supervisions = relationship("Supervision", back_populates="teacher")


# ======================
# SUPERVISION
# ======================

class Supervision(Base):
    __tablename__ = "supervisions"

    id = Column(Integer, primary_key=True, index=True)

    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    student_id = Column(Integer, ForeignKey("students.id"))

    date = Column(Date)

    # onsite / online
    type = Column(String)

    note = Column(String)
    status = Column(String)

    teacher = relationship("Teacher", back_populates="supervisions")
    student = relationship("Student", back_populates="supervisions")