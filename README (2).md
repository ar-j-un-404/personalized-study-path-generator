# Personalized Study Path Generator

A Python-based AI study planning tool that creates a personalized study schedule based on a student's subjects, topics, knowledge level, difficulty, priority, exam dates, and available study time.

## Features

- Collects multiple subjects and topics
- Validates user inputs
- Calculates subject priority scores
- Calculates remaining days until exams
- Allocates study time based on subject importance
- Distributes hours across topics
- Generates a day-by-day study schedule
- Reserves time for revision
- Tracks completed study tasks
- Shows study progress
- Supports dynamic replanning
- Allows changes to daily study hours and subject priority
- Saves study data using JSON
- Loads previously saved plans
- Provides AI study tips and plan-related answers using Ollama

## How It Works

```text
Student Input
    ↓
Input Validation
    ↓
Priority Scoring
    ↓
Remaining Days Calculation
    ↓
Study Hour Allocation
    ↓
Topic Hour Allocation
    ↓
Daily Schedule Generation
    ↓
Revision Planning
    ↓
Progress Tracking
    ↓
Dynamic Replanning
    ↓
Ollama AI Assistance
```

## Priority Scoring

Priority:

```text
Low = 1
Medium = 2
High = 3
```

Difficulty:

```text
Low = 1
Medium = 2
High = 3
```

Knowledge level:

```text
Advanced = 1
Intermediate = 2
Beginner = 3
```

The final subject importance score is calculated from these values. Subjects with higher scores receive more study attention.

## Project Structure

```text
personalized-study-path-generator/
│
├── main.py
├── requirements.txt
├── README.md
└── study_plan.json
```

`study_plan.json` is created automatically when study data is saved. It is recommended to keep this file out of Git because it may contain personal study information.

## Requirements

- Python 3.10 or newer
- Ollama
- qwen3:4b Ollama model

## Installation

Clone the repository:

```bash
git clone https://github.com/ar-j-un-404/personalized-study-path-generator.git
cd personalized-study-path-generator
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Install the Python dependencies:

```bash
pip install -r requirements.txt
```

Install Ollama separately if it is not already installed. Then download the model:

```bash
ollama pull qwen3:4b
```

## Usage

Run the program:

```bash
python main.py
```

The application allows you to:

```text
1. View study plan
2. Mark task completed
3. View progress
4. Replan remaining work
5. Change daily hours
6. Change subject priority
7. Get AI study tips
8. Ask AI about the plan
9. Save
0. Exit
```

## Data Storage

The application stores user data and the generated schedule in `study_plan.json`. This allows the study plan to be loaded again after restarting the program.

## AI Integration

The project uses Ollama with `qwen3:4b`. The AI component is used for natural-language study advice and questions about the generated plan.

The core scheduling system itself is implemented using normal Python logic rather than relying entirely on the LLM.

## Current Limitations

- Uses a command-line interface
- Topic difficulty is currently inherited from the subject rather than scored individually
- Scheduling uses rule-based allocation
- AI responses depend on the locally installed Ollama model
- The planner is an educational MVP

## Future Improvements

- Web interface
- Individual topic priority and difficulty
- Smarter revision scheduling
- Better deadline-aware scheduling
- Calendar integration
- Notifications and reminders
- Study streak tracking
- More advanced progress analytics
- AI-based plan adjustment from natural-language feedback
- Database storage
- User accounts

## Learning Goals

This project was built to practice:

- Python
- Dictionaries and lists
- Loops
- Functions
- Input validation
- Exception handling
- Date and time handling
- JSON storage
- Scheduling algorithms
- Priority-based allocation
- Progress tracking
- LLM integration
- Ollama
- AI application design

## Author

Arjun

GitHub: ar-j-un-404
