from Instructor import Instructor
from Student import Student
import pyodbc
import uuid
import getpass
from Course import Course

def connect_to_database():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER= LIECODEX\\SQLEXPRESS;"
        "DATABASE=E_Learning_Platform;"
        "Trusted_Connection=yes;"
    )

class Register():

    @classmethod
    def register_student(cls):
        students = Student.get_data()
        student_id = str(uuid.uuid4())
        username = input("Enter username: ")
        for student in students:
            if student.username == username:
                print("Username alread Exists!!")
                return
        password = getpass.getpass("Enter Password: ")
        con_password = getpass.getpass("Confirm Password: ")
        if password != con_password: 
            print("Password don't match") 
            return
        last_name = input("Enter Last Name: ")
        first_name = input("Enter First Name: ")
        middle_name = input("Enter Middle Name: ")
        age = int(input("Enter Age: "))  # Age should be an integer
        contact_number = input("Enter Contact Number: ")
        gender = input("Enter Gender (Male/Female/Other): ")
        email = input("Enter Email: ")
        address = input("Enter Address: ")
        total_courses = 0
        date_of_birth = input("Enter Date of Birth (YYYY-MM-DD): ")  # Date format string
        access_level = input("Enter Access Level (e.g., free, premuim): ")
        account_status = "Active"
        average_study_time = input("Enter Average Study Time (hours per week): ")  # Average study time 
        conn = connect_to_database()  
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Students(student_id, username, password, last_name, first_name, middle_name, age, contact_number, gender, email, address, total_courses, date_of_birth, access_level, account_status, average_study_time)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ? ,?, ?, ?, ?, ? ,?, ?)
        """, (student_id, username, password, last_name, first_name, middle_name, age, contact_number, gender, email, address, total_courses, date_of_birth, access_level, account_status, average_study_time))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Here's your student ID, please keep this confidential{student_id}, registred successfully!")

    @classmethod
    def register_instructor(cls):
        instructors = Instructor.get_data()
        instructor_id = str(uuid.uuid4())
        username = input("Enter username: ")
        for instructor in instructors:
            if instructor.username == username:
                print("Username already exists!!")
                return
        password = getpass.getpass("Enter Password: ")
        con_password = getpass.getpass("Confirm Password: ")
        if password != con_password:
            print("Passwords don't match")
            return
        last_name = input("Enter Last Name: ")
        first_name = input("Enter First Name: ")
        middle_name = input("Enter Middle Name: ")
        age = int(input("Enter Age: "))  # Age should be an integer
        contact_number = input("Enter Contact Number: ")
        gender = input("Enter Gender (Male/Female/Other): ")
        email = input("Enter Email: ")
        address = input("Enter Address: ")
        bio = input("Enter Bio: ")
        teaching_experience = int(input("Enter Years of Teaching Experience: "))  # Years of experience should be an integer
        specialization = input("Enter Specialization: ")
        contract_status = input("Enter Contract Status (Full-time/Part-time/Contract): ")
        office_hours = input("Enter Office Hours: ")
        response_time = input("Enter Response Time: ")
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Instructors(instructor_id, username, password, last_name, first_name, middle_name, age, contact_number, gender, email, address, bio, teaching_experience, specialization, contract_status, office_hours, response_time)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (instructor_id, username, password, last_name, first_name, middle_name, age, contact_number, gender, email, address, bio, teaching_experience, specialization, contract_status, office_hours, response_time))
        conn.commit()
        cursor.close()
        conn.close()
        Course.create_course(instructor_id)
        print(f"Here's your instructor ID, please keep this confidential {instructor_id}, registred successfully!")