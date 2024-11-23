import pyodbc
from datetime import datetime 
import os 
from tabulate import tabulate


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

    