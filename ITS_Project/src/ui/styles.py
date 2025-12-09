"""
UI Styles and Constants
Modern design using CustomTkinter
"""

import customtkinter as ctk

# Set global CustomTkinter theme
ctk.set_appearance_mode("light")  # "light" or "dark"
ctk.set_default_color_theme("blue")


class Colors:
    """Modern color palette"""
    
    # Primary colors
    PRIMARY = "#6366f1"
    PRIMARY_DARK = "#4f46e5"
    PRIMARY_SUBTLE = "#eef2ff"
    
    # Accent colors
    SUCCESS = "#10b981"
    SUCCESS_DARK = "#059669"
    SUCCESS_SUBTLE = "#d1fae5"
    
    WARNING = "#f59e0b"
    WARNING_SUBTLE = "#fef3c7"
    
    DANGER = "#ef4444"
    DANGER_SUBTLE = "#fee2e2"
    
    INFO = "#3b82f6"
    INFO_SUBTLE = "#dbeafe"
    
    # Neutral colors
    GRAY_50 = '#f9fafb'
    GRAY_100 = '#f3f4f6'
    GRAY_200 = '#e5e7eb'
    GRAY_500 = '#6b7280'
    GRAY_600 = '#4b5563'
    GRAY_900 = '#111827'
    
    # Semantic colors
    BACKGROUND = GRAY_50
    SURFACE = '#ffffff'
    TEXT_PRIMARY = GRAY_900
    TEXT_SECONDARY = GRAY_600
    TEXT_MUTED = GRAY_500
    BORDER = GRAY_200


class Fonts:
    """Font settings"""
    PRIMARY = 'Arial'
    MONOSPACE = 'Courier New'
    
    TITLE = 40
    HEADING_1 = 24
    HEADING_2 = 20
    BODY_LARGE = 16
    BODY = 14
    BODY_SMALL = 13
    CAPTION = 12


class Spacing:
    """Spacing scale"""
    XXS = 4
    XS = 8
    SM = 12
    MD = 16
    LG = 24
    XL = 32
    XXL = 48


class Sizes:
    """Component sizes"""
    WINDOW_WIDTH = 1100
    WINDOW_HEIGHT = 750
    WINDOW_MIN_WIDTH = 900
    WINDOW_MIN_HEIGHT = 600
    
    BUTTON_WIDTH = 200
    BUTTON_HEIGHT = 48
    
    CORNER_RADIUS = 10