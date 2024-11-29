from Person import Person  # Inherits from the Person class
import pyodbc  # Library for database interaction

def connect_to_database():
    """
    Establishes a connection to the E_Learning_Platform database.
    Returns:
        pyodbc.Connection: A connection object for the database.
    """
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=LIECODEX\\SQLEXPRESS;"
        "DATABASE=E_Learning_Platform;"
        "Trusted_Connection=yes;"
    )


class Instructor(Person):
    """
    Represents an instructor in the e-learning platform, inheriting from the Person class.
    Adds specific attributes and methods relevant to instructors.
    """

    def __init__(self, instructor_id, username, password, last_name, first_name, middle_name, age, contact_number, gender, email, address, bio, teaching_experience, specialization, contract_status, office_hours, response_time):
        """
        Initializes an Instructor object with attributes inherited from Person,
        along with additional attributes specific to instructors.
        """
        # Call the parent class (Person) initializer
        super().__init__(username, password, last_name, first_name, middle_name, age, contact_number, gender, email, address)
        
        # Instructor-specific attributes
        self.instructor_id = instructor_id
        self.bio = bio
        self.teaching_experience = teaching_experience
        self.specialization = specialization
        self.contract_status = contract_status
        self.office_hours = office_hours
        self.response_time = response_time

    @classmethod
    def get_data(cls):
        """
        Fetches all instructor records from the database and creates Instructor objects.

        Returns:
            list: A list of Instructor objects representing each record in the database.
        """
        conn = connect_to_database()
        cursor = conn.cursor()

        # Execute SQL query to retrieve instructor data
        cursor.execute("SELECT * FROM Instructors")
        rows = cursor.fetchall()

        # Convert database rows into Instructor objects
        instructors = [
            cls(
                instructor_id=row.instructor_id,
                username=row.username,
                password=row.password,
                last_name=row.last_name,
                first_name=row.first_name,
                middle_name=row.middle_name,
                age=row.age,
                contact_number=row.contact_number,
                gender=row.gender,
                email=row.email,
                address=row.address,
                bio=row.bio,
                teaching_experience=row.teaching_experience,
                specialization=row.specialization,
                contract_status=row.contract_status,
                office_hours=row.office_hours,
                response_time=row.response_time
            )
            for row in rows
        ]

        # Close database connection
        cursor.close()
        conn.close()
        return instructors

    def display_info(self):
        """
        Displays all details of the instructor in a readable format.
        """
        # Print attributes with labels
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
        print(f"{'Bio:':<20} {self.bio}")
        print(f"{'Teaching Experience:':<20} {self.teaching_experience} years")
        print(f"{'Specialization:':<20} {self.specialization}")
        print(f"{'Contract Status:':<20} {self.contract_status}")
        print(f"{'Office Hours:':<20} {self.office_hours}")
        print(f"{'Response Time:':<20} {self.response_time}")
        print("-" * 40)
