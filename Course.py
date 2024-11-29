import pyodbc
from datetime import datetime 
import os 
from tabulate import tabulate

# Helper function to establish a connection to the database
def connect_to_database():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"  # ODBC driver for SQL Server
        "SERVER=LIECODEX\\SQLEXPRESS;"  # SQL Server instance
        "DATABASE=E_Learning_Platform;"  # Target database
        "Trusted_Connection=yes;"  # Windows authentication
    )

class Course():
    # Constructor to initialize Course object attributes
    def __init__(self, course_id, course_name, instructor_id, price, average_duration, description, rating, last_updated, number_of_students):
        self.course_id = course_id
        self.course_name = course_name
        self.intructor_id = instructor_id  # Instructor responsible for the course
        self.price = price  # Cost of the course
        self.average_duration = average_duration  # Average duration to complete the course
        self.description = description  # Brief description of the course content
        self.rating = rating  # Course rating (default 2.0)
        self.last_updated = last_updated  # Date when the course was last updated
        self.number_of_students = number_of_students  # Number of enrolled students

    @classmethod
    def get_data(cls):
        # Fetch all courses from the database
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Courses")  # Fetch all rows from the Courses table
        rows = cursor.fetchall()

        # Create a list of Course objects from the fetched data
        courses = [
            cls(
                course_id=row.course_id,
                course_name=row.course_name,
                instructor_id=row.instructor_id,
                price=row.price,
                average_duration=row.average_duration,
                description=row.description,
                rating=row.rating,
                last_updated=row.last_updated,
                number_of_students=row.number_of_students
            )
            for row in rows
        ]
        
        # Close the database connection
        cursor.close()
        conn.close()
        return courses

    @classmethod
    def show_all_courses(cls):
        # Display all courses in a tabular format
        courses = cls.get_data()  # Retrieve all courses
        content = [
            [course.course_id, course.course_name, course.description, course.intructor_id, course.rating, course.number_of_students, course.price]
            for course in courses
        ]
        # Define headers and display the data using the tabulate library
        header = ["Course ID", "Course Name", "Description", "Instructor ID", "Rating", "Number of Students", "Price"]
        print(tabulate(content, header, tablefmt="pretty"))

    def get_details(self):
        # Print detailed information about the course
        print(f"{'Course ID:':<20} {self.course_id}")
        print(f"{'Course Name:':<20} {self.course_name}")
        print(f"{'Instructor ID:':<20} {self.intructor_id}")
        print(f"{'Rating:':<20} {self.rating}")
        print(f"{'Number Of Students:':<20} {self.number_of_students}")
        print(f"{'Price:':<20} {self.price}")
        print(f"{'Average Duration:':<20} {self.average_duration}")
        print(f"{'Description:':<20} {self.description}")
        print(f"{'Last Updated:':<20} {self.last_updated}")
        print("-" * 40)

    def update_course(self):
        # Update the course's last updated date in the database
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Courses SET last_updated = ? WHERE course_id = ?", 
            (datetime.now().date(), self.course_id)
        )
        conn.commit()  # Commit changes to the database
        cursor.close()
        conn.close()

    @classmethod
    def create_course(cls, instructor_id):
        # Allow an instructor to create a new course
        from Schedule import Schedule  # Import Schedule module to handle scheduling

        # Gather course details from the instructor
        course_name = input("Course Name: ")
        course_description = input("Course Description: ")
        average_duration = input("Average Duration: ")
        last_updated = datetime.now().date()  # Automatically set to the current date
        rating = "2.0"  # Default rating for a new course
        number_of_students = 0  # Initially, no students enrolled
        price = float(input("Course Price: "))

        # Insert the new course into the database and retrieve the generated course ID
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Courses(course_name, instructor_id, price, average_duration, description, rating, last_updated, number_of_students)
            OUTPUT INSERTED.course_id
            VALUES(?, ?, ?, ?, ?, ?, ?, ?)
        """, (course_name, instructor_id, price, average_duration, course_description, rating, last_updated, number_of_students))
        course_id = cursor.fetchone()[0]  # Retrieve the generated course ID
        conn.commit()
        cursor.close()
        conn.close()

        # Notify the user and create a schedule for the course
        print(f"Created course! Here's the course ID: {course_id}. Creating Schedule...")
        Schedule.create_schedule(instructor_id)

    @staticmethod
    def add_student(course_id):
        # Increment the number of students enrolled in a course
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Courses SET number_of_students = number_of_students + 1 WHERE course_id = ?", 
            (course_id,)
        )
        conn.commit()  # Commit the changes
        cursor.close()
        conn.close()
