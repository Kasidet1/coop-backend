from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models
from .auth import hash_password, verify_password


# ======================
# STUDENT
# ======================

def get_students(db: Session):
    return db.query(models.Student).all()


def create_student(db, student):
    new_student = models.Student(
        student_id=student.student_id,
        first_name=student.first_name,
        last_name=student.last_name,
        faculty=student.faculty,
        major=student.major,
        teacher_id=student.teacher_id
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student


def create_student_user(db, student):
    hashed = hash_password(student.password)

    db_student = models.Student(
        student_id=student.student_id,
        first_name=student.first_name,
        last_name=student.last_name,
        faculty=student.faculty,
        major=student.major,
        password=hashed
    )

    db.add(db_student)
    db.commit()
    db.refresh(db_student)

    return db_student


def update_student(db, student_id, student):
    db_student = db.query(models.Student).filter(
        models.Student.id == student_id
    ).first()

    if db_student:
        db_student.student_id = student.student_id
        db_student.first_name = student.first_name
        db_student.last_name = student.last_name
        db_student.faculty = student.faculty
        db_student.major = student.major

        db.commit()
        db.refresh(db_student)

    return db_student


def delete_student(db, student_id):
    student = db.query(models.Student).filter(
        models.Student.id == student_id
    ).first()

    if student:
        db.delete(student)
        db.commit()

    return student


# ======================
# USER
# ======================

def create_user(db, user):
    hashed_password = hash_password(user.password)

    db_user = models.User(
        email=user.email,
        password=hashed_password,
        role=user.role
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def login_user(db, email, password):
    user = db.query(models.User).filter(
        models.User.email == email
    ).first()

    if not user:
        return None

    if not verify_password(password, user.password):
        return None

    return user


# ======================
# STUDENT LOGIN (JWT)
# ======================

def student_login(db, student_id, password):

    student = db.query(models.Student).filter(
        models.Student.student_id == student_id
    ).first()

    if not student:
        return None

    if not verify_password(password, student.password):
        return None

    return student


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

    if application:
        application.status = status
        db.commit()
        db.refresh(application)

    return application


# Upload PDF
def upload_application_file(db, application_id, file_path):

    application = db.query(models.Application).filter(
        models.Application.id == application_id
    ).first()

    if application:
        application.file = file_path
        db.commit()
        db.refresh(application)

    return application


# ======================
# SUPERVISION
# ======================

def create_supervision(db, supervision):
    db_supervision = models.Supervision(**supervision.dict())

    db.add(db_supervision)
    db.commit()
    db.refresh(db_supervision)

    return db_supervision


def get_supervisions(db):
    return db.query(models.Supervision).all()


# ======================
# TEACHER
# ======================

def get_teacher_students(db, teacher_id):

    return db.query(models.Student).filter(
        models.Student.teacher_id == teacher_id
    ).all()


# ======================
# DASHBOARD
# ======================

def admin_dashboard(db: Session):

    student_count = db.query(func.count(models.Student.id)).scalar()

    company_count = db.query(func.count(models.Company.id)).scalar()

    application_count = db.query(
        func.count(models.Application.id)
    ).scalar()

    return {
        "students": student_count,
        "companies": company_count,
        "applications": application_count
    }


def teacher_dashboard(db: Session, teacher_id):

    student_count = db.query(models.Student).filter(
        models.Student.teacher_id == teacher_id
    ).count()

    supervisions = db.query(models.Supervision).filter(
        models.Supervision.teacher_id == teacher_id
    ).all()

    return {
        "students": student_count,
        "supervisions": supervisions
    }


# ======================
# ASSIGN TEACHER
# ======================

def assign_teacher(db, student_id, teacher_id):
    student = db.query(models.Student).filter(
        models.Student.id == student_id
    ).first()

    if student:
        student.teacher_id = teacher_id
        db.commit()
        db.refresh(student)

    return student


# ======================
# COMPANY CRUD
# ======================

def create_company(db, company):
    db_company = models.Company(**company.dict())

    db.add(db_company)
    db.commit()
    db.refresh(db_company)

    return db_company


def get_companies(db):
    return db.query(models.Company).all()


def update_company(db, company_id, company):
    db_company = db.query(models.Company).filter(
        models.Company.id == company_id
    ).first()

    if db_company:
        db_company.company_name = company.company_name
        db_company.address = company.address
        db_company.industry = company.industry

        db.commit()
        db.refresh(db_company)

    return db_company


def delete_company(db, company_id):
    company = db.query(models.Company).filter(
        models.Company.id == company_id
    ).first()

    if company:
        db.delete(company)
        db.commit()

    return company