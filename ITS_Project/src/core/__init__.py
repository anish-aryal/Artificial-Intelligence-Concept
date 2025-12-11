def __init__(self, save_file='user_progress.json'):
    """Initialize gamification system"""
    self.save_file = save_file
    self.user_data = self.load_user_data()
    
    # Ensure solved_problems exists
    if 'solved_problems' not in self.user_data:
        self.user_data['solved_problems'] = []
        self.save_user_data()