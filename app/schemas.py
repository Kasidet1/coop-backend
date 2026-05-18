from pydantic import BaseModel
from datetime import date
from typing import Optional, List


# ======================
# USER
# ======================

class UserCreate(BaseModel):
    username: str
    password: str
    role: str


class User(BaseModel):
    id: int
    username: str
    role: str

    class Config:
        from_attributes = True


# ======================
# LOGIN
# ======================

class Login(BaseModel):
    username: str
    password: str


# ======================
# STUDENT
# ======================

class StudentCreate(BaseModel):
    student_id: str
    first_name: str
    last_name: str
    faculty: str
    major: str
    email: str
    phone: str
    semester: str
    teacher_id: Optional[int] = None


class StudentRegister(BaseModel):
    student_id: str
    first_name: str
    last_name: str
    faculty: str
    major: str
    email: str
    phone: str
    semester: str
    password: str


class Student(BaseModel):
    id: int
    student_id: str
    first_name: str
    last_name: str
    faculty: str
    major: str
    email: str
    phone: str
    semester: str
    teacher_id: Optional[int] = None

    class Config:
        from_attributes = True


# ======================
# TEACHER
# ======================

class TeacherCreate(BaseModel):
    username: str
    rank: str
    first_name: str
    last_name: str
    email: str
    role: str


class Teacher(BaseModel):
    id: int
    username: str
    rank: str
    first_name: str
    last_name: str
    email: str
    role: str

    class Config:
        from_attributes = True


class TeacherUpdate(BaseModel):
    username: str
    rank: str
    first_name: str
    last_name: str
    email: str
    role: str


# ======================
# COMPANY
# ======================

class CompanyCreate(BaseModel):
    company_name: str
    address: str
    county: str
    industry: str
    allowance: str
    accommodation: str
    shuttle: str
    welfare: str


class Company(BaseModel):
    id: int
    company_name: str
    address: str
    county: str
    industry: str
    allowance: str
    accommodation: str
    shuttle: str
    welfare: str

    class Config:
        from_attributes = True


# ======================
# APPLICATION
# ======================

class ApplicationCreate(BaseModel):
    student_id: int
    company_id: int


class Application(BaseModel):
    id: int
    student_id: int
    company_id: int
    status: str

    class Config:
        from_attributes = True


# ======================
# SUPERVISION
# ======================

class SupervisionCreate(BaseModel):
    teacher_id: int
    student_id: int
    company_id: int

    date: date
    type: str
    note: str
    status: str


class Supervision(BaseModel):
    id: int

    teacher_id: int
    student_id: int
    company_id: int

    date: date
    type: str
    note: str
    status: str

    class Config:
        from_attributes = True


# ======================
# TEACHER SUPERVISION
# ======================

class TeacherSupervision(BaseModel):

    teacher_first_name: str
    teacher_last_name: str

    company_name: str
    industry: str

    student_id: str

    student_first_name: str
    student_last_name: str

    date: date
    type: str
    status: str

    class Config:
        from_attributes = True


# ======================
# DASHBOARD
# ======================

class AdminDashboard(BaseModel):
    students: int
    companies: int
    applications: int
    supervisions: int


class TeacherDashboard(BaseModel):
    students: int
    supervision_count: int
    supervisions: List[TeacherSupervision]


# ======================
# ASSIGN TEACHER
# ======================

class AssignTeacher(BaseModel):
    student_id: int
    teacher_id: int
