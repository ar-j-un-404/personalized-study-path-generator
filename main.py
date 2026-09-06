from datetime import datetime, timedelta
from pathlib import Path
import json

DATA_FILE = Path("study_plan.json")

REVISION_RATIO = 0.20
LEARNING_RATIO = 0.80

priority_score = {
    "low": 1,
    "medium": 2,
    "high": 3
}

difficulty_score = {
    "low": 1,
    "medium": 2,
    "high": 3
}

level_score = {
    "beginner": 3,
    "intermediate": 2,
    "advanced": 1
}

def positive_int(message):
    while True:
        try:
            value = int(input(message))
            if value > 0:
                return value
            print("Enter a number greater than 0")
        except ValueError:
            print("Enter a valid whole number")

def positive_float(message):
    while True:
        try:
            value = float(input(message))
            if value > 0:
                return value
            print("Enter a number greater than 0")
        except ValueError:
            print("Enter a valid number")

def choice_input(message, allowed):
    while True:
        value = input(message).lower()
        if value in allowed:
            return value
        print("Invalid input")

def future_date_input():
    while True:
        date = input("Enter exam date (DD-MM-YYYY): ")
        try:
            exam_date = datetime.strptime(date, "%d-%m-%Y").date()
            today = datetime.today().date()
            if exam_date > today:
                return date
            print("Exam date must be in the future")
        except ValueError:
            print("Invalid date")

def calculate_score(level, difficulty, priority):
    lvl_number = level_score[level]
    diff_number = difficulty_score[difficulty]
    prior_number = priority_score[priority]
    total_score = lvl_number + diff_number + prior_number
    return total_score

def get_remaining_days(date):
    exam_date = datetime.strptime(date, "%d-%m-%Y").date()
    today = datetime.today().date()
    remaining = (exam_date - today).days
    return max(remaining, 0)

def collect_student():
    student = {}

    student["name"] = input("Enter student name: ")

    student["daily_hours"] = positive_float(
        "How many hours can you study per day: "
    )

    number_subjects = positive_int(
        "How many subjects: "
    )

    subjects = []

    for i in range(number_subjects):
        print("\nSubject", i + 1)

        sub_name = input("Enter subject name: ")

        topic_count = positive_int(
            "Enter number of topics: "
        )

        topic_names = []

        for j in range(topic_count):
            topic = input(
                f"Enter topic {j + 1}: "
            )
            topic_names.append(topic)

        level = choice_input(
            "Knowledge level (beginner/intermediate/advanced): ",
            ["beginner", "intermediate", "advanced"]
        )

        difficulty = choice_input(
            "Difficulty (low/medium/high): ",
            ["low", "medium", "high"]
        )

        priority = choice_input(
            "Priority (low/medium/high): ",
            ["low", "medium", "high"]
        )

        exam_date = future_date_input()

        total_score = calculate_score(
            level,
            difficulty,
            priority
        )

        remaining_days = get_remaining_days(
            exam_date
        )

        subject = {
            "subject_name": sub_name,
            "topic_count": topic_count,
            "topic_names": topic_names,
            "level": level,
            "difficulty": difficulty,
            "priority": priority,
            "exam_date": exam_date,
            "total_score": total_score,
            "remaining_days": remaining_days
        }

        subjects.append(subject)

    student["subjects"] = subjects
    student["progress"] = {}

    return student

def refresh_remaining_days(student):
    for subject in student["subjects"]:
        subject["remaining_days"] = get_remaining_days(
            subject["exam_date"]
        )

def allocate_subject_hours(student):
    refresh_remaining_days(student)

    subjects = student["subjects"]

    active_subjects = [
        subject
        for subject in subjects
        if subject["remaining_days"] > 0
    ]

    if not active_subjects:
        return

    all_score = 0

    for subject in active_subjects:
        all_score += subject["total_score"]

    max_days = max(
        subject["remaining_days"]
        for subject in active_subjects
    )

    learning_hours_per_day = (
        student["daily_hours"]
        * LEARNING_RATIO
    )

    total_available_learning_hours = (
        learning_hours_per_day
        * max_days
    )

    for subject in subjects:
        if subject["remaining_days"] <= 0:
            subject["percentage"] = 0
            subject["allocated_hr"] = 0
            subject["hr_per_topic"] = 0
            continue

        percentage = (
            subject["total_score"]
            / all_score
        )

        allocated_hr = (
            percentage
            * total_available_learning_hours
        )

        maximum_before_exam = (
            learning_hours_per_day
            * subject["remaining_days"]
        )

        allocated_hr = min(
            allocated_hr,
            maximum_before_exam
        )

        subject["percentage"] = percentage
        subject["allocated_hr"] = allocated_hr

        subject["hr_per_topic"] = (
            allocated_hr
            / subject["topic_count"]
        )

def make_progress_key(subject_name, topic_name):
    return subject_name + "||" + topic_name

