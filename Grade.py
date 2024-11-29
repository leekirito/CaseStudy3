import pyodbc
from Assignment import Assignment  # Import Assignment class to interact with assignments

def connect_to_database():
    """
    Establish a connection to the E_Learning_Platform database.
    
    Returns:
        pyodbc.Connection: A connection object for the database.
    """
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=LIECODEX\\SQLEXPRESS;"
        "DATABASE=E_Learning_Platform;"
        "Trusted_Connection=yes;"
    )


class Grade:
    """
    A class that provides functionality to grade assignments.
    """
    def __init__(self):
        """
        Constructor for Grade class.
        Currently, no instance attributes are required.
        """
        pass

    @classmethod
    def grade_assignment(cls, instructor_id):
        """
        Grade an assignment assigned by a specific instructor.
        
        Args:
            instructor_id (int): The ID of the instructor grading the assignment.
        
        Functionality:
        - Displays all assignments assigned by the instructor.
        - Allows the instructor to select an assignment by its ID.
        - Prompts the instructor to input a grade (0-100) for the assignment.
        - Updates the grade in the database.
        
        Returns:
            None
        """
        # Display all assignments assigned by this instructor
        Assignment.show_all_assigned_work(instructor_id)
        
        # Prompt the instructor to select an assignment to grade
        assignment_id = input("Which Assignment to grade (ID): ")
        assignments = Assignment.get_data()  # Retrieve all assignments
        
        # Validate the selected assignment ID
        for assignment in assignments:
            if str(assignment.assignment_id) == str(assignment_id):
                # Ensure the grade is within the valid range (0-100)
                while True:
                    try:
                        grade = int(input("Grade (0-100): "))
                        if grade < 0 or grade > 100:
                            print("Grade too high or low! Please enter a value between 0 and 100.")
                        else:
                            break
                    except ValueError:
                        print("Invalid input! Please enter a numeric grade.")
                break
        else:
            # If no matching assignment is found, notify the user
            print("Assignment does not exist!")
            return None
        
        # Update the grade in the database
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Assignments SET grade = ? WHERE assignment_id = ?",
            (grade, assignment_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Successfully graded Assignment ID {assignment_id} with a grade of {grade}.")
