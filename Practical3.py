
import csv
import mysql.connector

def connect():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="YOUR_PASSWORD",
        database="college"
    )

def create_tables(conn):
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS Student(
            student_id INT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            spi DECIMAL(3,2) NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS CourseRegistration(
            student_id INT,
            course_id VARCHAR(20),
            FOREIGN KEY(student_id) REFERENCES Student(student_id)
        )
    """)

    conn.commit()
    cur.close()

def insert_students(conn, filename):
    cur = conn.cursor()

    with open(filename, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            cur.execute(
                "INSERT IGNORE INTO Student VALUES (%s,%s,%s)",
                (row["student_id"], row["name"], row["spi"])
            )

    conn.commit()
    cur.close()

def insert_registrations(conn, filename):
    cur = conn.cursor()

    with open(filename, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            cur.execute(
                "INSERT INTO CourseRegistration VALUES (%s,%s)",
                (row["student_id"], row["course_id"])
            )

    conn.commit()
    cur.close()

def show_students(conn, course_id, threshold):
    cur = conn.cursor()

    cur.execute("""
        SELECT s.student_id, s.name, s.spi, r.course_id
        FROM Student s
        JOIN CourseRegistration r
        ON s.student_id = r.student_id
        WHERE r.course_id = %s AND s.spi > %s
        ORDER BY s.spi DESC, s.student_id ASC
    """, (course_id, threshold))

    for row in cur:
        print(*row)

    cur.close()

def main():
    student_file = input("Student CSV: ").strip()
    registration_file = input("Registration CSV: ").strip()
    course_id = input("Course ID: ").strip()

    try:
        threshold = float(input("SPI threshold: "))

        if not 0 <= threshold <= 10:
            raise ValueError("SPI must be between 0 and 10")

        conn = connect()
        create_tables(conn)
        insert_students(conn, student_file)
        insert_registrations(conn, registration_file)
        show_students(conn, course_id, threshold)
        conn.close()

    except (ValueError, mysql.connector.Error, FileNotFoundError) as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
