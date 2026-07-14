# Phần 1: Báo cáo lỗi cấu hình
# Lỗi 1: Quan hệ 1 - N (Department ↔ Employee)
# Lỗi: Sai back_populates.
# Sai:
# employees = relationship("Employee", back_populates="department_id")
# Nguyên nhân: department_id là khóa ngoại (Column), không phải thuộc tính relationship.
# Cách sửa:
# employees = relationship("Employee", back_populates="department")
# Lỗi 2: Quan hệ 1 - 1 (Employee ↔ Device)
# Lỗi: Chưa cấu hình quan hệ 1-1 thực sự.
# Nguyên nhân: Thiếu uselist=False và unique=True, nên SQLAlchemy hiểu thành quan hệ 1-N.
# Cách sửa:
# device = relationship("Device", back_populates="employee", uselist=False)
# employee_id = Column(Integer, ForeignKey("employees.id"), unique=True)
# Lỗi 3: Quan hệ N - N (Employee ↔ Project)
# Lỗi: Thiếu tham số secondary.
# Nguyên nhân: SQLAlchemy không biết sử dụng bảng trung gian employee_project.
# Cách sửa:
# projects = relationship(
#     "Project",
#     secondary=employee_project,
#     back_populates="employees"
# )
# employees = relationship(
#     "Employee",
#     secondary=employee_project,
#     back_populates="projects"
# )

from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base

# Bảng trung gian Employee - Project
employee_project = Table(
    "employee_project",
    Base.metadata,
    Column("employee_id", Integer, ForeignKey("employees.id"), primary_key=True),
    Column("project_id", Integer, ForeignKey("projects.id"), primary_key=True),
)


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)

    employees = relationship("Employee", back_populates="department")


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)

    department_id = Column(Integer, ForeignKey("departments.id"))
    department = relationship("Department", back_populates="employees")

    # Quan hệ 1-1
    device = relationship("Device", back_populates="employee", uselist=False)

    # Quan hệ N-N
    projects = relationship(
        "Project", secondary=employee_project, back_populates="employees"
    )


class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    serial_number = Column(String(50), unique=True, nullable=False)

    employee_id = Column(Integer, ForeignKey("employees.id"), unique=True)

    employee = relationship("Employee", back_populates="device")


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)

    employees = relationship(
        "Employee", secondary=employee_project, back_populates="projects"
    )
