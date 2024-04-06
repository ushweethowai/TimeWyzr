
# TimeWyzr

TimeWyzr is a Python-based tool designed to help individuals organize their tasks based on priority, energy level, and personal schedules. By collecting user data through a structured format, Task Scheduler personalizes task allocation throughout the week, optimizing productivity and ensuring time management aligns with personal energy levels and priorities.

## Features

- **Personalized Task Scheduling:** Dynamically schedules tasks based on the user's input regarding energy levels, priority, and duration.
- **Priority and Energy Level Assessment:** Categorizes tasks into high, medium, and low priorities and energy levels to fit the user's daily rhythms.
- **Weekly Planning:** Generates a weekly schedule that accommodates personal and professional obligations.

## Installation

To get started with Task Scheduler, clone this repository to your local machine using:

```bash
git clone https://github.com/yourusername/task-scheduler.git
```

Ensure you have Python installed on your system. Task Scheduler has been tested on Python 3.8 and above.

## Usage

The project consists of three main components:

1. **`userData.py`**: This module collects and formats user data regarding tasks, including the task name, energy level, priority, and duration.

2. **`priority.py`**: Defines the logic for sorting and prioritizing tasks based on the user-defined criteria.

3. **`main.py`**: The core execution script that integrates user data with the scheduling logic to generate a personalized task schedule.

To run the Task Scheduler, navigate to the project directory and execute:

```bash
python main.py
```

Follow the on-screen prompts to input your tasks and preferences.

