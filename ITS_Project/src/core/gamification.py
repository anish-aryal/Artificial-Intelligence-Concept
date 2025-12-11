import json
import os
from datetime import datetime


class GamificationSystem:
    """Manages user progress, XP, and levels"""
    
    # XP values for different actions
    XP_VALUES = {
        'concept_viewed': 25,
        'problem_attempted': 50,
        'problem_solved': 100,
        'perfect_score': 150,
        'hint_used': -10,
        'solution_viewed': -25
    }
    
    # XP required for each level
    LEVEL_REQUIREMENTS = {
        1: 0,
        2: 500,
        3: 1200,
        4: 2100,
        5: 3200,
        6: 4500,
        7: 6000,
        8: 7800,
        9: 9900,
        10: 12500
    }
    
    def __init__(self, save_file='user_progress.json'):
        """Initialize gamification system"""
        self.save_file = save_file
        self.user_data = self.load_user_data()
        
        # Load data from file
        self.current_xp = self.user_data.get('xp', 0)
        self.current_level = self.user_data.get('level', 1)
        self.problems_solved = self.user_data.get('problems_solved', 0)
        self.problems_attempted = self.user_data.get('problems_attempted', 0)
        self.concepts_completed = set(self.user_data.get('concepts_completed', []))
        self.perfect_scores = self.user_data.get('perfect_scores', 0)
        self.hints_used = self.user_data.get('hints_used', 0)
        self.solved_problems = self.user_data.get('solved_problems', [])
    
    def load_user_data(self):
        """Load user progress from file"""
        if os.path.exists(self.save_file):
            try:
                with open(self.save_file, 'r') as f:
                    data = json.load(f)
                    
                    # Ensure solved_problems exists
                    if 'solved_problems' not in data:
                        data['solved_problems'] = []
                    
                    return data
            except Exception as e:
                print(f"Error loading user data: {e}")
        
        # Default user data
        return {
            'level': 1,
            'xp': 0,
            'problems_solved': 0,
            'problems_attempted': 0,
            'concepts_completed': [],
            'perfect_scores': 0,
            'hints_used': 0,
            'solved_problems': [],
            'created_at': datetime.now().isoformat(),
            'last_updated': datetime.now().isoformat()
        }
    
    def save_user_data(self):
        """Save user progress to file"""
        self.user_data = {
            'level': self.current_level,
            'xp': self.current_xp,
            'problems_solved': self.problems_solved,
            'problems_attempted': self.problems_attempted,
            'concepts_completed': list(self.concepts_completed),
            'perfect_scores': self.perfect_scores,
            'hints_used': self.hints_used,
            'solved_problems': self.solved_problems,
            'created_at': self.user_data.get('created_at', datetime.now().isoformat()),
            'last_updated': datetime.now().isoformat()
        }
        
        try:
            with open(self.save_file, 'w') as f:
                json.dump(self.user_data, f, indent=2)
        except Exception as e:
            print(f"Error saving user data: {e}")
    
    def add_xp(self, action):
        """Add XP for an action"""
        xp_gained = self.XP_VALUES.get(action, 0)
        old_level = self.current_level
        
        self.current_xp += xp_gained
        
        # Don't go below 0 XP
        if self.current_xp < 0:
            self.current_xp = 0
        
        # Calculate new level
        new_level = self._calculate_level(self.current_xp)
        level_up = new_level > old_level
        
        if level_up:
            self.current_level = new_level
        
        self.save_user_data()
        
        return {
            'xp_gained': xp_gained,
            'new_total': self.current_xp,
            'level_up': level_up,
            'leveled_up_from': old_level,  # Added for popup
            'new_level': new_level
        }
    
    def _calculate_level(self, xp):
        """Calculate level based on total XP"""
        level = 1
        for lvl in sorted(self.LEVEL_REQUIREMENTS.keys(), reverse=True):
            if xp >= self.LEVEL_REQUIREMENTS[lvl]:
                level = lvl
                break
        return level
    
    def get_xp_for_next_level(self):
        """Get XP required for next level"""
        next_level = self.current_level + 1
        if next_level in self.LEVEL_REQUIREMENTS:
            return self.LEVEL_REQUIREMENTS[next_level]
        return None
    
    def get_xp_progress(self):
        """Get progress towards next level"""
        current_level_xp = self.LEVEL_REQUIREMENTS[self.current_level]
        next_level_xp = self.get_xp_for_next_level()
        
        if next_level_xp is None:
            return {
                'current_xp_in_level': 0,
                'xp_for_next': 0,
                'percentage': 100
            }
        
        xp_in_current_level = self.current_xp - current_level_xp
        xp_needed = next_level_xp - current_level_xp
        percentage = (xp_in_current_level / xp_needed) * 100
        
        return {
            'current_xp_in_level': xp_in_current_level,
            'xp_for_next': xp_needed,
            'percentage': percentage
        }
    
    def record_problem_attempt(self, problem_name, score, perfect=False):
        """
        Record a problem attempt and award XP
        
        Args:
            problem_name: Name of the problem
            score: Score percentage (0-100)
            perfect: Whether all tests passed (100% score)
            
        Returns:
            dict with XP gained and level up info
        """
        self.problems_attempted += 1
        
        result = {
            'xp_gained': 0,
            'leveled_up': False,
            'leveled_up_from': self.current_level,  # Track old level
            'new_level': self.current_level
        }
        
        # Award XP based on performance
        if score >= 70:  # Passing score
            if perfect:
                xp_result = self.add_xp('perfect_score')
                result['xp_gained'] = xp_result['xp_gained']
                result['leveled_up'] = xp_result['level_up']
                result['leveled_up_from'] = xp_result['leveled_up_from']
                result['new_level'] = xp_result['new_level']
                
                self.perfect_scores += 1
                
                # Mark as solved
                if problem_name not in self.solved_problems:
                    self.solved_problems.append(problem_name)
                    self.problems_solved = len(self.solved_problems)
            else:
                xp_result = self.add_xp('problem_solved')
                result['xp_gained'] = xp_result['xp_gained']
                result['leveled_up'] = xp_result['level_up']
                result['leveled_up_from'] = xp_result['leveled_up_from']
                result['new_level'] = xp_result['new_level']
                
                # Still mark as solved even if not perfect
                if problem_name not in self.solved_problems:
                    self.solved_problems.append(problem_name)
                    self.problems_solved = len(self.solved_problems)
        else:
            # Still attempted, but no XP
            xp_result = self.add_xp('problem_attempted')
            result['xp_gained'] = xp_result['xp_gained']
        
        self.save_user_data()
        
        return result
    
    def record_hint_used(self):
        """Record when user uses a hint"""
        self.hints_used += 1
        result = self.add_xp('hint_used')
        self.save_user_data()
        return result
    
    def record_solution_viewed(self):
        """Record when user views solution"""
        result = self.add_xp('solution_viewed')
        self.save_user_data()
        return result
    
    def mark_concept_completed(self, concept_name):
        """Mark a concept as completed"""
        if concept_name not in self.concepts_completed:
            self.concepts_completed.add(concept_name)
            result = self.add_xp('concept_viewed')
            self.save_user_data()
            return result
        return {'xp_gained': 0, 'new_total': self.current_xp, 'level_up': False, 'new_level': self.current_level}
    
    def get_stats(self):
        """Get all user statistics"""
        return {
            'level': self.current_level,
            'xp': self.current_xp,
            'xp_for_next': self.get_xp_for_next_level() or self.current_xp,
            'problems_solved': self.problems_solved,
            'problems_attempted': self.problems_attempted,
            'success_rate': (self.problems_solved / self.problems_attempted * 100) if self.problems_attempted > 0 else 0,
            'perfect_scores': self.perfect_scores,
            'concepts_completed': len(self.concepts_completed),
            'hints_used': self.hints_used,
            'solved_problems': self.solved_problems
        }
    
    def reset_progress(self):
        """Reset all user progress"""
        self.current_xp = 0
        self.current_level = 1
        self.problems_solved = 0
        self.problems_attempted = 0
        self.concepts_completed = set()
        self.perfect_scores = 0
        self.hints_used = 0
        self.solved_problems = []
        self.save_user_data()