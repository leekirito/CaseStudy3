import pyodbc

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
        
        schedules = []
        for row in rows:
            schedules.append(cls(
                schedule_id=row.schedule_id,
                course_id=row.course_id,
                instructor_id=row.instructor_id,
                session_days=row.session_days,
                start_time=row.start_time,
                end_time=row.end_time,
                location=row.location,
                time_zone=row.time_zone
            ))
        
        cursor.close()
        conn.close()
        return schedules
