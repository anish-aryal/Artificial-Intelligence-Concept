"""
UI Styles and Constants
Modern Minimal Design System
"""

# Modern Minimal Color Palette
class Colors:
    # Primary - Sophisticated Purple
    PRIMARY = '#6366f1'          
    PRIMARY_LIGHT = '#818cf8'    
    PRIMARY_DARK = '#4f46e5'     
    PRIMARY_SUBTLE = '#eef2ff'  
    
    # Accent Colors - Clean & Purposeful
    SUCCESS = '#10b981'          
    SUCCESS_LIGHT = '#34d399'    
    SUCCESS_SUBTLE = '#d1fae5'   
    
    WARNING = '#f59e0b'        
    WARNING_LIGHT = '#fbbf24'  
    WARNING_SUBTLE = '#fef3c7' 
    
    DANGER = '#ef4444'       
    DANGER_LIGHT = '#f87171' 
    DANGER_SUBTLE = '#fee2e2'
    
    INFO = '#3b82f6'             
    INFO_SUBTLE = '#dbeafe'      
    
    # Neutral Grays - Modern & Clean
    GRAY_50 = '#f9fafb'          
    GRAY_100 = '#f3f4f6'         
    GRAY_200 = '#e5e7eb'         
    GRAY_300 = '#d1d5db'         
    GRAY_400 = '#9ca3af'         
    GRAY_500 = '#6b7280'         
    GRAY_600 = '#4b5563'         
    GRAY_700 = '#374151'         
    GRAY_800 = '#1f2937'         
    GRAY_900 = '#111827'         
    
    # Semantic Colors
    BACKGROUND = GRAY_50       
    SURFACE = '#ffffff'        
    TEXT_PRIMARY = GRAY_900    
    TEXT_SECONDARY = GRAY_600  
    TEXT_MUTED = GRAY_500      
    BORDER = GRAY_200          
    DIVIDER = GRAY_100         


# Modern Typography - San Francisco / System Fonts
class Fonts:
    # Font Stacks (System fonts for native feel)
    PRIMARY = '-apple-system, BlinkMacSystemFont, "SF Pro Display", "Segoe UI", Arial, sans-serif'
    MONOSPACE = '"SF Mono", "Monaco", "Courier New", monospace'
    
    # Font Sizes (Tailwind-inspired scale)
    DISPLAY = 36      
    TITLE = 30        
    HEADING_1 = 24    
    HEADING_2 = 20    
    HEADING_3 = 18    
    BODY_LARGE = 16   
    BODY = 14         
    BODY_SMALL = 13   
    CAPTION = 12      
    TINY = 11         

    # Font Weights
    LIGHT = 'normal'
    REGULAR = 'normal'
    MEDIUM = 'normal'
    SEMIBOLD = 'bold'
    BOLD = 'bold'
    EXTRABOLD = 'bold'


# Spacing Scale (8px base - industry standard)
class Spacing:
    XXS = 4      # 0.25rem
    XS = 8       # 0.5rem
    SM = 12      # 0.75rem
    MD = 16      # 1rem
    LG = 24      # 1.5rem
    XL = 32      # 2rem
    XXL = 48     # 3rem
    XXXL = 64    # 4rem
    GIANT = 96   # 6rem


# Border Radius (Smooth, modern corners)
class BorderRadius:
    NONE = 0
    SM = 6      
    MD = 8      
    LG = 12     
    XL = 16     
    XXL = 24    
    FULL = 9999 


# Shadows (Subtle depth)
class Shadows:
    NONE = 'none'
    SM = '0 1px 2px 0 rgba(0, 0, 0, 0.05)'
    MD = '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)'
    LG = '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)'
    XL = '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)'
    INNER = 'inset 0 2px 4px 0 rgba(0, 0, 0, 0.06)'


# Component Sizes
class Sizes:
    # Window
    WINDOW_WIDTH = 1100
    WINDOW_HEIGHT = 750
    WINDOW_MIN_WIDTH = 900
    WINDOW_MIN_HEIGHT = 600
    
    # Layout
    HEADER_HEIGHT = 120
    SIDEBAR_WIDTH = 280
    
    # Buttons
    BUTTON_SM_HEIGHT = 32
    BUTTON_MD_HEIGHT = 40
    BUTTON_LG_HEIGHT = 48
    BUTTON_PADDING_X = 20
    
    # Inputs
    INPUT_HEIGHT = 44
    INPUT_PADDING = 12
    
    # Cards
    CARD_MIN_HEIGHT = 100
    CARD_PADDING = 20
    
    # Icons
    ICON_SM = 16
    ICON_MD = 20
    ICON_LG = 24


# Animations & Transitions
class Animation:
    FAST = 150      
    NORMAL = 250    
    SLOW = 350      
    
    # Easing
    EASE_IN = 'ease-in'
    EASE_OUT = 'ease-out'
    EASE_IN_OUT = 'ease-in-out'


# Z-Index Layers (Proper stacking)
class ZIndex:
    BASE = 0
    DROPDOWN = 1000
    STICKY = 1100
    OVERLAY = 1200
    MODAL = 1300
    POPOVER = 1400
    TOOLTIP = 1500