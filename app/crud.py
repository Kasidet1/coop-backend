from sqlalchemy.orm import Session
from sqlalchemy import func, or_

from . import models
from .auth import hash_password, verify_password


# ======================
# STUDENT
# ======================

def get_students(db: Session):

    return db.query(models.Student).all()


def create_student(db, student):

    hashed_password = hash_password(student.password)

    new_student = models.Student(
        student_id=student.student_id,
        first_name=student.first_name,
        last_name=student.last_name,
        faculty=student.faculty,
        major=student.major,
        username=student.username,
        phone=student.phone,
        semester=student.semester,
        password=hashed_password,
        teacher_id=student.teacher_id
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
    db_student.username = student.username
    db_student.phone = student.phone
    db_student.semester = student.semester
    db_student.teacher_id = student.teacher_id

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

def get_student_profile(
    db,
    student_id
):

    return db.query(models.Student).filter(
        models.Student.student_id == student_id
    ).first()


def update_student_profile(
    db,
    student_id,
    student_data
):

    student = db.query(models.Student).filter(
        models.Student.student_id == student_id
    ).first()

    if not student:
        return None

    student.first_name = student_data.first_name
    student.last_name = student_data.last_name
    student.username = student_data.username
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

    hashed_password = hash_password(user.password)

    db_user = models.User(
        username=user.username,
        password=hashed_password,
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

    if not user:
        return None

    if not user.password:
        return None

    if not verify_password(
        password,
        user.password
    ):
        return None

    return user


# ======================
# STUDENT LOGIN
# ======================

def student_login(
    db,
    student_id,
    password
):

    student = db.query(models.Student).filter(
        models.Student.student_id == student_id
    ).first()

    if not student:
        return None

    if not student.password:
        return None

    if not verify_password(
        password,
        student.password
    ):
        return None

    return student


# ======================
# TEACHER
# ======================

def get_teacher_by_username(
    db,
    username
):

    return db.query(models.Teacher).filter(
        models.Teacher.username == username
    ).first()


def get_teacher_students(
    db,
    teacher_id
):

    return db.query(models.Student).filter(
        models.Student.teacher_id == teacher_id
    ).all()


# ======================
# TEACHER PROFILE
# ======================

def get_teacher_profile(
    db,
    username
):

    return db.query(models.Teacher).filter(
        models.Teacher.username == username
    ).first()


def update_teacher_profile(
    db,
    username,
    teacher_data
):

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

def create_application(
    db: Session,
    application
):

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

    return db.query(
        models.Application
    ).all()


def update_application_status(
    db,
    application_id,
    status
):

    application = db.query(
        models.Application
    ).filter(
        models.Application.id == application_id
    ).first()

    if not application:
        return None

    application.status = status

    db.commit()

    db.refresh(application)

    return application


# ======================
# UPLOAD PDF
# ======================

def upload_application_file(
    db,
    application_id,
    file_path
):

    application = db.query(
        models.Application
    ).filter(
        models.Application.id == application_id
    ).first()

    if not application:
        return None

    application.file = file_path

    db.commit()

    db.refresh(application)

    return application


# ======================
# SUPERVISION
# ======================

def create_supervision(
    db,
    supervision
):

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

    return db.query(
        models.Supervision
    ).all()


def get_teacher_supervisions(
    db,
    teacher_id
):

    result = db.query(

        models.Teacher.first_name.label(
            "teacher_first_name"
        ),

        models.Teacher.last_name.label(
            "teacher_last_name"
        ),

        models.Company.company_name,

        models.Company.industry,

        models.Student.student_id,

        models.Student.first_name.label(
            "student_first_name"
        ),

        models.Student.last_name.label(
            "student_last_name"
        ),

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

    student_count = db.query(
        func.count(models.Student.id)
    ).scalar()

    company_count = db.query(
        func.count(models.Company.id)
    ).scalar()

    application_count = db.query(
        func.count(models.Application.id)
    ).scalar()

    supervision_count = db.query(
        func.count(models.Supervision.id)
    ).scalar()

    return {
        "students": student_count,
        "companies": company_count,
        "applications": application_count,
        "supervisions": supervision_count
    }


def teacher_dashboard(
    db: Session,
    teacher_id
):

    student_count = db.query(
        models.Student
    ).filter(
        models.Student.teacher_id == teacher_id
    ).count()

    supervision_count = db.query(
        models.Supervision
    ).filter(
        models.Supervision.teacher_id == teacher_id
    ).count()

    supervisions = get_teacher_supervisions(
        db,
        teacher_id
    )

    return {
        "students": student_count,
        "supervision_count": supervision_count,
        "supervisions": supervisions
    }


# ======================
# ASSIGN TEACHER
# ======================

def assign_teacher(
    db,
    student_id,
    teacher_id
):

    student = db.query(
        models.Student
    ).filter(
        models.Student.id == student_id
    ).first()

    if not student:
        return None

    student.teacher_id = teacher_id

    db.commit()

    db.refresh(student)

    return student


# ======================
# COMPANY CRUD
# ======================

def create_company(
    db,
    company
):

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


# ======================
# SEARCH + FILTER COMPANY
# ======================

def get_companies(
    db,
    search=None,
    county=None,
    industry=None,
    allowance=None,
    accommodation=None,
    shuttle=None
):

    query = db.query(models.Company)

    if search:

        query = query.filter(

            or_(

                models.Company.company_name.ilike(
                    f"%{search}%"
                ),

                models.Company.address.ilike(
                    f"%{search}%"
                ),

                models.Company.county.ilike(
                    f"%{search}%"
                ),

                models.Company.industry.ilike(
                    f"%{search}%"
                )

            )

        )

    if county:

        query = query.filter(
            models.Company.county == county
        )

    if industry:

        query = query.filter(
            models.Company.industry == industry
        )

    if allowance:

        query = query.filter(
            models.Company.allowance == allowance
        )

    if accommodation:

        query = query.filter(
            models.Company.accommodation == accommodation
        )

    if shuttle:

        query = query.filter(
            models.Company.shuttle == shuttle
        )

    return query.all()


def update_company(
    db,
    company_id,
    company
):

    db_company = db.query(
        models.Company
    ).filter(
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


def delete_company(
    db,
    company_id
):

    company = db.query(
        models.Company
    ).filter(
        models.Company.id == company_id
    ).first()

    if not company:
        return None

    db.delete(company)

    db.commit()

    return company
