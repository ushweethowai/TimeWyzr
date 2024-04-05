class Priority:
    def get_priority(self, urgency, impact):
        urgency = urgency.upper()
        impact = impact.upper()
        if not self.is_valid(urgency) or not self.is_valid(impact):
            raise ValueError("Invalid level input. Levels must be LOW, MEDIUM, or HIGH.")
        if urgency == "HIGH" and impact == "HIGH":
            return "HIGH"
        elif urgency == "MEDIUM" and impact == "HIGH":
            return "HIGH"
        elif urgency == "HIGH" and impact == "MEDIUM":
            return "HIGH"
        elif urgency == "MEDIUM" and impact == "MEDIUM":
            return "MEDIUM"
        elif urgency == "HIGH" and impact == "LOW":
            return "MEDIUM"
        elif urgency == "LOW" and impact == "HIGH":
            return "MEDIUM"
        else:
            return "LOW"
    
    def is_valid(self, level):
        return level in ["MEDIUM", "LOW", "HIGH"]
