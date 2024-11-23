from Person import Person
import pyodbc
import uuid
import getpass



def connect_to_database():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER= LIECODEX\\SQLEXPRESS;"
        "DATABASE=E_Learning_Platform;"
        "Trusted_Connection=yes;"
    )

class Student(Person):

    def __init__(self, student_id, username, password, last_name, first_name, middle_name, age, contact_number, gender, email, address, total_courses, date_of_birth, access_level, account_status, average_study_time):
        super().__init__(id, username, password, last_name, first_name, middle_name, age, contact_number, gender, email, address)
        self.student_id = student_id
        self.total_courses = total_courses
        self.date_of_birth = date_of_birth
        self.access_level = access_level
        self.account_status = account_status
        self.average_study_time = average_study_time

    @classmethod
    def get_data(cls):
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Students")
        rows = cursor.fetchall()
        studends = [cls(student_id = row.student_id, username = row.username, password = row.password, last_name = row.last_name, first_name = row.first_name, middle_name = row.middle_name, age = row.age, contact_number = row.contact_number, gender = row.gender, email = row.email, address = row.address, total_courses = row.total_courses, date_of_birth = row.date_of_birth, access_level = row.access_level, account_status = row.account_status, average_study_time = row.average_study_time)for row in rows]
        cursor.close()
        conn.close()
        return studends

    def display_info(self):
        print(f"{'Username:':<20} {self.username}")
        print(f"{'Password:':<20} {self.password}")
        print(f"{'Last Name:':<20} {self.last_name}")
        print(f"{'First Name:':<20} {self.first_name}")
        print(f"{'Middle Name:':<20} {self.middle_name}")
        print(f"{'Age:':<20} {self.age}")
        print(f"{'Contact Number:':<20} {self.contact_number}")
        print(f"{'Gender:':<20} {self.gender}")
        print(f"{'Email:':<20} {self.email}")
        print(f"{'Address:':<20} {self.address}")
        print(f"{'Total Courses:':<20} {self.total_courses}")
        print(f"{'Date of Birth:':<20} {self.date_of_birth}")
        print(f"{'Access Level:':<20} {self.access_level}")
        print(f"{'Account Status:':<20} {self.account_status}")
        print(f"{'Average Study Time:':<20} {self.average_study_time}")
        print("-" * 40)

    
