class Priority:
    def get_priority(self, urgency, difficulty):
        urgency = urgency.upper()
        difficulty = difficulty.upper()
        if not self.is_valid(urgency) or not self.is_valid(difficulty):
            raise ValueError("Invalid level input. Levels must be LOW, MEDIUM, or HIGH.")
        if urgency == "HIGH" and difficulty == "HIGH":
            return "HIGH"
        elif urgency == "MEDIUM" and difficulty == "HIGH":
            return "HIGH"
        elif urgency == "HIGH" and difficulty == "MEDIUM":
            return "HIGH"
        elif urgency == "MEDIUM" and difficulty == "MEDIUM":
            return "MEDIUM"
        elif urgency == "HIGH" and difficulty == "LOW":
            return "MEDIUM"
        elif urgency == "LOW" and difficulty == "HIGH":
            return "MEDIUM"
        else:
            return "LOW"
    
    def is_valid(self, level):
        return level in ["MEDIUM", "LOW", "HIGH"]
