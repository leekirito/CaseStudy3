import pyodbc
from datetime import datetime 
import os 
from tabulate import tabulate
from Student import Student
from Enrollment import Enrollment
from Course import Course

# Helper function to establish a connection to the database
def connect_to_database():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=LIECODEX\\SQLEXPRESS;"  # Specify the server name
        "DATABASE=E_Learning_Platform;"  # Specify the database name
        "Trusted_Connection=yes;"  # Use Windows authentication
    )

class Assignment():
    # Constructor to initialize an Assignment object with necessary attributes
    def __init__(self, assignment_id, instructor_id, student_id, course_id, assignment_name, assigned_date, due_date, details, grade, response):
        self.assignment_id  = assignment_id
        self.instructor_id = instructor_id  # ID of the instructor who created the assignment
        self.student_id = student_id  # ID of the student for whom the assignment is assigned
        self.course_id = course_id  # ID of the course to which the assignment belongs
        self.assignment_name = assignment_name  # Name of the assignment
        self.assigned_date = assigned_date  # Date the assignment was assigned
        self.due_date = due_date  # Date the assignment is due
        self.details = details  # Instructions/details about the assignment
        self.grade = grade  # Grade given for the assignment (initially 0)
        self.response = response  # Student's response to the assignment

    @classmethod
    def get_data(cls):
        # Fetch all assignments from the database
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Assignments")
        rows = cursor.fetchall()
        
        # Create a list of Assignment objects from the fetched rows
        assignments = [
            cls(
                assignment_id=row.assignment_id,
                instructor_id=row.instructor_id,
                student_id=row.student_id,
                course_id=row.course_id,
                assignment_name=row.assignment_name,
                assigned_date=row.assigned_date,
                due_date=row.due_date,
                details=row.details,
                grade=row.grade,
                response=row.response
            )
            for row in rows
        ]

        # Close database connection
        cursor.close()
        conn.close()
        return assignments

    @classmethod
    def assign_work(cls, instructor_id):
        # Assign a new assignment to a student
        
        # Prompt for the student's username and find their ID
        username = input("Student Username: ")
        students = Student.get_data()
        student_id = None
        for student in students:
            if student.username == username:
                student_id = student.student_id
                break
        else:
            print("Student does not exist")
            return None

        # Find the course ID associated with the instructor
        course_id = None
        courses = Course.get_data()
        for course in courses:
            if instructor_id == course.instructor_id:
                course_id = course.course_id

        # Verify if the student is enrolled in the instructor's course
        enrollments = Enrollment.get_data()
        for enroll in enrollments:
            if student_id == enroll.student_id and course_id == enroll.course_id:
                break
        else:
            print("This student is not enrolled in your course!")
            return None

        # Gather assignment details
        assignment_name = input("Assignment Name: ")
        assigned_date = datetime.now().date()
        due_date = input("Due Date (YYYY-MM-DD): ")
        details = input("Instructions: ")
        grade = 0  # Default grade
        
        # Save the assignment to the database
        conn = connect_to_database()  
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Assignments(instructor_id, student_id, course_id, assignment_name, assigned_date, due_date, details, grade)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?)
        """, (instructor_id, student_id, course_id, assignment_name, assigned_date, due_date, details, grade))
        conn.commit()
        
        # Close the connection
        cursor.close()
        conn.close()
        os.system("cls")  # Clear the console for a cleaner output
        print("Assigned successfully")
    
    @classmethod
    def show_all_assigned_work(cls, instructor_id):
        # Display all assignments created by a specific instructor
        works = cls.get_data()  # Retrieve all assignments
        content = []
        for work in works:
            if instructor_id == work.instructor_id:
                # Collect assignment details in a list
                content.append([work.assignment_id, work.student_id, work.course_id, work.assignment_name, work.details, work.assigned_date, work.due_date, work.grade, work.response])
        # Print assignments in a tabular format
        header = ["Assignment ID", "Student ID", "Course ID", "Title", "Details", "Assigned Date", "Due Date", "Grade", "Response"]
        print(tabulate(content, header, tablefmt="pretty"))

    @classmethod
    def show_assigned_work(cls, student_id):
        # Display all assignments assigned to a specific student
        works = Assignment.get_data()  # Retrieve all assignments
        content = []
        for work in works:
            if student_id == work.student_id:
                # Collect assignment details in a list
                content.append([work.assignment_id, work.instructor_id, work.course_id, work.assignment_name, work.details, work.assigned_date, work.due_date, work.grade, work.response])
        # Print assignments in a tabular format
        header = ["Assignment ID", "Instructor ID", "Course ID", "Title", "Details", "Assigned Date", "Due Date", "Grade", "Response"]
        print(tabulate(content, header, tablefmt="pretty"))

    @classmethod
    def answer_assignment(cls, student_id):
        # Allow a student to respond to an assignment
        cls.show_assigned_work(student_id)  # Display all assignments for the student
        assignment_id = int(input("Assignment ID: "))  # Prompt for assignment ID
        assignments = cls.get_data()  # Retrieve all assignments
        response = None
        
        # Check if the assignment exists and belongs to the student
        for assignment in assignments:
            if assignment_id == assignment.assignment_id and student_id == assignment.student_id:
                response = input("Your answer: ")  # Prompt for student's answer
                break
        else:
            print("Assignment does not exist")
            return None

        # Save the response to the database
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("UPDATE Assignments SET response = ? WHERE assignment_id = ?", (response, assignment_id))
        conn.commit()
        
        # Close the connection
        cursor.close()
        conn.close()
