import pyodbc

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

class PlatformAdmin:
    """
    Represents a platform administrator with predefined username and password.
    Provides methods to remove entities (students, instructors, courses) from the database.
    """

    # Static attributes for admin credentials
    username = "admin"
    password = "admin"

    @classmethod
    def remove_student(cls, student_id):
        """
        Removes a student record from the database based on the student_id.

        Args:
            student_id (int): The ID of the student to be removed.
        """
        conn = connect_to_database()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                DELETE FROM Students WHERE student_id = ?
            """, (student_id,))
            conn.commit()
            print(f"Student with ID {student_id} has been removed.")
        except Exception as e:
            print(f"Error removing student: {e}")
        finally:
            cursor.close()
            conn.close()

    @classmethod
    def remove_instructor(cls, instructor_id):
        """
        Removes an instructor record from the database based on the instructor_id.

        Args:
            instructor_id (int): The ID of the instructor to be removed.
        """
        conn = connect_to_database()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                DELETE FROM Instructors WHERE instructor_id = ?
            """, (instructor_id,))
            conn.commit()
            print(f"Instructor with ID {instructor_id} has been removed.")
        except Exception as e:
            print(f"Error removing instructor: {e}")
        finally:
            cursor.close()
            conn.close()

    @classmethod
    def remove_course(cls, course_id):
        """
        Removes a course record from the database based on the course_id.

        Args:
            course_id (int): The ID of the course to be removed.
        """
        conn = connect_to_database()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                DELETE FROM Courses WHERE course_id = ?
            """, (course_id,))
            conn.commit()
            print(f"Course with ID {course_id} has been removed.")
        except Exception as e:
            print(f"Error removing course: {e}")
        finally:
            cursor.close()
            conn.close()
