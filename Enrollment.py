import pyodbc
from datetime import datetime 
import os 
from tabulate import tabulate
from Student import Student  # Importing the Student class to access student-related operations
from Payment import Payment  # Importing Payment class for payment handling

# Helper function to establish a connection to the database
def connect_to_database():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"  # Driver for SQL Server
        "SERVER=LIECODEX\\SQLEXPRESS;"  # Server name
        "DATABASE=E_Learning_Platform;"  # Target database
        "Trusted_Connection=yes;"  # Use Windows authentication
    )

class Enrollment:
    # Constructor to initialize an Enrollment object
    def __init__(self, enrollment_id, student_id, course_id, enrollment_date, status, progress):
        self.enrollment_id = enrollment_id  # Unique ID for the enrollment
        self.student_id = student_id  # ID of the student enrolled in the course
        self.course_id = course_id  # ID of the course the student is enrolled in
        self.enrollment_date = enrollment_date  # Date of enrollment
        self.status = status  # Status of enrollment (e.g., "active")
        self.progress = progress  # Progress in the course (e.g., "0%")

    @classmethod
    def get_data(cls):
        # Fetch all enrollment records from the database
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Enrollments")  # Query to fetch all records
        rows = cursor.fetchall()
        
        # Create a list of Enrollment objects from the fetched data
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
        
        # Close the database connection
        cursor.close()
        conn.close()
        return enrollments

    @classmethod
    def show__all_enrolled_course(cls):
        # Display all enrollments in a tabular format
        enrolls = cls.get_data()
        content = [
            [enroll.enrollment_id, enroll.student_id, enroll.course_id, enroll.enrollment_date, enroll.status, enroll.progress]
            for enroll in enrolls
        ]
        header = ["Enrollment ID", "Student ID", "Course ID", "Enrolled Date", "Status", "Progress"]
        print(tabulate(content, header, tablefmt="pretty"))

    @classmethod
    def show_my_enrolled_course(cls, student_id):
        # Display enrollments specific to a particular student
        enrolls = cls.get_data()
        content = [
            [enroll.enrollment_id, enroll.student_id, enroll.course_id, enroll.enrollment_date, enroll.status, enroll.progress]
            for enroll in enrolls if student_id == enroll.student_id
        ]
        header = ["Enrollment ID", "Student ID", "Course ID", "Enrolled Date", "Status", "Progress"]
        print(tabulate(content, header, tablefmt="pretty"))

    @classmethod
    def take_course(cls, student_id):
        # Allow a student to enroll in a course
        from Course import Course  # Import Course class to access course-related functionality

        Course.show_all_courses()  # Show all available courses
        course_id = input("Course ID: ")  # Prompt the student to select a course
        course_price = None  # Initialize course price

        # Retrieve course data and check if the selected course exists
        courses = Course.get_data()
        for course in courses:
            if str(course.course_id) == str(course_id):  # Match course_id as strings for flexibility
                course_price = course.price
                break
        else:  # If no course matches, show an error
            print("Course ID does not exist!")
            return None 

        # Enrollment details
        enrollment_date = datetime.now().date()  # Current date as the enrollment date
        status = "active"  # Default status
        progress = "0%"  # Default progress

        # Process payment for the course
        if not Payment.pay(course_price):  # If payment fails, exit
            return None

        # Insert the enrollment record into the database
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Enrollments(student_id, course_id, enrollment_date, status, progress)
            VALUES(?, ?, ?, ?, ?)
        """, (student_id, course_id, enrollment_date, status, progress))
        conn.commit()  # Commit the changes to the database
        cursor.close()
        conn.close()

        # Update the number of students in the course
        Course.add_student(course_id)
        print("Successfully enrolled in the course!")

    @classmethod
    def show_all_student_in_course(cls, course_id):
        # Display all students enrolled in a specific course
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT Students.username, Students.last_name, Courses.course_name, Enrollments.status, Enrollments.progress
            FROM Enrollments
            JOIN Students ON Enrollments.student_id = Students.student_id
            JOIN Courses ON Enrollments.course_id = Courses.course_id
            WHERE Enrollments.course_id = ?
        """, (course_id,))
        rows = cursor.fetchall()

        # Prepare content for tabular display
        content = [
            [row.username, row.last_name, row.course_name, row.status, row.progress]
            for row in rows
        ]
        header = ["Username", "Last Name", "Course Name", "Status", "Progress"]
        print(tabulate(content, header, tablefmt="pretty"))
