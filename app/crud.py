from sqlalchemy.orm import Session
from sqlalchemy import func, or_

from . import models


# ============================================================
# STUDENT
# ============================================================

def get_students(db: Session):
    return db.query(models.Student).all()


def get_student_by_student_id(
    db: Session,
    student_id
):
    return db.query(
        models.Student
    ).filter(
        models.Student.student_id == student_id
    ).first()


def create_student(
    db: Session,
    student
):
    new_student = models.Student(
        student_id=student.student_id,
        first_name=student.first_name,
        last_name=student.last_name,
        faculty=student.faculty,
        major=student.major,
        phone=student.phone,
        semester=student.semester
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student


def update_student(
    db: Session,
    student_id,
    student
):
    db_student = db.query(
        models.Student
    ).filter(
        models.Student.id == student_id
    ).first()

    if not db_student:
        return None

    db_student.student_id = student.student_id
    db_student.first_name = student.first_name
    db_student.last_name = student.last_name
    db_student.faculty = student.faculty
    db_student.major = student.major
    db_student.phone = student.phone
    db_student.semester = student.semester

    db.commit()
    db.refresh(db_student)

    return db_student


def delete_student(
    db: Session,
    student_id
):
    student = db.query(
        models.Student
    ).filter(
        models.Student.id == student_id
    ).first()

    if not student:
        return None

    db.delete(student)
    db.commit()

    return student


# ============================================================
# STUDENT PROFILE
# ============================================================

def get_student_profile(
    db: Session,
    student_id
):
    return db.query(
        models.Student
    ).filter(
        models.Student.student_id == student_id
    ).first()


def update_student_profile(
    db: Session,
    student_id,
    student_data
):
    student = db.query(
        models.Student
    ).filter(
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


# ============================================================
# USER
# ============================================================

def get_users(db: Session):
    return db.query(
        models.User
    ).all()


def create_user(
    db: Session,
    user
):
    db_user = models.User(
        username=user.username,
        password=user.password,
        role=user.role
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def login_user(
    db: Session,
    username,
    password
):

    # --------------------------------------------------------
    # LOGIN USER
    # --------------------------------------------------------

    user = db.query(
        models.User
    ).filter(
        models.User.username == username
    ).first()

    if user and password == user.password:
        return user

    # --------------------------------------------------------
    # LOGIN STUDENT
    # --------------------------------------------------------

    student = db.query(
        models.Student
    ).filter(
        models.Student.student_id == username
    ).first()

    # --------------------------------------------------------
    # IMPORTANT
    #
    # ตอนนี้ Student model ไม่มี password
    # ดังนั้นไม่ตรวจ student.password
    #
    # ถ้าระบบของคุณมี password ใน database จริง
    # ต้องเพิ่ม Column password ใน models.Student ก่อน
    # --------------------------------------------------------

    return None


def update_user_role(
    db: Session,
    user_id: int,
    role: str
):
    user = db.query(
        models.User
    ).filter(
        models.User.id == user_id
    ).first()

    if not user:
        return None

    user.role = role

    db.commit()
    db.refresh(user)

    return user


# ============================================================
# TEACHER
# ============================================================

def get_teacher_by_username(
    db: Session,
    username
):
    return db.query(
        models.Teacher
    ).filter(
        models.Teacher.username == username
    ).first()


def get_teacher_profile(
    db: Session,
    username
):
    return db.query(
        models.Teacher
    ).filter(
        models.Teacher.username == username
    ).first()


def update_teacher_profile(
    db: Session,
    username,
    teacher_data
):
    teacher = db.query(
        models.Teacher
    ).filter(
        models.Teacher.username == username
    ).first()

    if not teacher:
        return None

    teacher.username = teacher_data.username
    teacher.rank = teacher_data.rank
    teacher.first_name = teacher_data.first_name
    teacher.last_name = teacher_data.last_name

    # ไม่ให้ Teacher เปลี่ยน role ของตัวเอง
    # teacher.role = teacher_data.role

    db.commit()
    db.refresh(teacher)

    return teacher


# ============================================================
# TEACHER STUDENTS
# ============================================================

def create_teacher_student(
    db: Session,
    teacher_student,
    teacher_name: str
):
    """
    สร้างข้อมูลนักศึกษาที่อาจารย์ดูแล

    teacher_name ต้องมาจาก Backend
    ไม่รับจาก Frontend เพื่อป้องกัน
    การสร้างข้อมูลในชื่ออาจารย์คนอื่น
    """

    db_teacher_student = models.TeacherStudent(

        teacher_name=teacher_name,

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


def get_all_teacher_students(
    db: Session
):
    """
    Admin ใช้ดูนักศึกษาที่อาจารย์ทุกคนดูแล
    """

    return db.query(
        models.TeacherStudent
    ).all()


def get_teacher_students(
    db: Session,
    teacher_name: str
):
    """
    Teacher ใช้ดูเฉพาะนักศึกษาที่ตัวเองดูแล
    """

    return db.query(
        models.TeacherStudent
    ).filter(
        models.TeacherStudent.teacher_name ==
        teacher_name
    ).all()


def get_teacher_student_by_id(
    db: Session,
    teacher_student_id: int,
    teacher_name: str
):
    """
    ดึงข้อมูลนักศึกษาที่อาจารย์ดูแล
    และต้องเป็นของอาจารย์คนนี้เท่านั้น
    """

    return db.query(
        models.TeacherStudent
    ).filter(
        models.TeacherStudent.id ==
        teacher_student_id,
        models.TeacherStudent.teacher_name ==
        teacher_name
    ).first()


def update_teacher_student(
    db: Session,
    teacher_student_id: int,
    teacher_student,
    teacher_name: str
):
    """
    Teacher แก้ไขได้เฉพาะนักศึกษาของตัวเอง
    """

    db_teacher_student = db.query(
        models.TeacherStudent
    ).filter(
        models.TeacherStudent.id ==
        teacher_student_id,
        models.TeacherStudent.teacher_name ==
        teacher_name
    ).first()

    if not db_teacher_student:
        return None

    # ไม่ให้เปลี่ยน teacher_name

    db_teacher_student.company_name = (
        teacher_student.company_name
    )

    db_teacher_student.student_id = (
        teacher_student.student_id
    )

    db_teacher_student.student_name = (
        teacher_student.student_name
    )

    db_teacher_student.department = (
        teacher_student.department
    )

    db_teacher_student.industry = (
        teacher_student.industry
    )

    db_teacher_student.work_modes = (
        teacher_student.work_modes
    )

    db.commit()
    db.refresh(db_teacher_student)

    return db_teacher_student


def delete_teacher_student(
    db: Session,
    teacher_student_id: int,
    teacher_name: str
):
    """
    Teacher ลบได้เฉพาะนักศึกษาของตัวเอง
    """

    db_teacher_student = db.query(
        models.TeacherStudent
    ).filter(
        models.TeacherStudent.id ==
        teacher_student_id,
        models.TeacherStudent.teacher_name ==
        teacher_name
    ).first()

    if not db_teacher_student:
        return None

    db.delete(db_teacher_student)
    db.commit()

    return db_teacher_student


def get_student_teacher(
    db: Session,
    student_name: str
):
    """
    ค้นหาอาจารย์ที่ดูแลนักศึกษาจากชื่อนักศึกษา
    """

    return db.query(
        models.TeacherStudent
    ).filter(
        models.TeacherStudent.student_name ==
        student_name
    ).all()


# ============================================================
# APPLICATION
# ============================================================

def create_application(
    db: Session,
    application,
    user
):
    # ==============================
    # หา Student จาก JWT
    # user["sub"] = student_id
    # เช่น "65100521"
    # ==============================

    student = db.query(
        models.Student
    ).filter(
        models.Student.student_id == str(user["sub"])
    ).first()

    if not student:
        return None

    # ==============================
    # ตรวจสอบบริษัท
    # ==============================

    company = db.query(
        models.Company
    ).filter(
        models.Company.id == application.company_id
    ).first()

    if not company:
        return None

    # ==============================
    # สร้างใบสมัคร
    #
    # applications.student_id
    # = students.id
    # ==============================

    db_application = models.Application(
        student_id=student.id,
        company_id=company.id,
        status="pending"
    )

    db.add(db_application)
    db.commit()
    db.refresh(db_application)

    return db_application


def get_applications(
    db: Session
):
    applications = db.query(
        models.Application
    ).all()

    results = []

    for application in applications:

        student = db.query(
            models.Student
        ).filter(
            models.Student.id ==
            application.student_id
        ).first()

        company = db.query(
            models.Company
        ).filter(
            models.Company.id ==
            application.company_id
        ).first()

        results.append({

            "application_id":
                application.id,

            "student_id":
                student.student_id
                if student
                else None,

            "first_name":
                student.first_name
                if student
                else None,

            "last_name":
                student.last_name
                if student
                else None,

            "student_name":
                (
                    f"{student.first_name} "
                    f"{student.last_name}"
                )
                if student
                else None,

            "company_name":
                company.company_name
                if company
                else None,

            "status":
                application.status
        })

    return results


def update_application_status(
    db: Session,
    application_id,
    status
):
    application = db.query(
        models.Application
    ).filter(
        models.Application.id ==
        application_id
    ).first()

    if not application:
        return None

    application.status = status

    db.commit()
    db.refresh(application)

    return application


# ============================================================
# SUPERVISION
# ============================================================

def create_supervision(
    db: Session,
    supervision,
    teacher
):
    # ========================================================
    # 1. หา teacher จาก username ที่ Login อยู่
    # ========================================================

    db_teacher = db.query(
        models.Teacher
    ).filter(
        models.Teacher.username == teacher["sub"]
    ).first()

    if not db_teacher:
        return None, "Teacher not found"

    teacher_name = (
        f"{db_teacher.first_name} "
        f"{db_teacher.last_name}"
    )

    # ========================================================
    # 2. ตรวจว่านักศึกษาคนนี้อยู่ใน teacher_students
    #    ของอาจารย์คนนี้จริงหรือไม่
    # ========================================================

    assigned_student = db.query(
        models.TeacherStudent
    ).filter(
        models.TeacherStudent.teacher_name
        == teacher_name,

        models.TeacherStudent.student_id
        == supervision.student_id
    ).first()

    if not assigned_student:
        return None, "Student is not assigned to this teacher"

    # ========================================================
    # 3. หา Student จาก student_id
    #    เช่น 65123481
    # ========================================================

    db_student = db.query(
        models.Student
    ).filter(
        models.Student.student_id
        == supervision.student_id
    ).first()

    if not db_student:
        return None, "Student not found"

    # ========================================================
    # 4. สร้าง supervision
    #
    # student_id ใน supervisions ต้องใช้ students.id
    # ========================================================

    db_supervision = models.Supervision(
        teacher_id=db_teacher.id,
        student_id=db_student.id,
        company_id=supervision.company_id,
        date=supervision.date,
        type=supervision.type,
        note=supervision.note,
        status=supervision.status
    )

    db.add(db_supervision)
    db.commit()
    db.refresh(db_supervision)

    return db_supervision, None


def get_supervisions(
    db: Session
):
    return db.query(
        models.Supervision
    ).all()


# ============================================================
# TEACHER SUPERVISIONS
# ============================================================

def get_teacher_supervisions(db: Session, teacher_name: str):

    rows = db.query(
        models.TeacherStudent.student_id.label("student_id"),
        models.TeacherStudent.student_name.label("student_name"),
        models.TeacherStudent.company_name.label("company_name"),
        models.TeacherStudent.department.label("department"),
        models.TeacherStudent.industry.label("industry"),
        models.TeacherStudent.work_modes.label("work_modes"),

        models.Supervision.id.label("supervision_id"),
        models.Supervision.date.label("date"),
        models.Supervision.type.label("type"),
        models.Supervision.status.label("status"),
        models.Supervision.note.label("note")

    ).select_from(
        models.TeacherStudent

    ).outerjoin(
        models.Student,
        models.TeacherStudent.student_id
        == models.Student.student_id

    ).outerjoin(
        models.Supervision,
        models.Supervision.student_id
        == models.Student.id

    ).filter(
        models.TeacherStudent.teacher_name
        == teacher_name
    ).all()

    result = []

    for row in rows:

        result.append({
            "student_id": row.student_id,
            "student_name": row.student_name,
            "company_name": row.company_name,
            "department": row.department,
            "industry": row.industry,
            "work_modes": row.work_modes,

            "supervision_id": row.supervision_id,
            "date": row.date,
            "type": row.type,
            "status": row.status,
            "note": row.note
        })

    return result

def get_all_supervisions(db: Session):

    rows = db.query(
        models.Supervision.id.label("supervision_id"),

        models.Teacher.first_name.label("teacher_first_name"),
        models.Teacher.last_name.label("teacher_last_name"),

        models.Student.student_id.label("student_id"),
        models.Student.first_name.label("student_first_name"),
        models.Student.last_name.label("student_last_name"),

        models.Company.company_name.label("company_name"),
        models.Company.industry.label("industry"),

        models.Supervision.date.label("date"),
        models.Supervision.type.label("type"),
        models.Supervision.status.label("status"),
        models.Supervision.note.label("note")

    ).join(
        models.Teacher,
        models.Supervision.teacher_id == models.Teacher.id
    ).join(
        models.Student,
        models.Supervision.student_id == models.Student.id
    ).join(
        models.Company,
        models.Supervision.company_id == models.Company.id
    ).order_by(
        models.Supervision.date.desc()
    ).all()

    result = []

    for row in rows:
        result.append({
            "supervision_id": row.supervision_id,

            "teacher_name": (
                f"{row.teacher_first_name} "
                f"{row.teacher_last_name}"
            ),

            "student_id": row.student_id,

            "student_name": (
                f"{row.student_first_name} "
                f"{row.student_last_name}"
            ),

            "company_name": row.company_name,
            "industry": row.industry,

            "date": row.date,
            "type": row.type,
            "status": row.status,
            "note": row.note
        })

    return result

# ============================================================
# TEACHER DASHBOARD
# ============================================================

def teacher_dashboard(
    db: Session,
    teacher_name: str
):
    """
    Dashboard ของ Teacher

    students:
        จำนวนคนที่อาจารย์ดูแล
        จาก teacher_students

    supervision_count:
        จำนวนการนิเทศของอาจารย์

    supervisions:
        ประวัติการนิเทศ
        ของนักศึกษาที่อาจารย์ดูแล
    """

    # --------------------------------------------------------
    # นักศึกษาที่อาจารย์ดูแล
    # --------------------------------------------------------

    students = get_teacher_students(
        db,
        teacher_name
    )

    # --------------------------------------------------------
    # หา Teacher
    # --------------------------------------------------------

    teacher = db.query(
        models.Teacher
    ).filter(
        models.Teacher.first_name +
        " " +
        models.Teacher.last_name ==
        teacher_name
    ).first()

    supervision_count = 0
    supervisions = []

    if teacher:

        # ----------------------------------------------------
        # จำนวน supervision
        # ----------------------------------------------------

        supervision_count = db.query(
            models.Supervision
        ).filter(
            models.Supervision.teacher_id ==
            teacher.id
        ).count()

        # ----------------------------------------------------
        # ประวัติ supervision
        #
        # อิง teacher_students
        # ----------------------------------------------------

        supervisions = get_teacher_supervisions(
            db,
            teacher_name
        )

    return {

        "students":
            len(students),

        "supervision_count":
            supervision_count,

        "supervisions":
            supervisions
    }


# ============================================================
# ADMIN DASHBOARD
# ============================================================

def admin_dashboard(
    db: Session
):
    return {

        "students":
            db.query(
                func.count(
                    models.Student.id
                )
            ).scalar(),

        "companies":
            db.query(
                func.count(
                    models.Company.id
                )
            ).scalar(),

        "applications":
            db.query(
                func.count(
                    models.Application.id
                )
            ).scalar(),

        "supervisions":
            db.query(
                func.count(
                    models.Supervision.id
                )
            ).scalar()
    }


# ============================================================
# COMPANY
# ============================================================

def create_company(
    db: Session,
    company
):
    db_company = models.Company(

        company_name=
            company.company_name,

        address=
            company.address,

        county=
            company.county,

        industry=
            company.industry,

        allowance=
            company.allowance,

        accommodation=
            company.accommodation,

        shuttle=
            company.shuttle,

        welfare=
            company.welfare
    )

    db.add(db_company)
    db.commit()
    db.refresh(db_company)

    return db_company


def get_companies(
    db: Session,
    search=None,
    county=None,
    industry=None,
    allowance=None,
    accommodation=None,
    shuttle=None
):

    query = db.query(
        models.Company
    )

    # --------------------------------------------------------
    # Search
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # County
    # --------------------------------------------------------

    if county:

        query = query.filter(
            models.Company.county == county
        )

    # --------------------------------------------------------
    # Industry
    # --------------------------------------------------------

    if industry:

        query = query.filter(
            models.Company.industry == industry
        )

    # --------------------------------------------------------
    # Allowance
    # --------------------------------------------------------

    if allowance:

        query = query.filter(
            models.Company.allowance == allowance
        )

    # --------------------------------------------------------
    # Accommodation
    # --------------------------------------------------------

    if accommodation:

        query = query.filter(
            models.Company.accommodation ==
            accommodation
        )

    # --------------------------------------------------------
    # Shuttle
    # --------------------------------------------------------

    if shuttle:

        query = query.filter(
            models.Company.shuttle ==
            shuttle
        )

    return query.all()


def update_company(
    db: Session,
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

    db_company.company_name = (
        company.company_name
    )

    db_company.address = (
        company.address
    )

    db_company.county = (
        company.county
    )

    db_company.industry = (
        company.industry
    )

    db_company.allowance = (
        company.allowance
    )

    db_company.accommodation = (
        company.accommodation
    )

    db_company.shuttle = (
        company.shuttle
    )

    db_company.welfare = (
        company.welfare
    )

    db.commit()
    db.refresh(db_company)

    return db_company


def delete_company(
    db: Session,
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
