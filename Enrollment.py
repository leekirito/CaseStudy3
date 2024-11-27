import pyodbc
from datetime import datetime 
import os 
from tabulate import tabulate
from Course import Course
from Student import Student
from Course import Course
from Payment import Payment


def connect_to_database():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=LIECODEX\\SQLEXPRESS;"
        "DATABASE=E_Learning_Platform;"
        "Trusted_Connection=yes;"
    )

class Enrollment():
    def __init__(self, enrollment_id, student_id, course_id, enrollment_date, status, progress):
        self.enrollment_id = enrollment_id
        self.student_id =student_id
        self.course_id = course_id
        self.enrollment_date = enrollment_date
        self.status = status
        self.progress = progress

    @classmethod
    def get_data(cls):
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Enrollments")
        rows = cursor.fetchall()
        
        # Create Enrollment objects for each row in the database
        enrollments = [
            cls(
                enrollment_id=row.enrollment_id,
                student_id=row.student_id,
                course_id=row.course_id,
                enrollment_date=row.enrollment_date,
                status=row.status,
                progress=row.progress
            )
            for row in rows
        ]
        
        cursor.close()
        conn.close()
        return enrollments

    @classmethod
    def show__all_enrolled_course(cls):
        enrolls = cls.get_data()
        content = []
        for enroll in enrolls:
            content.append([enroll.enrollment_id, enroll.student_id, enroll.course_id, enroll.enrollment_date, enroll.status, enroll.progress])

        header = ["Enrollment ID","Student ID","Course ID","Enrolled Date","Status","Progress",]
        print(tabulate(content, header, tablefmt="pretty"))

    @classmethod
    def show_my_enrolled_course(cls, student_id):
        enrolls = cls.get_data()
        content = []
        for enroll in enrolls:
            if student_id == enroll.student_id:
                content.append([enroll.enrollment_id, enroll.student_id, enroll.course_id, enroll.enrollment_date, enroll.status, enroll.progress])

        header = ["Enrollment ID","Student ID","Course ID","Enrolled Date","Status","Progress",]
        print(tabulate(content, header, tablefmt="pretty"))

    @classmethod
    def take_course(username):
        Course.show_all_courses()
        studetns = Student.get_data()
        student_id = None
        for student in studetns:
            if student.username == username:
                student_id = student.student_id
        Course.show_all_courses()
        course_id = input("Course ID: ")
        course_price = None
        courses = Course.get_data()
        for course in courses:
            if course.course_id == course_id:
                course_price = course.price
                break
        else:#for else logic, else statement will execute if and only if for loop doesn't hit a break statement
            print("Course ID does not exist!")
            return None 
        enrollment_date = datetime.now().date()
        status = "active"
        progress = "0%"
        if not Payment.pay(course_price):
            return None
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Enrollments(student_id, course_id, enrollment_date, status, progress)
            VALUES(?, ?, ?, ?, ?)
        """, (student_id, course_id, enrollment_date, status, progress))
        conn.commit()
        cursor.close()
        conn.close()
        Course.add_student(course_id)
        print("succesfuly took course!")

    @classmethod
    def show_all_student_in_course(cls, course_id):
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("""SELECT Students.username, Students.last_name, Courses.course_name, Enrollments.status, Enrollments.progress FROM Enrollments
                       JOIN Students ON Enrollments.student_id = Students.student_id
                       JOIN Courses ON Enrollments.course_id = Courses.course_id
                       WHERE Enrollments.course_id = ?
                       """, (course_id))
        rows = cursor.fetchall()

        content = []
        for row in rows:
            content.append([row.username, row.last_name, row.course_name, row.status, row.progress])

        header = ["Username", "Last Name","Course Name","Progress","Progress"]

        print(tabulate(content, header, tablefmt="pretty"))

    
