import pyodbc
from Assignment import Assignment


def connect_to_database():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=LIECODEX\\SQLEXPRESS;"
        "DATABASE=E_Learning_Platform;"
        "Trusted_Connection=yes;"
    )


class Grade():
    def __init__(self):
        pass
    
    @classmethod
    def grade_assignment(cls, intructor_id):
        Assignment.show_all_assigned_work(intructor_id)
        assignment_id = input("Which Assignment to grade(ID): ")
        assignments = Assignment.get_data()
        for assignment in assignments:
            if str(assignment.assignment_id) == (assignment_id):
                while True:
                    grade = int(input("Grade(0/100): "))
                    if grade < 0 or grade > 100:
                        print("Grade too high or low!")
                    else:
                        break
                break
        else:
            print("Assignment does not exist!")
            return None
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("UPDATE Assignments SET grade = ? WHERE assignment_id = ?", (grade, assignment_id))
        conn.commit()
        cursor.close()
        conn.close()