def create_topic_work(student):
    work = []

    for subject in student["subjects"]:
        if subject["remaining_days"] <= 0:
            continue

        for topic in subject["topic_names"]:
            key = make_progress_key(
                subject["subject_name"],
                topic
            )

            completed_hours = student["progress"].get(
                key,
                0
            )

            remaining_topic_hours = (
                subject["hr_per_topic"]
                - completed_hours
            )

            remaining_topic_hours = max(
                remaining_topic_hours,
                0
            )

            if remaining_topic_hours > 0:
                work.append({
                    "subject": subject["subject_name"],
                    "topic": topic,
                    "remaining_hours": remaining_topic_hours,
                    "deadline": subject["remaining_days"],
                    "score": subject["total_score"]
                })

    return work

def generate_schedule(student):
    allocate_subject_hours(student)

    topic_work = create_topic_work(student)

    schedule = {}

    if not topic_work:
        return schedule

    daily_hours = student["daily_hours"]

    learning_limit = (
        daily_hours
        * LEARNING_RATIO
    )

    revision_limit = (
        daily_hours
        * REVISION_RATIO
    )

    active_subjects = [
        subject
        for subject in student["subjects"]
        if subject["remaining_days"] > 0
    ]

    if not active_subjects:
        return schedule

    max_days = max(
        subject["remaining_days"]
        for subject in active_subjects
    )

    today = datetime.today().date()

    task_id = 1

    for day_number in range(1, max_days + 1):
        day_key = f"Day {day_number}"

        schedule[day_key] = {
            "date": (
                today
                + timedelta(days=day_number - 1)
            ).strftime("%d-%m-%Y"),
            "tasks": []
        }

        remaining_daily_hours = learning_limit

        while remaining_daily_hours > 0:
            available_topics = [
                item
                for item in topic_work
                if (
                    item["remaining_hours"] > 0
                    and day_number <= item["deadline"]
                )
            ]

            if not available_topics:
                break

            available_topics.sort(
                key=lambda item: (
                    item["deadline"],
                    -item["score"]
                )
            )

            topic = available_topics[0]

            chunk = min(
                1,
                topic["remaining_hours"],
                remaining_daily_hours
            )

            schedule[day_key]["tasks"].append({
                "id": task_id,
                "type": "study",
                "subject": topic["subject"],
                "topic": topic["topic"],
                "hours": round(chunk, 2),
                "completed": False
            })

            task_id += 1

            topic["remaining_hours"] -= chunk

            remaining_daily_hours -= chunk

        if day_number > 1:
            previous_day = schedule[
                f"Day {day_number - 1}"
            ]

            previous_topics = []

            for task in previous_day["tasks"]:
                if task["type"] == "study":
                    value = (
                        task["subject"],
                        task["topic"]
                    )

                    if value not in previous_topics:
                        previous_topics.append(value)

            if previous_topics:
                revision_per_topic = (
                    revision_limit
                    / len(previous_topics)
                )

                for subject_name, topic_name in previous_topics:
                    schedule[day_key]["tasks"].append({
                        "id": task_id,
                        "type": "revision",
                        "subject": subject_name,
                        "topic": topic_name,
                        "hours": round(
                            revision_per_topic,
                            2
                        ),
                        "completed": False
                    })

                    task_id += 1

    return schedule

def print_schedule(schedule):
    print("\n" + "=" * 50)
    print("PERSONALIZED STUDY PLAN")
    print("=" * 50)

    if not schedule:
        print("No study tasks available")
        return

    for day, data in schedule.items():
        print("\n", day, "-", data["date"])

        total_hours = 0

        for task in data["tasks"]:
            if task["completed"]:
                status = "Done"
            else:
                status = "Pending"

            print(
                f"[{task['id']}] "
                f"{task['type']} | "
                f"{task['subject']} | "
                f"{task['topic']} | "
                f"{task['hours']} hours | "
                f"{status}"
            )

            total_hours += task["hours"]

        print(
            "Total planned:",
            round(total_hours, 2),
            "hours"
        )

def ask_ai(student, schedule, question):
    try:
        from langchain_ollama import ChatOllama
    except ImportError:
        print("Install langchain-ollama first")
        return

    try:
        llm = ChatOllama(
            model="qwen3:4b"
        )

        context = ""

        count = 0

        for day, data in schedule.items():
            context += (
                f"\n{day} "
                f"{data['date']}\n"
            )

            for task in data["tasks"]:
                context += (
                    f"{task['type']} - "
                    f"{task['subject']} - "
                    f"{task['topic']} - "
                    f"{task['hours']} hours\n"
                )

            count += 1

            if count == 7:
                break

        prompt = f"""
You are a study planning assistant.

Student:
{student["name"]}

Available study hours per day:
{student["daily_hours"]}

Study plan:
{context}

Question:
{question}

Give practical advice based on the study plan.
"""

        response = llm.invoke(prompt)

        print(
            "\nAI:",
            response.content
        )

    except Exception as error:
        print("Could not connect to Ollama")
        print("Make sure Ollama is running")
        print(error)

