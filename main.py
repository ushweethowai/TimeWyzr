from datetime import datetime, timedelta
import userData

# Task structure: {'name': str, 'energy': 'HE'/'ME'/'LE', 'priority': int, 'duration': int (in minutes)}

def parse_tasks(task_inputs):
    """
    Parses user input into a structured task list.
    task_inputs: List of tuples [(task_name, energy_level, priority_level, duration), ...]
    """
    tasks = [{'name': name, 'energy': energy, 'priority': priority, 'duration': duration}
             for name, energy, priority, duration in task_inputs]
    return tasks

def sort_tasks(tasks):
    """
    Sorts tasks based on priority level (higher first) and energy level (HE > ME > LE).
    """
    energy_order = {'HE': 3, 'ME': 2, 'LE': 1}
    sorted_tasks = sorted(tasks, key=lambda x: (x['priority'], energy_order[x['energy']]), reverse=True)
    return sorted_tasks

def find_next_weekday(start_date, weekday):
    """
    Finds the next specific weekday (0=Monday, 1=Tuesday, ..., 6=Sunday) from a given start date.
    """
    days_ahead = weekday - start_date.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return start_date + timedelta(days_ahead)

# def allocate_tasks(tasks, person_state, start_date):
#     """
#     Allocates tasks to appropriate times of the day based on person's state (M, A, E) from Monday to Friday.
#     """
#     time_slots = {
#         'M': (6, 12),
#         'A': (12, 18),
#         'E': (18, 23)
#     }
#     start, end = time_slots[person_state]
#     schedule = [[] for _ in range(5)] # Monday to Friday
#     current_day_index = 0
#     current_time = find_next_weekday(start_date, 0).replace(hour=start, minute=0, second=0, microsecond=0) # Start from the next Monday

#     for task in tasks:
#         if current_day_index >= 5: # Only schedule from Monday to Friday
#             break

#         end_time = current_time + timedelta(minutes=task['duration'])
#         if end_time.hour > end or end_time.day != current_time.day:
#             # Move to the next available time slot, respecting the weekday constraint
#             current_day_index += 1
#             if current_day_index >= 5: # Check again in case we've moved past Friday
#                 break
#             current_time = current_time + timedelta(days=(1 if current_time.weekday() < 4 else 3)) # Skip to next Monday if needed
#             current_time = current_time.replace(hour=start, minute=0, second=0, microsecond=0)
#             end_time = current_time + timedelta(minutes=task['duration'])
        
#         task_schedule = {
#             'name': task['name'],
#             'start': current_time.strftime("%Y-%m-%d %H:%M"),
#             'end': end_time.strftime("%Y-%m-%d %H:%M")
#         }
#         schedule[current_day_index].append(task_schedule)
#         current_time = end_time if end_time.hour < end else current_time.replace(hour=start, minute=0) + timedelta(days=1)

#     return schedule

def allocate_tasks(tasks, person_state, start_date):
    """
    Allocates tasks to appropriate times of the day based on person's state (M, A, E) from Monday to Friday,
    scheduling low-energy tasks later in the day and including breaks between tasks.
    """
    time_slots = {
        'M': (6, 12),
        'A': (12, 18),
        'E': (18, 23)
    }
    break_duration = {
        'HE': 60,
        'ME': 30,
        'LE': 30
    }
    start, end = time_slots[person_state]
    schedule = [[] for _ in range(5)]  # Monday to Friday
    current_day_index = 0
    current_time = find_next_weekday(start_date, 0).replace(hour=start, minute=0, second=0, microsecond=0)  # Start from the next Monday

    # Sort tasks by priority, then by energy level (reverse), and finally by duration for LE tasks later
    sorted_tasks = sorted(tasks, key=lambda x: (x['priority'], -break_duration[x['energy']], x['duration'] if x['energy'] == 'LE' else -x['duration']), reverse=True)

    for task in sorted_tasks:
        if current_day_index >= 5:  # Only schedule from Monday to Friday
            break

        # Add break duration based on previous task's energy level (if there was a previous task)
        if schedule[current_day_index]:
            current_time += timedelta(minutes=break_duration[schedule[current_day_index][-1]['energy']])

        end_time = current_time + timedelta(minutes=task['duration'])
        if end_time.hour > end or end_time.day != current_time.day:
            # Move to the next available time slot, respecting the weekday constraint
            current_day_index += 1
            if current_day_index >= 5:  # Check again in case we've moved past Friday
                break
            current_time = current_time + timedelta(days=(1 if current_time.weekday() < 4 else 3))  # Skip to next Monday if needed
            current_time = current_time.replace(hour=start, minute=0, second=0, microsecond=0)
            end_time = current_time + timedelta(minutes=task['duration'])

        task_schedule = {
            'name': task['name'],
            'start': current_time.strftime("%Y-%m-%d %H:%M"),
            'end': end_time.strftime("%Y-%m-%d %H:%M"),
            'energy': task['energy']  # Keep track of energy for scheduling breaks
        }
        schedule[current_day_index].append(task_schedule)
        current_time = end_time

    return schedule

