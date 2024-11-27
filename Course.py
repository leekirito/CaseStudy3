import pyodbc
from datetime import datetime 
import os 
from tabulate import tabulate
from Schedule import Schedule


def connect_to_database():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=LIECODEX\\SQLEXPRESS;"
        "DATABASE=E_Learning_Platform;"
        "Trusted_Connection=yes;"
    )

class Course():

    def __init__(self, course_id, course_name, intructor_id, price, average_duration, description, rating, last_updated, number_of_students):
        self.course_id = course_id
        self.course_name = course_name
        self.intructor_id= intructor_id
        self.price = price
        self.average_duration =average_duration
        self.description = description
        self.rating = rating
        self.last_updated = last_updated
        self.number_of_students = number_of_students

    @classmethod
    def get_data(cls):
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Courses")
        rows = cursor.fetchall()
        
        # Create Course objects for each row in the database
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
        
        cursor.close()
        conn.close()
        return courses
    @classmethod
    def show_all_courses(cls):
        courses = cls.get_data()
        content = []
        for course in courses:
            content.append([course.course_id, course.course_name,course.description, course.intructor_id, course.rating, course.number_of_students, course.price])
        header = ["Course ID","Course Name","Description","Intructor ID","Rating","Number of students","Price"]
        print(tabulate(content, header, tablefmt="pretty"))

    
    def get_details(self):
        print(f"{'Course ID:':<20} {self.course_id}")
        print(f"{'Course Name:':<20} {self.course_name}")
        print(f"{'Intructor ID:':<20} {self.intructor_id}")
        print(f"{'Rating:':<20} {self.rating}")
        print(f"{'Number Of Students:':<20} {self.number_of_students}")
        print(f"{'Price:':<20} {self.price}")
        print(f"{'Average Duration:':<20} {self.average_duration}")
        print(f"{'Description:':<20} {self.description}")
        print(f"{'Last Updated:':<20} {self.last_updated}")
        print("-" * 40)
    
    
    def update_course(self):
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("UPDATE Courses SET last_updated = ? WHERE course_id = ?", (datetime.now().date(), self.course_id))
        conn.commit()
        cursor.close()
        conn.close()

    @classmethod
    def create_course(cls, intructor_id):
        course_name = input("Course Name: ")
        course_description = input("Course Description: ")
        average_duration = input("Average duration: ")
        last_updated = datetime.now().date()
        rating = "2.0"
        number_of_students = 0
        price = int(input("Course Price: "))
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO Courses(course_name, intructor_id, price, average_duration, description, rating, last_updated, number_of_students)
                       OUTPUT INSERTED.course_id
                       VALUES(?,?,?,?,?,?,?,?,)
                       """, (course_name, intructor_id, price, average_duration, course_description, rating, last_updated, number_of_students))
        
        course_id = cursor.fetchone()[0]
        Schedule.create_schedule(course_id)
        conn.commit()
        cursor.close()
        conn.close()
    
    @staticmethod
    def add_student(course_id):
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("UPDATE Courses SET number_of_students = number_of_students + 1 WHERE course_id = ?", (course_id))
        conn.commit()
        cursor.close()
        conn.close()

    

