import pyodbc
from Course import Course
from tabulate import tabulate

def connect_to_database():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER= LIECODEX\\SQLEXPRESS;"
        "DATABASE=E_Learning_Platform;"
        "Trusted_Connection=yes;"
    )

class Schedule():
    def __init__(self, schedule_id, course_id, instructor_id, session_days, start_time, end_time, location, time_zone):
        self.schedule_id = schedule_id
        self.course_id = course_id
        self.instructor_id = instructor_id
        self.session_days = session_days
        self.start_time = start_time
        self.end_time = end_time
        self.location = location
        self.time_zone = time_zone

    @classmethod
    def get_data(cls):
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Schedules")  
        rows = cursor.fetchall()
        
        schedules = [cls(
                schedule_id=row.schedule_id,
                course_id=row.course_id,
                instructor_id=row.instructor_id,
                session_days=row.session_days,
                start_time=row.start_time,
                end_time=row.end_time,
                location=row.location,
                time_zone=row.time_zone
            )for row in rows]
        
        cursor.close()
        conn.close()
        return schedules
    
    @classmethod
    def create_schedule(cls, intructor_id):
        course_id = int(input("Course ID: "))
        courses = Course.get_data()
        for course in courses:
            if course.intructor_id == intructor_id and course.course_id == course_id:
                break
        else:
            print("You don't own this course!")
            return None
        
        schedules = cls.get_data()
        for schedule in schedules:
            if schedule.instructor_id == intructor_id and course.course_id == course_id:
                print("You already have a schedule for this course, try changing the values instead")
                return None 
            
        session_days = input("Session Days(Monday, Tuesday etc..) : ")
        start_time = input("Start time: ")
        end_time = input("End Time: ")
        location = input("Location(ftf, google meet) :")
        time_zone = input("Time Zone(EST, MST): ")

        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO Schedules(course_id, instructor_id, session_days, start_time, end_time, location, time_zone)
                       VALUES(?,?,?,?,?,?,?)
                       """, (course_id, intructor_id, session_days, start_time, end_time, location, time_zone))
        conn.commit()
        cursor.close()
        conn.close()

    @classmethod
    def update_session_days(cls, intructor_id):
        course_id = int(input("Course ID: "))
        courses = Course.get_data()
        for course in courses:
            if course.intructor_id == intructor_id and course.course_id == course_id:
                break
        else:
            print("You don't own this course!")
            return None
        session_days = input("Session Days: ")
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("""UPDATE Schedules SET session_days = ? WHERE course_id = ? AND instructor_id = ?
                       """, (session_days, course_id, intructor_id))
        conn.commit()
        cursor.close()
        conn.close()

    @classmethod
    def update_start_time(cls, intructor_id):
        course_id = int(input("Course ID: "))
        courses = Course.get_data()
        for course in courses:
            if course.intructor_id == intructor_id and course.course_id == course_id:
                break
        else:
            print("You don't own this course!")
            return None
        start_time = input("Start Time: ")
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("""UPDATE Schedules SET start_time = ? WHERE course_id = ? AND instructor_id = ?
                       """, (start_time, course_id, intructor_id))
        conn.commit()
        cursor.close()
        conn.close()

    @classmethod
    def update_end_time(cls, intructor_id):
        course_id = int(input("Course ID: "))
        courses = Course.get_data()
        for course in courses:
            if course.intructor_id == intructor_id and course.course_id == course_id:
                break
        else:
            print("You don't own this course!")
            return None
        end_time = input("End Time: ")
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("""UPDATE Schedules SET end_time = ? WHERE course_id = ? AND instructor_id = ?
                       """, (end_time, course_id, intructor_id))
        conn.commit()
        cursor.close()
        conn.close()

    @classmethod
    def update_location(cls, intructor_id):
        course_id = int(input("Course ID: "))
        courses = Course.get_data()
        for course in courses:
            if course.intructor_id == intructor_id and course.course_id == course_id:
                break
        else:
            print("You don't own this course!")
            return None
        location = input("Location: ")
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("""UPDATE Schedules SET location = ? WHERE course_id = ? AND instructor_id = ?
                       """, (location, course_id, intructor_id))
        conn.commit()
        cursor.close()
        conn.close()

    @classmethod
    def update_time_zone(cls, intructor_id):
        course_id = int(input("Course ID: "))
        courses = Course.get_data()
        for course in courses:
            if course.intructor_id == intructor_id and course.course_id == course_id:
                break
        else:
            print("You don't own this course!")
            return None
        time_zone = input("Time Zone: ")
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("""UPDATE Schedules SET time_zone = ? WHERE course_id = ? AND instructor_id = ?
                       """, (time_zone, course_id, intructor_id))
        conn.commit()
        cursor.close()
        conn.close()

    @classmethod
    def get_schedule(cls):
        course_id = int(input("Course ID: "))
        schedules = cls.get_data()
        content = []
        for schedule in schedules:
            if course_id == schedule.course_id:
                content.append([schedule.course_id, schedule.instructor_id, schedule.session_days, schedule.start_time, schedule.end_time, schedule.location, schedule.time_zone])
                break

        else:
            print("Course Doesn't exist or does not have a schedule")
            return
        
        header = ["Course ID","Intructor ID","Session Days","Start Time","End Time","Location","Time Zone" ]
        print(tabulate(content, header, tablefmt="pretty"))


        
        

