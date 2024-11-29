import pyodbc
import uuid
import getpass  # For secure password input
from Instructor import Instructor
from Student import Student
from Course import Course  # To allow instructors to create courses during registration

# Function to establish a connection with the database
def connect_to_database():
    """
    Connects to the E_Learning_Platform database using pyodbc.

    Returns:
        pyodbc.Connection: A connection object for the database.
    """
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER= LIECODEX\\SQLEXPRESS;"
        "DATABASE=E_Learning_Platform;"
        "Trusted_Connection=yes;"
    )

class Register:
    """
    Handles the registration process for students and instructors.
    """

    @classmethod
    def register_student(cls):
        """
        Registers a new student by collecting their details and saving them in the database.
        """
        students = Student.get_data()  # Fetch existing student data to validate username uniqueness
        student_id = str(uuid.uuid4())  # Generate a unique identifier for the student
        username = input("Enter username: ")
        for student in students:
            if student.username == username:
                print("Username already exists!!")
                return
        
        # Secure password input and confirmation
        password = getpass.getpass("Enter Password: ")
        con_password = getpass.getpass("Confirm Password: ")
        if password != con_password:
            print("Passwords don't match!")
            return

        # Collect additional student details
        last_name = input("Enter Last Name: ")
        first_name = input("Enter First Name: ")
        middle_name = input("Enter Middle Name: ")
        age = int(input("Enter Age: "))
        contact_number = input("Enter Contact Number: ")
        gender = input("Enter Gender (Male/Female/Other): ")
        email = input("Enter Email: ")
        address = input("Enter Address: ")
        total_courses = 0
        date_of_birth = input("Enter Date of Birth (YYYY-MM-DD): ")
        access_level = input("Enter Access Level (e.g., free, premium): ")
        account_status = "Active"
        average_study_time = input("Enter Average Study Time (hours per week): ")

        # Insert student data into the database
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Students(
                student_id, username, password, last_name, first_name, middle_name, age, 
                contact_number, gender, email, address, total_courses, date_of_birth, 
                access_level, account_status, average_study_time
            )
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            student_id, username, password, last_name, first_name, middle_name, age, 
            contact_number, gender, email, address, total_courses, date_of_birth, 
            access_level, account_status, average_study_time
        ))
        conn.commit()
        cursor.close()
        conn.close()

        # Confirmation message
        print(f"Here's your student ID, please keep this confidential: {student_id}. Registered successfully!")

    @classmethod
    def register_instructor(cls):
        """
        Registers a new instructor by collecting their details and saving them in the database.
        """
        instructors = Instructor.get_data()  # Fetch existing instructor data to validate username uniqueness
        instructor_id = str(uuid.uuid4())  # Generate a unique identifier for the instructor
        username = input("Enter username: ")
        for instructor in instructors:
            if instructor.username == username:
                print("Username already exists!!")
                return

        # Secure password input and confirmation
        password = getpass.getpass("Enter Password: ")
        con_password = getpass.getpass("Confirm Password: ")
        if password != con_password:
            print("Passwords don't match!")
            return

        # Collect additional instructor details
        last_name = input("Enter Last Name: ")
        first_name = input("Enter First Name: ")
        middle_name = input("Enter Middle Name: ")
        age = int(input("Enter Age: "))
        contact_number = input("Enter Contact Number: ")
        gender = input("Enter Gender (Male/Female/Other): ")
        email = input("Enter Email: ")
        address = input("Enter Address: ")
        bio = input("Enter Bio: ")
        teaching_experience = int(input("Enter Years of Teaching Experience: "))
        specialization = input("Enter Specialization: ")
        contract_status = input("Enter Contract Status (Full-time/Part-time/Contract): ")
        office_hours = input("Enter Office Hours: ")
        response_time = input("Enter Response Time: ")

        # Insert instructor data into the database
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Instructors(
                instructor_id, username, password, last_name, first_name, middle_name, age, 
                contact_number, gender, email, address, bio, teaching_experience, specialization, 
                contract_status, office_hours, response_time
            )
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            instructor_id, username, password, last_name, first_name, middle_name, age, 
            contact_number, gender, email, address, bio, teaching_experience, specialization, 
            contract_status, office_hours, response_time
        ))
        conn.commit()
        cursor.close()
        conn.close()

        # Prompt instructor to create a course after registration
        Course.create_course(instructor_id)

        # Confirmation message
        print(f"Here's your instructor ID, please keep this confidential: {instructor_id}. Registered successfully!")
