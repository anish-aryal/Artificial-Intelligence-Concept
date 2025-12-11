"""
Modern UI Styles - Professional Design System
"""

import customtkinter as ctk

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class Colors:
    """Modern color system"""
    
    # Primary
    PRIMARY = "#6366f1"
    PRIMARY_DARK = "#4f46e5"
    PRIMARY_LIGHT = "#818cf8"
    PRIMARY_SUBTLE = "#eef2ff"
    
    # Semantic
    SUCCESS = "#10b981"
    SUCCESS_DARK = "#059669"
    SUCCESS_LIGHT = "#34d399"
    SUCCESS_SUBTLE = "#d1fae5"
    
    WARNING = "#f59e0b"
    WARNING_SUBTLE = "#fef3c7"
    
    DANGER = "#ef4444"
    DANGER_SUBTLE = "#fee2e2"
    
    INFO = "#3b82f6"
    INFO_SUBTLE = "#dbeafe"
    
    # Neutrals
    GRAY_50 = '#fafafa'
    GRAY_100 = '#f4f4f5'
    GRAY_200 = '#e4e4e7'
    GRAY_300 = '#d4d4d8'
    GRAY_400 = '#a1a1aa'
    GRAY_500 = '#71717a'
    GRAY_600 = '#52525b'
    GRAY_700 = '#3f3f46'
    GRAY_800 = '#27272a'
    GRAY_900 = '#18181b'
    
    # UI Elements
    BACKGROUND = GRAY_50
    SURFACE = '#ffffff'
    SURFACE_HOVER = GRAY_100
    BORDER = GRAY_200
    BORDER_FOCUS = PRIMARY
    
    # Text
    TEXT_PRIMARY = GRAY_900
    TEXT_SECONDARY = GRAY_600
    TEXT_MUTED = GRAY_500
    TEXT_INVERSE = '#ffffff'
    
    # Code
    CODE_BG = '#1e1e1e'
    CODE_TEXT = '#d4d4d4'
    WHITE = '#ffffff'


class Typography:
    """Typography scale"""
    
    PRIMARY = 'Arial'
    FALLBACK = 'Arial'
    MONO = 'Courier New'
    MONO_FALLBACK = 'Courier New'
    
    DISPLAY = 48
    H1 = 36
    H2 = 30
    H3 = 24
    H4 = 20
    H5 = 18
    BODY_LARGE = 16
    BODY = 14
    BODY_SMALL = 13
    CAPTION = 12
    TINY = 11


class Spacing:
    """Spacing scale"""
    XXS = 2      # ← ADDED
    XS = 4
    SM = 8
    MD = 12
    BASE = 16
    LG = 20
    XL = 24
    XXL = 32
    XXXL = 48
    GIANT = 64


class Layout:
    """Layout dimensions"""
    
    WINDOW_WIDTH = 1400
    WINDOW_HEIGHT = 900
    WINDOW_MIN_WIDTH = 1200
    WINDOW_MIN_HEIGHT = 700
    
    NAVBAR_HEIGHT = 64
    
    BUTTON_HEIGHT_SM = 36
    BUTTON_HEIGHT_MD = 44
    BUTTON_HEIGHT_LG = 52
    
    CARD_PADDING = 24


class Effects:
    """Visual effects"""
    
    RADIUS_SM = 6
    RADIUS_MD = 8
    RADIUS_LG = 12
    RADIUS_XL = 16
    RADIUS_FULL = 9999