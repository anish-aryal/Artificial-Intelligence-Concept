"""
Reusable UI Components
Modern components using CustomTkinter
"""

import customtkinter as ctk
from .styles import Colors, Fonts, Sizes


class Button:
    """Modern button component"""
    
    @staticmethod
    def create(parent, text, command, style='primary', width=None):
        """Create a modern button"""
        width = width or Sizes.BUTTON_WIDTH
        
        styles = {
            'primary': {
                'fg_color': Colors.PRIMARY,
                'hover_color': Colors.PRIMARY_DARK,
                'text_color': 'white'
            },
            'success': {
                'fg_color': Colors.SUCCESS,
                'hover_color': Colors.SUCCESS_DARK,
                'text_color': 'white'
            },
            'danger': {
                'fg_color': Colors.DANGER,
                'hover_color': '#dc2626',
                'text_color': 'white'
            },
            'secondary': {
                'fg_color': '#f3f4f6',
                'hover_color': '#e5e7eb',
                'text_color': '#374151'
            },
            'outline': {
                'fg_color': 'transparent',
                'hover_color': Colors.PRIMARY_SUBTLE,
                'text_color': Colors.PRIMARY,
                'border_width': 2,
                'border_color': Colors.PRIMARY
            }
        }
        
        btn_style = styles.get(style, styles['primary'])
        
        button = ctk.CTkButton(
            parent,
            text=text,
            command=command,
            width=width,
            height=Sizes.BUTTON_HEIGHT,
            corner_radius=Sizes.CORNER_RADIUS,
            font=(Fonts.PRIMARY, 14, 'bold'),
            **btn_style
        )
        
        return button


class Card:
    """Modern card component"""
    
    @staticmethod
    def create(parent):
        """Create a card frame"""
        card = ctk.CTkFrame(
            parent,
            fg_color=Colors.SURFACE,
            corner_radius=12,
            border_width=1,
            border_color=Colors.BORDER
        )
        return card


class Label:
    """Label components with different styles"""
    
    @staticmethod
    def title(parent, text):
        """Large title"""
        return ctk.CTkLabel(
            parent,
            text=text,
            font=(Fonts.PRIMARY, Fonts.TITLE, 'bold'),
            text_color=Colors.TEXT_PRIMARY
        )
    
    @staticmethod
    def heading(parent, text):
        """Section heading"""
        return ctk.CTkLabel(
            parent,
            text=text,
            font=(Fonts.PRIMARY, Fonts.HEADING_1, 'bold'),
            text_color=Colors.TEXT_PRIMARY
        )
    
    @staticmethod
    def subheading(parent, text):
        """Subsection heading"""
        return ctk.CTkLabel(
            parent,
            text=text,
            font=(Fonts.PRIMARY, Fonts.BODY_LARGE, 'bold'),
            text_color=Colors.TEXT_SECONDARY
        )
    
    @staticmethod
    def body(parent, text):
        """Body text"""
        return ctk.CTkLabel(
            parent,
            text=text,
            font=(Fonts.PRIMARY, Fonts.BODY),
            text_color=Colors.TEXT_SECONDARY,
            wraplength=600,
            justify='left'
        )
    
    @staticmethod
    def muted(parent, text):
        """Muted text"""
        return ctk.CTkLabel(
            parent,
            text=text,
            font=(Fonts.PRIMARY, Fonts.BODY_SMALL),
            text_color=Colors.TEXT_MUTED
        )


class CodeBlock:
    """Code display component"""
    
    @staticmethod
    def create(parent, code, height=200, width=600):
        """Create code display"""
        textbox = ctk.CTkTextbox(
            parent,
            height=height,
            width=width,
            corner_radius=8,
            fg_color='#1e1e1e',
            text_color='#d4d4d4',
            font=(Fonts.MONOSPACE, 13)
        )
        textbox.insert('1.0', code)
        textbox.configure(state='disabled')
        return textbox


class InputBox:
    """Text input component"""
    
    @staticmethod
    def create(parent, height=150, width=500):
        """Create text input box"""
        textbox = ctk.CTkTextbox(
            parent,
            height=height,
            width=width,
            corner_radius=8,
            border_width=1,
            border_color=Colors.BORDER,
            font=(Fonts.MONOSPACE, 13)
        )
        return textbox


class Badge:
    """Small badge component"""
    
    @staticmethod
    def create(parent, text, bg_color=None, fg_color=None):
        """Create badge"""
        bg = bg_color or Colors.PRIMARY_SUBTLE
        fg = fg_color or Colors.PRIMARY
        
        badge = ctk.CTkLabel(
            parent,
            text=text,
            font=(Fonts.PRIMARY, Fonts.CAPTION, 'bold'),
            fg_color=bg,
            text_color=fg,
            corner_radius=6,
            padx=12,
            pady=6
        )
        return badge


class Divider:
    """Horizontal divider line"""
    
    @staticmethod
    def create(parent):
        """Create divider"""
        line = ctk.CTkFrame(
            parent,
            fg_color=Colors.BORDER,
            height=1
        )
        return line