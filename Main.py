from Assignment import Assignment
from Authentication import Authentication
from Course import Course
from Enrollment import Enrollment
from Grade import Grade
from Instructor import Instructor
from PlatformAdmin import PlatformAdmin
from Register import Register
from Schedule import Schedule
from Student import Student
from getpass import getpass

class main():
    def __init__(self):
        self.current_student = None
        self.current_instructor = None
        self.students = Student.get_data()
        self.instructors = Instructor.get_data()
        self.courses = Course.get_data()

    def Start_menu(self):

        start_options = {
            "1": self.log_in_instructor_menu(),
            "2": self.log_in_student_menu(),
            "3": self.log_in_admin_menu(),
            "4": self.register_as_instructor_menu(),
            "5": self.register_as_student_menu()
        }
        while True:
            self.students = Student.get_data()
            self.instructors = Instructor.get_data()
            self.courses = Course.get_data()
            print("1. Log In As Instructor")
            print("2. Log In As Student")
            print("3. Log In As Admin")
            print("4. Register As a Instructor")
            print("5. Register as a Student")

            choice = input("Please enter your choice: ")
            action = start_options.get(choice)
            if action:
                action()
            else:
                print("Invalid choice, please try again.")

    def log_in_instructor_menu(self):
        while True:
            username = input("Username: ")
            password = getpass("Password: ")
            if not Authentication.authenticate_instructor(username, password):
                print("Username or Password is wrong")
            else:
                self.current_instructor = Authentication.authenticate_instructor(username, password)
                self.instructor_menu()
    def log_in_student_menu(self):
        while True:
            username = input("Username: ")
            password = getpass("Password: ")
            if not Authentication.authenticate_student(username, password):
                print("Username or Password is wrong")
            else:
                self.current_student = Authentication.authenticate_student(username, password)
                self.student_menu()

    def log_in_admin_menu(self):
        while True:
            username = input("Username: ")
            password = getpass("Password: ")
            if not Authentication.authenticate_admin(username, password):
                print("Username or Password is wrong")
            else:
                self.admin_menu()

    def register_as_instructor_menu(self):
        Register.register_instructor()

    def register_as_student_menu(self):
        Register.register_student()

    def instructor_menu(self):
        intructor_options = {
            "1": self.assign_work(),
            "2": self.show_all_assigned_work(),
            "3": self.grade_work(),
            "4": self.create_schedule(),
            "5": self.update_session_days(),
            "6": self.update_start_time(),
            "7": self.update_end_time(),
            "8": self.update_location(),
            "9": self.update_time_zone(),
            "10": self.get_schedule(),
            "11": self.instructor_personal_info()

        }
        while True:
            print("1. Assign Work")
            print("2. Show all assigned Work")
            print("3. Grade Work")
            print("4. Create Schedule")
            print("5. Update Session Days")
            print("6. Update Start Time")
            print("7. Update End Time")
            print("8. Update Location")
            print("9. Update Time Zone")
            print("10. Get Schedule")
            print("11. Personal Info")
            print("12. Return")

            choice = input("Please enter your choice: ")
            action = intructor_options.get(choice)
            if choice == "12":
                return
            elif action:
                action()
            else:
                print("Invalid choice, please try again.")


    def assign_work(self):
        course_id = int(input("Course ID: "))
        Enrollment.show_all_student_in_course(course_id)
        Assignment.assign_work(self.current_instructor.instructor_id)
    def show_all_assigned_work(self):
        Assignment.show_all_assigned_work(self.current_instructor.instructor_id)
    def grade_work(self):
        Grade.grade_assignment(self.current_instructor.instructor_id)
    def create_schedule(self):
        Schedule.create_schedule(self.current_instructor.instructor_id)
    def update_session_days(self):
        Schedule.update_session_days(self.current_instructor.instructor_id)
    def update_start_time(self):
        Schedule.update_start_time(self.current_instructor.instructor_id)
    def update_end_time(self):
        Schedule.update_end_time(self.current_instructor.instructor_id)
    def update_location(self):
        Schedule.update_location(self.current_instructor.instructor_id)
    def update_time_zone(self):
        Schedule.update_time_zone(self.current_instructor.instructor_id)
    def get_schedule(self):
        Schedule.get_schedule()
    def instructor_personal_info(self):
        self.current_instructor.display_info()






    def student_menu(self):
        intructor_options = {
            "1": self.take_course(),
            "2": self.show_assigned_work(),
            "3": self.show_my_enrolled_course(),
            "4": self.answer_assignment(),
            "5": self.get_schedule(),
            "6": self.student_personal_info()

        }
        while True:
            print("1. Take Course")
            print("2. Show All assignments")
            print("3. Show enrolled course")
            print("4. Answer Assignment")
            print("5. Get Schedule")
            print("6. Personal Info")
            print("7. Return")

            choice = input("Please enter your choice: ")
            action = intructor_options.get(choice)
            if choice == "7":
                return
            elif action:
                action()
            else:
                print("Invalid choice, please try again.")
    
    def take_course(self):
        Enrollment.take_course(self.current_student.username)
    def show_assigned_work(self):
        Assignment.show_assigned_work(self.current_student.student_id)
    def show_my_enrolled_course(self):
        Enrollment.show_my_enrolled_course(self.current_student.student_id)
    def answer_assignment(self):
        Assignment.answer_assignment(self.current_student.student_id)
    def student_personal_info(self):
        self.current_student.display_info()

    



    def admin_menu(self):
        intructor_options = {
            "1": self.remove_student(),
            "2": self.remove_intructor(),
            "3": self.remove_course(),

        }
        while True:
            print("1. Remove Student")
            print("2. Remove Instructor")
            print("3. Remove Course")
            print("4. Return")


            choice = input("Please enter your choice: ")
            action = intructor_options.get(choice)
            if choice == "4":
                return
            elif action:
                action()
            else:
                print("Invalid choice, please try again.")


    def remove_student(self):
        username = input("Student Username: ")
        student_id = None
        for student in self.students:
            if username == student.username:
                student_id = student.student_id
                break
        else:
            print("Student Does not exist")
            return
        confirm = input("Are you sure you want to delete this student Y/N? ")
        if confirm.lower == "y":
            PlatformAdmin.remove_student(student_id)
        else:
            print("Cancelled operation")
            return
        
    def remove_intructor(self):
        username = input("Instructor Username: ")
        instructor_id = None
        for instructor in self.instructors:
            if username == instructor.username:
                instructor_id = instructor.instructor_id
                break
        else:
            print("Instructor Does not exist")
            return
        confirm = input("Are you sure you want to delete this instructor Y/N? ")
        if confirm.lower == "y":
            PlatformAdmin.remove_instructor(instructor_id)
        else:
            print("Cancelled operation")
            return
    def remove_course(self):
        course_id = input("Course ID: ")
        for course in self.courses:
            if course_id == course.course_id:
                break
        else:
            print("Course Does not exist")
            return
        confirm = input("Are you sure you want to delete this course Y/N? ")
        if confirm.lower == "y":
            PlatformAdmin.remove_course(course_id)
        else:
            print("Cancelled operation")
            return
        
# Initialize the online shop
if __name__ == "__main__":
    Main = main()
    Main.Start_menu()



