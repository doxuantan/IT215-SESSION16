from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base

# Bảng trung gian Student - Course
student_course = Table(
    "student_course",
    Base.metadata,
    Column("student_id", Integer, ForeignKey("students.id"), primary_key=True),
    Column("course_id", Integer, ForeignKey("courses.id"), primary_key=True),
)


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)

    # Quan hệ 1-N
    students = relationship("Student", back_populates="department")


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)

    # Khóa ngoại tới Department
    department_id = Column(Integer, ForeignKey("departments.id"))
    department = relationship("Department", back_populates="students")

    # Quan hệ 1-1 với Profile
    profile = relationship("Profile", back_populates="student", uselist=False)

    # Quan hệ N-N với Course
    courses = relationship(
        "Course", secondary=student_course, back_populates="students"
    )


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    bio = Column(String(255))

    # Mỗi Student chỉ có một Profile
    student_id = Column(Integer, ForeignKey("students.id"), unique=True)

    student = relationship("Student", back_populates="profile")


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)

    # Quan hệ N-N với Student
    students = relationship(
        "Student", secondary=student_course, back_populates="courses"
    )


# Phần 1: Tóm tắt báo cáo lỗi

# Lỗi 1: Quan hệ 1 - N (Department ↔ Student)

# Lỗi: back_populates khai báo sai.
# Sai:
# students = relationship("Student", back_populates="department_id")
# Đúng:
# students = relationship("Student", back_populates="department")
# Nguyên nhân: department_id là khóa ngoại (Column), không phải thuộc tính relationship.

# Lỗi 2: Quan hệ 1 - 1 (Student ↔ Profile)

# Lỗi: Chưa cấu hình quan hệ 1-1 thực sự.
# Nguyên nhân: Thiếu uselist=False và unique=True, nên SQLAlchemy hiểu thành quan hệ 1-N.
# Cách sửa:
# profile = relationship("Profile", back_populates="student", uselist=False)
# student_id = Column(Integer, ForeignKey("students.id"), unique=True)

# Lỗi 3: Quan hệ N - N (Student ↔ Course)

# Lỗi: Thiếu tham số secondary.
# Nguyên nhân: SQLAlchemy không biết sử dụng bảng trung gian student_course.
# Cách sửa:
# courses = relationship(
#     "Course",
#     secondary=student_course,
#     back_populates="students"
# )
# students = relationship(
#     "Student",
#     secondary=student_course,
#     back_populates="courses"
# )
