from sqlalchemy.orm import Session
from sqlalchemy import func, or_

from . import models


# ======================
# STUDENT
# ======================

def get_students(db: Session):
    return db.query(models.Student).all()


def get_student_by_student_id(db, student_id):
    return db.query(models.Student).filter(
        models.Student.student_id == student_id
    ).first()


def create_student(db, student):

    new_student = models.Student(
        student_id=student.student_id,
        first_name=student.first_name,
        last_name=student.last_name,
        faculty=student.faculty,
        major=student.major,
        username=student.student_id,
        phone=student.phone,
        semester=student.semester,
        password=student.password
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student


def update_student(db, student_id, student):

    db_student = db.query(models.Student).filter(
        models.Student.id == student_id
    ).first()

    if not db_student:
        return None

    db_student.student_id = student.student_id
    db_student.first_name = student.first_name
    db_student.last_name = student.last_name
    db_student.faculty = student.faculty
    db_student.major = student.major
    db_student.username = student.student_id
    db_student.phone = student.phone
    db_student.semester = student.semester
    db_student.password = student.password

    db.commit()
    db.refresh(db_student)

    return db_student


def delete_student(db, student_id):

    student = db.query(models.Student).filter(
        models.Student.id == student_id
    ).first()

    if not student:
        return None

    db.delete(student)
    db.commit()

    return student


# ======================
# STUDENT PROFILE
# ======================

def get_student_profile(db, student_id):

    return db.query(models.Student).filter(
        models.Student.student_id == student_id
    ).first()


def update_student_profile(db, student_id, student_data):

    student = db.query(models.Student).filter(
        models.Student.student_id == student_id
    ).first()

    if not student:
        return None

    student.first_name = student_data.first_name
    student.last_name = student_data.last_name
    student.phone = student_data.phone
    student.faculty = student_data.faculty
    student.major = student_data.major
    student.semester = student_data.semester

    db.commit()
    db.refresh(student)

    return student


# ======================
# USER
# ======================

def create_user(db, user):

    db_user = models.User(
        username=user.username,
        password=user.password,
        role=user.role
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def login_user(db, username, password):

    user = db.query(models.User).filter(
        models.User.username == username
    ).first()

    if user and password == user.password:
        return user

    student = db.query(models.Student).filter(
        models.Student.student_id == username
    ).first()

    if student and password == student.password:
        student.role = "student"
        return student

    return None


# ======================
# TEACHER
# ======================

def get_teacher_by_username(db, username):
    return db.query(models.Teacher).filter(
        models.Teacher.username == username
    ).first()


def get_teacher_students(db, teacher_id):
    # ❌ teacher_id relationship removed → return empty or all students
    return []


# ======================
# TEACHER PROFILE
# ======================

def get_teacher_profile(db, username):

    return db.query(models.Teacher).filter(
        models.Teacher.username == username
    ).first()


def update_teacher_profile(db, username, teacher_data):

    teacher = db.query(models.Teacher).filter(
        models.Teacher.username == username
    ).first()

    if not teacher:
        return None

    teacher.username = teacher_data.username
    teacher.rank = teacher_data.rank
    teacher.first_name = teacher_data.first_name
    teacher.last_name = teacher_data.last_name
    teacher.role = teacher_data.role

    db.commit()
    db.refresh(teacher)

    return teacher


# ======================
# APPLICATION
# ======================

def create_application(db: Session, application):

    db_application = models.Application(
        student_id=application.student_id,
        company_id=application.company_id,
        status="pending"
    )

    db.add(db_application)
    db.commit()
    db.refresh(db_application)

    return db_application


def get_applications(db: Session):

    return db.query(models.Application).all()


def update_application_status(db, application_id, status):

    application = db.query(models.Application).filter(
        models.Application.id == application_id
    ).first()

    if not application:
        return None

    application.status = status

    db.commit()
    db.refresh(application)

    return application


# ======================
# SUPERVISION
# ======================

def create_supervision(db, supervision):

    db_supervision = models.Supervision(
        teacher_id=supervision.teacher_id,
        student_id=supervision.student_id,
        company_id=supervision.company_id,
        date=supervision.date,
        type=supervision.type,
        note=supervision.note,
        status=supervision.status
    )

    db.add(db_supervision)
    db.commit()
    db.refresh(db_supervision)

    return db_supervision


def get_supervisions(db):

    return db.query(models.Supervision).all()


def get_teacher_supervisions(db, teacher_id):

    result = db.query(
        models.Teacher.first_name.label("teacher_first_name"),
        models.Teacher.last_name.label("teacher_last_name"),
        models.Company.company_name,
        models.Company.industry,
        models.Student.student_id,
        models.Student.first_name.label("student_first_name"),
        models.Student.last_name.label("student_last_name"),
        models.Supervision.date,
        models.Supervision.type,
        models.Supervision.status
    ).join(
        models.Supervision,
        models.Supervision.teacher_id == models.Teacher.id
    ).join(
        models.Student,
        models.Supervision.student_id == models.Student.id
    ).join(
        models.Company,
        models.Supervision.company_id == models.Company.id
    ).filter(
        models.Teacher.id == teacher_id
    ).all()

    return result


# ======================
# DASHBOARD
# ======================

def admin_dashboard(db: Session):

    return {
        "students": db.query(func.count(models.Student.id)).scalar(),
        "companies": db.query(func.count(models.Company.id)).scalar(),
        "applications": db.query(func.count(models.Application.id)).scalar(),
        "supervisions": db.query(func.count(models.Supervision.id)).scalar()
    }


def teacher_dashboard(db: Session, teacher_id):

    return {
        "students": 0,  # ❌ removed teacher_id relation
        "supervision_count": db.query(models.Supervision).filter(
            models.Supervision.teacher_id == teacher_id
        ).count(),
        "supervisions": get_teacher_supervisions(db, teacher_id)
    }


# ======================
# COMPANY
# ======================

def create_company(db, company):

    db_company = models.Company(
        company_name=company.company_name,
        address=company.address,
        county=company.county,
        industry=company.industry,
        allowance=company.allowance,
        accommodation=company.accommodation,
        shuttle=company.shuttle,
        welfare=company.welfare
    )

    db.add(db_company)
    db.commit()
    db.refresh(db_company)

    return db_company


def get_companies(db, search=None, county=None, industry=None,
                  allowance=None, accommodation=None, shuttle=None):

    query = db.query(models.Company)

    if search:
        query = query.filter(
            or_(
                models.Company.company_name.ilike(f"%{search}%"),
                models.Company.address.ilike(f"%{search}%"),
                models.Company.county.ilike(f"%{search}%"),
                models.Company.industry.ilike(f"%{search}%")
            )
        )

    if county:
        query = query.filter(models.Company.county == county)

    if industry:
        query = query.filter(models.Company.industry == industry)

    if allowance:
        query = query.filter(models.Company.allowance == allowance)

    if accommodation:
        query = query.filter(models.Company.accommodation == accommodation)

    if shuttle:
        query = query.filter(models.Company.shuttle == shuttle)

    return query.all()


def update_company(db, company_id, company):

    db_company = db.query(models.Company).filter(
        models.Company.id == company_id
    ).first()

    if not db_company:
        return None

    db_company.company_name = company.company_name
    db_company.address = company.address
    db_company.county = company.county
    db_company.industry = company.industry
    db_company.allowance = company.allowance
    db_company.accommodation = company.accommodation
    db_company.shuttle = company.shuttle
    db_company.welfare = company.welfare

    db.commit()
    db.refresh(db_company)

    return db_company


def delete_company(db, company_id):

    company = db.query(models.Company).filter(
        models.Company.id == company_id
    ).first()

    if not company:
        return None

    db.delete(company)
    db.commit()

    return company

# ======================
# TEACHER STUDENTS
# ======================

def create_teacher_student(db: Session, teacher_student):

    db_teacher_student = models.TeacherStudent(
        teacher_name=teacher_student.teacher_name,
        company_name=teacher_student.company_name,
        student_id=teacher_student.student_id,
        student_name=teacher_student.student_name,
        department=teacher_student.department,
        industry=teacher_student.industry,
        work_modes=teacher_student.work_modes
    )

    db.add(db_teacher_student)
    db.commit()
    db.refresh(db_teacher_student)

    return db_teacher_student


def get_all_teacher_students(db: Session):

    return db.query(models.TeacherStudent).all()


def get_teacher_student_by_id(db: Session, teacher_student_id):

    return db.query(models.TeacherStudent).filter(
        models.TeacherStudent.id == teacher_student_id
    ).first()


def update_teacher_student(db: Session, teacher_student_id, teacher_student):

    db_teacher_student = db.query(models.TeacherStudent).filter(
        models.TeacherStudent.id == teacher_student_id
    ).first()

    if not db_teacher_student:
        return None

    db_teacher_student.teacher_name = teacher_student.teacher_name
    db_teacher_student.company_name = teacher_student.company_name
    db_teacher_student.student_id = teacher_student.student_id
    db_teacher_student.student_name = teacher_student.student_name
    db_teacher_student.department = teacher_student.department
    db_teacher_student.industry = teacher_student.industry
    db_teacher_student.work_modes = teacher_student.work_modes

    db.commit()
    db.refresh(db_teacher_student)

    return db_teacher_student


def delete_teacher_student(db: Session, teacher_student_id):

    db_teacher_student = db.query(models.TeacherStudent).filter(
        models.TeacherStudent.id == teacher_student_id
    ).first()

    if not db_teacher_student:
        return None

    db.delete(db_teacher_student)
    db.commit()

    return db_teacher_student
