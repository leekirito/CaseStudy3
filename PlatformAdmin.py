import pyodbc

def connect_to_database():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER= LIECODEX\\SQLEXPRESS;"
        "DATABASE=E_Learning_Platform;"
        "Trusted_Connection=yes;"
    )

class PlatformAdmin():
    username  = "admin"
    password = "admin"


    @classmethod
    def remove_student(cls, student_id):
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("""
        DELETE FROM Students WHERE student_id = ? 
        """, (student_id))
        conn.commit()
        cursor.close()
        conn.close()

    @classmethod
    def remove_instructor(cls, intructor_id):
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("""
        DELETE FROM Instructors WHERE instructor_id = ? 
        """, (intructor_id))
        conn.commit()
        cursor.close()
        conn.close()

    @classmethod
    def remove_course(cls, course_id):
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("""
        DELETE FROM Courses WHERE course_id = ? 
        """, (course_id))
        conn.commit()
        cursor.close()
        conn.close()