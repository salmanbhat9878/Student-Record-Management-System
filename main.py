import csv
import json
from pathlib import Path

DATA_FILE = Path(__file__).with_name("students.json")


def load_students():
    if not DATA_FILE.exists():
        return []
    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
        if not isinstance(data, list):
            raise ValueError("JSON data must be a list.")
        return data
    except (json.JSONDecodeError, OSError, ValueError) as error:
        print(f"Could not load student data: {error}")
        return []


def save_students(students):
    try:
        with DATA_FILE.open("w", encoding="utf-8") as file:
            json.dump(students, file, indent=4)
        return True
    except OSError as error:
        print(f"Could not save student data: {error}")
        return False


def get_gpa():
    while True:
        try:
            gpa = float(input("Enter GPA (0-10): "))
            if 0 <= gpa <= 10:
                return gpa
            print("GPA must be between 0 and 10.")
        except ValueError:
            print("Please enter a valid number.")


def add_student(students):
    student_id = input("Enter student ID: ").strip()
    if not student_id:
        print("Student ID cannot be empty.")
        return
    if any(s["id"].casefold() == student_id.casefold() for s in students):
        print("That student ID already exists.")
        return

    name = input("Enter full name: ").strip()
    email = input("Enter email: ").strip()
    if not name:
        print("Name cannot be empty.")
        return
    if not email or "@" not in email or "." not in email.split("@")[-1]:
        print("Please enter a valid email address.")
        return

    students.append({"id": student_id, "name": name, "email": email, "gpa": get_gpa()})
    if save_students(students):
        print("Student added successfully.")


def view_students(students):
    if not students:
        print("No student records found.")
        return
    for student in students:
        print(f'ID: {student["id"]} | Name: {student["name"]} | Email: {student["email"]} | GPA: {student["gpa"]}')


def search_student(students):
    query = input("Search by ID or name: ").strip().casefold()
    matches = [s for s in students if query in s["id"].casefold() or query in s["name"].casefold()]
    if matches:
        view_students(matches)
    else:
        print("No matching student found.")


def update_student(students):
    student_id = input("Enter the ID of the student to update: ").strip().casefold()
    student = next((s for s in students if s["id"].casefold() == student_id), None)
    if student is None:
        print("Student not found.")
        return
    name = input(f'New name (Enter to keep {student["name"]}): ').strip()
    email = input(f'New email (Enter to keep {student["email"]}): ').strip()
    if name:
        student["name"] = name
    if email:
        if "@" not in email or "." not in email.split("@")[-1]:
            print("Invalid email; update cancelled.")
            return
        student["email"] = email
    change_gpa = input("Change GPA? (y/n): ").strip().casefold()
    if change_gpa == "y":
        student["gpa"] = get_gpa()
    if save_students(students):
        print("Student updated successfully.")


def delete_student(students):
    student_id = input("Enter the ID of the student to delete: ").strip().casefold()
    student = next((s for s in students if s["id"].casefold() == student_id), None)
    if student is None:
        print("Student not found.")
        return
    confirm = input(f'Delete {student["name"]}? (y/n): ').strip().casefold()
    if confirm == "y":
        students.remove(student)
        if save_students(students):
            print("Student deleted successfully.")


import csv

def sort_students_by_name(students):
    if not students:
        print("No student records found.")
        return

    sorted_students = sorted(
        students,
        key=lambda student: student["name"].lower()
    )

    print("\n=== Students Sorted by Name ===")
    for student in sorted_students:
        print(
            f'ID: {student["id"]} | '
            f'Name: {student["name"]} | '
            f'Email: {student["email"]} | '
            f'GPA: {student["gpa"]}'
        )


def export_students_csv(students):
    try:
        with open("students.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=["id", "name", "email", "gpa"]
            )
            writer.writeheader()
            writer.writerows(students)

        print("Students exported to students.csv successfully.")

    except OSError as error:
        print(f"Could not export students: {error}")


def main():
    students = load_students()

    actions = {
        "1": add_student,
        "2": view_students,
        "3": search_student,
        "4": update_student,
        "5": delete_student,
        "7": lambda: export_students_csv(students),
        "8": sort_students_by_name
    }

    while True:
        print("\n=== Student Record Management System ===")
        print("1. Add student\n2. View all students\n3. Search student")
        print("4. Update student\n5. Delete student\n6. Exit\n7. Export students to CSV")
        print("8. Sort students by name")
        choice = input("Choose an option (1-8): ").strip()

        if choice == "6":
            print("Goodbye!")
            break

        action = actions.get(choice)

        if choice == "7":
            action()
        elif action:
            try:
                action(students)
            except (KeyError, TypeError) as error:
                print(f"Invalid student data: {error}")
        else:
            print("Please choose a number from 1 to 8.")


if __name__ == "__main__":
    main()