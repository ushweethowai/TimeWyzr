def input_continue(user_input):
    return user_input.strip().lower() != "end"

def prompt_for_level(scanner, level_type):
    valid_levels = ["LOW", "MEDIUM", "HIGH"]
    while True:
        level = input(f"Please enter level (LOW/MEDIUM/HIGH) for {level_type}: ").upper()
        if level in valid_levels:
            return level
        else:
            print("Invalid level. Please enter LOW/MEDIUM/HIGH.")

def prompt_for_time():
    while True:
        input_str = input("Please enter the time(min/hour): ").strip()
        parts = input_str.split(" ")
        if len(parts) > 0:
            try:
                time = int(parts[0])
                return str(time) + parts[1]
            except ValueError:
                print("Invalid input. Please enter a valid number followed by the unit (min/hour).")

def main():
    task_input = ""
    task_priority_map = {}
    task_duration_map = {}
    task_energy_map = {}
    priority = Priority()

    print("Please enter your task information (type 'end' to finish):")
    while not input_continue(task_input := input()):
        if task_input.strip() == "":
            print("Please enter correctly:")
            continue
        
        difficulty_level = prompt_for_level(input, "difficulty")
        urgency_level = prompt_for_level(input, "urgency")
        time = prompt_for_time()
        
        priority_level_string = priority.get_priority(urgency_level, difficulty_level)
        priority_level_num = {"HIGH": 3, "MEDIUM": 2, "LOW": 1}[priority_level_string]
        energy_level = {"HIGH": "HE", "MEDIUM": "ME", "LOW": "LE"}[priority_level_string]
        
        task_duration_map[task_input] = time
        task_priority_map[task_input] = priority_level_num
        task_energy_map[task_input] = energy_level
        
        print("Please enter your next task information (type 'end' to finish):")
    
    print("All tasks and their details:")
    for task, priority in task_priority_map.items():
        print(f"Task: {task}, Priority: {priority}, Energy: {task_energy_map[task]}, Time: {task_duration_map[task]}")

if __name__ == "__main__":
    main()
