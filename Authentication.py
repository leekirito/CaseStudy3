from Instructor import Instructor  # Import Instructor class to access instructor-related data
from Student import Student  # Import Student class to access student-related data
from PlatformAdmin import PlatformAdmin  # Import PlatformAdmin for admin authentication

class Authentication:
    """
    This class provides methods to authenticate users based on their roles:
    - Instructor
    - Student
    - Platform Administrator
    """

    @staticmethod
    def authenticate_instructor(username, password):
        """
        Authenticate an instructor using their username and password.
        
        Args:
            username (str): The username provided by the instructor.
            password (str): The password provided by the instructor.
        
        Returns:
            Instructor object if authentication is successful.
            False if the credentials do not match.
        """
        instructors = Instructor.get_data()  # Retrieve all instructors' data
        for instructor in instructors:
            if username == instructor.username and password == instructor.password:
                return instructor  # Return the matched instructor object
        print("User does not exist")  # Inform user if no match is found
        return False  # Return False if authentication fails

    @staticmethod
    def authenticate_student(username, password):
        """
        Authenticate a student using their username and password.
        
        Args:
            username (str): The username provided by the student.
            password (str): The password provided by the student.
        
        Returns:
            Student object if authentication is successful.
            False if the credentials do not match.
        """
        students = Student.get_data()  # Retrieve all students' data
        for student in students:
            if username == student.username and password == student.password:
                return student  # Return the matched student object
        print("User does not exist")  # Inform user if no match is found
        return False  # Return False if authentication fails

    @staticmethod
    def authenticate_admin(username, password):
        """
        Authenticate a platform administrator using a static username and password.
        
        Args:
            username (str): The username provided by the admin.
            password (str): The password provided by the admin.
        
        Returns:
            True if authentication is successful.
            False otherwise.
        """
        if username == PlatformAdmin.username and password == PlatformAdmin.password:
            return True  # Return True if credentials match
        else:
            return False  # Return False if authentication fails
