"""
Gamification System - XP, Levels, Progress Tracking
Professional implementation without childish elements
"""


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
    
    def __init__(self):
        """Initialize gamification system"""
        self.current_xp = 0
        self.current_level = 1
        self.problems_solved = 0
        self.problems_attempted = 0
        self.concepts_completed = set()
        self.perfect_scores = 0
        self.hints_used = 0
        
    def add_xp(self, action):
        """Add XP for an action"""
        xp_gained = self.XP_VALUES.get(action, 0)
        old_level = self.current_level
        
        self.current_xp += xp_gained
        
        # Calculate new level
        new_level = self._calculate_level(self.current_xp)
        level_up = new_level > old_level
        
        if level_up:
            self.current_level = new_level
        
        return {
            'xp_gained': xp_gained,
            'new_total': self.current_xp,
            'level_up': level_up,
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
            'hints_used': self.hints_used
        }