def generate_schedule(task_inputs, person_state, start_date):
    """
    Generates a weekly schedule based on tasks, their priorities, energy levels, and person's state, starting from a specific date.
    """
    tasks = parse_tasks(task_inputs)
    sorted_tasks = sort_tasks(tasks)
    weekly_schedule = allocate_tasks(sorted_tasks, person_state, start_date)
    return weekly_schedule

# # Example usage
# task_inputs = [
#     ('Task 1', 'HE', 1, 60),
#     ('Task 2', 'ME', 2, 45),
#     ('Task 60', 'LE', 3, 109),
#     ('Task 82', 'ME', 2, 43),
#     ('Task 41', 'HE', 2, 113),
#     ('Task 18', 'ME', 2, 102),
#     ('Task 94', 'LE', 2, 50),
#     ('Task 51', 'HE', 3, 114),
#     ('Task 52', 'LE', 2, 48),
#     ('Task 45', 'LE', 1, 41),
#     ('Task 47', 'HE', 3, 50),
#     ('Task 91', 'HE', 1, 17),
#     ('Task 7', 'HE', 3, 104),
#     ('Task 87', 'HE', 1, 42),
#     ('Task 3', 'LE', 3, 74),
#     ('Task 58', 'HE', 1, 114)
#     # Add more tasks as needed
# ]

task_inputs = [
    ('Math Homework', 'HE', 2, 60),
    ('Science Project', 'ME', 3, 45),
    ('English Essay', 'LE', 1, 109),
    ('History Presentation', 'ME', 2, 43),
    ('Biology Lab Report', 'HE', 3, 113),
    ('Economics Research', 'ME', 1, 102),
    ('Art Assignment', 'LE', 2, 50),
    ('Marketing Strategy', 'HE', 3, 114),
    ('Programming Exercise', 'LE', 2, 48),
    ('Yoga Session', 'LE', 1, 41),
    ('Professional Networking', 'HE', 3, 50),
    ('Coffee Break', 'LE', 1, 17),
    ('Team Meeting', 'HE', 3, 104),
    ('Client Feedback Review', 'HE', 2, 42),
    ('Reading Time', 'LE', 3, 74),
    ('Creative Writing', 'HE', 1, 114),
    ('Physics Problem Set', 'ME', 2, 65),
    ('Philosophy Reading', 'LE', 2, 33),
    ('Music Practice', 'ME', 1, 120),
    ('Workout', 'HE', 1, 90),
    ('Language Learning', 'ME', 2, 30),
    ('Meditation', 'LE', 3, 20),
    ('Tech Workshop', 'HE', 3, 80),
    ('Cooking Class', 'ME', 1, 75),
    ('Volunteering', 'LE', 2, 60),
    ('Gardening', 'LE', 1, 45),
    ('Online Course', 'ME', 3, 50),
    ('Financial Planning', 'HE', 2, 30),
    ('Book Club Discussion', 'LE', 1, 60),
    ('Personal Branding', 'ME', 2, 40),
    ('Data Analysis Project', 'HE', 3, 55),
    ('UX Design Review', 'ME', 1, 35),
    ('Travel Planning', 'LE', 2, 25),
    ('Digital Detox', 'LE', 3, 15),
    ('SEO Optimization', 'ME', 2, 70),
    ('Networking Event Preparation', 'HE', 1, 85),
    ('Photography', 'LE', 1, 95),
    ('Portfolio Update', 'HE', 2, 110),
    ('Mental Health Day', 'LE', 3, 30),
    ('Strategic Planning Session', 'HE', 3, 45),
    ('Customer Service Training', 'ME', 2, 35),
    ('Home Renovation Planning', 'LE', 1, 55),
    ('Investment Research', 'HE', 2, 40),
    ('Public Speaking Practice', 'ME', 3, 50),
    ('Social Media Cleanup', 'LE', 1, 20),
    ('Podcast Recording', 'HE', 3, 60),
    ('Graphic Design Project', 'ME', 2, 75),
    ('Personal Development Workshop', 'HE', 1, 80),
    ('Sustainability Research', 'LE', 2, 45),
    ('Cultural Studies Essay', 'ME', 3, 60)
]


person_state = 'M' # 'M', 'A', or 'E'
start_date = datetime.now() # Starting point to find the next Monday

schedule = generate_schedule(task_inputs, person_state, start_date)
for day, tasks in enumerate(schedule, start=1):
    # print(f"Day {day} (Tasks):")
    for task in tasks:
        print(f"- {task['name']}: {task['start']} to {task['end']}")