def find_task(schedule, task_id):
    for day in schedule.values():
        for task in day["tasks"]:
            if task["id"] == task_id:
                return task

    return None

def mark_completed(student, schedule):
    try:
        task_id = int(
            input("Enter task id: ")
        )

    except ValueError:
        print("Invalid task id")
        return

    task = find_task(
        schedule,
        task_id
    )

    if task is None:
        print("Task not found")
        return

    if task["completed"]:
        print("Task already completed")
        return

    task["completed"] = True

    if task["type"] == "study":
        key = make_progress_key(
            task["subject"],
            task["topic"]
        )

        student["progress"][key] = (
            student["progress"].get(
                key,
                0
            )
            + task["hours"]
        )

    print("Task completed")

def show_progress(student):
    allocate_subject_hours(student)

    total_required = 0
    total_completed = 0

    for subject in student["subjects"]:
        required = subject.get(
            "allocated_hr",
            0
        )

        completed = 0

        for topic in subject["topic_names"]:
            key = make_progress_key(
                subject["subject_name"],
                topic
            )

            completed += student["progress"].get(
                key,
                0
            )

        completed = min(
            completed,
            required
        )

        if required > 0:
            percentage = (
                completed
                / required
                * 100
            )
        else:
            percentage = 0

        print(
            subject["subject_name"],
            ":",
            round(percentage, 1),
            "%"
        )

        total_required += required
        total_completed += completed

    if total_required > 0:
        overall = (
            total_completed
            / total_required
            * 100
        )
    else:
        overall = 0

    print(
        "Overall progress:",
        round(overall, 1),
        "%"
    )

def change_daily_hours(student):
    student["daily_hours"] = positive_float(
        "Enter new study hours per day: "
    )

def change_priority(student):
    name = input(
        "Enter subject name: "
    ).lower()

    for subject in student["subjects"]:
        if (
            subject["subject_name"].lower()
            == name
        ):
            priority = choice_input(
                "New priority (low/medium/high): ",
                ["low", "medium", "high"]
            )

            subject["priority"] = priority

            subject["total_score"] = calculate_score(
                subject["level"],
                subject["difficulty"],
                subject["priority"]
            )

            print("Priority updated")
            return

    print("Subject not found")

def save_data(student, schedule):
    data = {
        "student": student,
        "schedule": schedule
    }

    with open(
        DATA_FILE,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            data,
            file,
            indent=4
        )

    print("Study data saved")

def load_data():
    if not DATA_FILE.exists():
        return None, None

    with open(
        DATA_FILE,
        "r",
        encoding="utf-8"
    ) as file:
        data = json.load(file)

    return (
        data["student"],
        data["schedule"]
    )

def main():
    print(
        "PERSONALIZED STUDY PATH GENERATOR"
    )

    if DATA_FILE.exists():
        option = input(
            "Type load to open saved plan "
            "or press Enter for new plan: "
        ).lower()
    else:
        option = ""

    if option == "load":
        student, schedule = load_data()

    else:
        student = collect_student()

        schedule = generate_schedule(
            student
        )

        save_data(
            student,
            schedule
        )

    while True:
        print(
            "\n1. View study plan"
            "\n2. Mark task completed"
            "\n3. View progress"
            "\n4. Replan remaining work"
            "\n5. Change daily hours"
            "\n6. Change subject priority"
            "\n7. AI study tips"
            "\n8. Ask AI"
            "\n9. Save"
            "\n0. Exit"
        )

        choice = input("Choose: ")

        if choice == "1":
            print_schedule(schedule)

        elif choice == "2":
            mark_completed(
                student,
                schedule
            )

            save_data(
                student,
                schedule
            )

        elif choice == "3":
            show_progress(student)

        elif choice == "4":
            schedule = generate_schedule(
                student
            )

            print("Schedule replanned")

            save_data(
                student,
                schedule
            )

        elif choice == "5":
            change_daily_hours(student)

            schedule = generate_schedule(
                student
            )

            save_data(
                student,
                schedule
            )

        elif choice == "6":
            change_priority(student)

            schedule = generate_schedule(
                student
            )

            save_data(
                student,
                schedule
            )

        elif choice == "7":
            ask_ai(
                student,
                schedule,
                "Explain how I should follow "
                "this study plan and give me "
                "useful study tips."
            )

        elif choice == "8":
            question = input(
                "Ask about your plan: "
            )

            ask_ai(
                student,
                schedule,
                question
            )

        elif choice == "9":
            save_data(
                student,
                schedule
            )

        elif choice == "0":
            save_data(
                student,
                schedule
            )

            print("Good bye")

            break

        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()

