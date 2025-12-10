"""
Professional Icon System - Clean symbols only
"""

class Icons:
    """Professional icons"""
    
    # Symbols
    ARROW_RIGHT = "→"
    ARROW_LEFT = "←"
    CHECK = "✓"
    CROSS = "✕"
    STAR = "★"
    CIRCLE = "●"
    
    NONE = ""


class IconHelper:
    """Helper functions"""
    
    @staticmethod
    def get_difficulty_badge(level):
        """Get difficulty badge text and variant"""
        if level == 1:
            return ("Easy", "success")
        elif level == 2:
            return ("Medium", "warning")
        else:
            return ("Hard", "danger")
    
    @staticmethod
    def format_xp(xp):
        """Format XP display"""
        return f"{xp} XP"
    
    @staticmethod
    def format_level(level):
        """Format level display"""
        return f"Level {level}"


class UIText:
    """UI text labels"""
    
    # Headers
    DASHBOARD = "Dashboard"
    CONTINUE_LEARNING = "Continue Learning"
    QUICK_ACTIONS = "Quick Actions"
    
    # Actions
    START_LEARNING = "Start Learning"
    PRACTICE_NOW = "Practice Now"
    VIEW_PROGRESS = "View Progress"
    NEXT = "Next"
    PREVIOUS = "Previous"
    
    # Info
    TOPICS = "Topics"
    PROBLEMS = "Problems"