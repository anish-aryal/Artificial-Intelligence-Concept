"""
Reusable UI Components
Building blocks for the interface - buttons, cards, labels, etc.
"""

import tkinter as tk
from tkinter import scrolledtext
from .styles import Colors, Fonts, Spacing, BorderRadius


class Button:
    """Modern button component"""
    
    @staticmethod
    def create(parent, text, command, style='primary', width=200):
        """
        Create a styled button using Frame + Label
        
        Args:
            parent: Parent widget
            text: Button text
            command: Function to call when clicked
            style: 'primary', 'success', 'danger', 'secondary', 'outline'
            width: Button width in pixels
        """
        # Define button styles
        styles = {
            'primary': {
                'bg': '#6366f1',
                'fg': 'white',
                'hover_bg': '#4f46e5',
                'border_color': '#6366f1',
                'border_width': 0
            },
            'success': {
                'bg': '#10b981',
                'fg': 'white',
                'hover_bg': '#059669',
                'border_color': '#10b981',
                'border_width': 0
            },
            'danger': {
                'bg': '#ef4444',
                'fg': 'white',
                'hover_bg': '#dc2626',
                'border_color': '#ef4444',
                'border_width': 0
            },
            'secondary': {
                'bg': '#6b7280',
                'fg': 'white',
                'hover_bg': '#4b5563',
                'border_color': '#6b7280',
                'border_width': 0
            },
            'outline': {
                'bg': 'white',
                'fg': '#6366f1',
                'hover_bg': '#eef2ff',
                'border_color': '#6366f1',
                'border_width': 2
            }
        }
        
        btn_style = styles.get(style, styles['primary'])
        
        # Create frame with border
        btn_frame = tk.Frame(
            parent,
            bg=btn_style['bg'],
            cursor='hand2',
            width=width,
            height=44,
            highlightbackground=btn_style['border_color'],
            highlightthickness=btn_style['border_width'],
            highlightcolor=btn_style['border_color']
        )
        btn_frame.pack_propagate(False)
        
        # Create label inside
        btn_label = tk.Label(
            btn_frame,
            text=text,
            font=('Arial', 13, 'bold'),
            bg=btn_style['bg'],
            fg=btn_style['fg'],
            cursor='hand2'
        )
        btn_label.place(relx=0.5, rely=0.5, anchor='center')
        
        # Click handlers
        def on_click(e):
            command()
        
        def on_enter(e):
            btn_frame.config(bg=btn_style['hover_bg'])
            btn_label.config(bg=btn_style['hover_bg'])
        
        def on_leave(e):
            btn_frame.config(bg=btn_style['bg'])
            btn_label.config(bg=btn_style['bg'])
        
        # Bind events
        btn_frame.bind('<Button-1>', on_click)
        btn_label.bind('<Button-1>', on_click)
        btn_frame.bind('<Enter>', on_enter)
        btn_label.bind('<Enter>', on_enter)
        btn_frame.bind('<Leave>', on_leave)
        btn_label.bind('<Leave>', on_leave)
        
        return btn_frame


class Card:
    """Card component for displaying content"""
    
    @staticmethod
    def create(parent, bg=Colors.SURFACE):
        """Create a card frame"""
        card = tk.Frame(
            parent,
            bg=bg,
            relief='solid',
            bd=1,
            highlightbackground=Colors.BORDER,
            highlightthickness=1
        )
        return card


class Label:
    """Label components with different styles"""
    
    @staticmethod
    def title(parent, text, bg=Colors.SURFACE):
        """Large title label"""
        return tk.Label(
            parent,
            text=text,
            font=('Arial', Fonts.TITLE, 'bold'),
            bg=bg,
            fg=Colors.TEXT_PRIMARY
        )
    
    @staticmethod
    def heading(parent, text, bg=Colors.SURFACE):
        """Section heading"""
        return tk.Label(
            parent,
            text=text,
            font=('Arial', Fonts.HEADING_1, 'bold'),
            bg=bg,
            fg=Colors.TEXT_PRIMARY
        )
    
    @staticmethod
    def subheading(parent, text, bg=Colors.SURFACE):
        """Subsection heading"""
        return tk.Label(
            parent,
            text=text,
            font=('Arial', Fonts.BODY_LARGE, 'bold'),
            bg=bg,
            fg=Colors.TEXT_SECONDARY
        )
    
    @staticmethod
    def body(parent, text, bg=Colors.SURFACE):
        """Body text"""
        return tk.Label(
            parent,
            text=text,
            font=('Arial', Fonts.BODY),
            bg=bg,
            fg=Colors.TEXT_SECONDARY,
            wraplength=600,
            justify='left'
        )
    
    @staticmethod
    def muted(parent, text, bg=Colors.SURFACE):
        """Muted/secondary text"""
        return tk.Label(
            parent,
            text=text,
            font=('Arial', Fonts.BODY_SMALL),
            bg=bg,
            fg=Colors.TEXT_MUTED
        )


class CodeBlock:
    """Code display component"""
    
    @staticmethod
    def create(parent, code_text, height=10):
        """Create a code display area"""
        # Container with dark background
        container = tk.Frame(
            parent,
            bg=Colors.GRAY_900,
            relief='flat',
            bd=0
        )
        
        # Scrolled text widget
        code_display = scrolledtext.ScrolledText(
            container,
            font=('Courier New', Fonts.BODY_SMALL),
            bg=Colors.GRAY_900,
            fg=Colors.GRAY_100,
            height=height,
            width=60,
            relief='flat',
            bd=0,
            padx=Spacing.MD,
            pady=Spacing.MD,
            wrap='word'
        )
        code_display.pack(fill='both', expand=True)
        
        # Insert code
        code_display.insert('1.0', code_text)
        code_display.config(state='disabled')
        
        return container


class InputBox:
    """Text input component"""
    
    @staticmethod
    def create(parent, height=5, width=60):
        """Create a text input box"""
        # Container
        container = tk.Frame(
            parent,
            bg=Colors.SURFACE,
            relief='solid',
            bd=1,
            highlightbackground=Colors.BORDER,
            highlightthickness=1
        )
        
        # Text widget
        text_box = scrolledtext.ScrolledText(
            container,
            font=('Courier New', Fonts.BODY),
            bg=Colors.SURFACE,
            fg=Colors.TEXT_PRIMARY,
            height=height,
            width=width,
            relief='flat',
            bd=0,
            padx=Spacing.MD,
            pady=Spacing.MD,
            wrap='word',
            insertbackground=Colors.PRIMARY
        )
        text_box.pack(fill='both', expand=True, padx=2, pady=2)
        
        return container, text_box


class Badge:
    """Small badge for difficulty levels, status, etc."""
    
    @staticmethod
    def create(parent, text, bg_color=Colors.PRIMARY_SUBTLE, fg_color=Colors.PRIMARY):
        """Create a small badge"""
        badge = tk.Label(
            parent,
            text=text,
            font=('Arial', Fonts.CAPTION, 'bold'),
            bg=bg_color,
            fg=fg_color,
            padx=Spacing.SM,
            pady=Spacing.XXS
        )
        return badge


class Divider:
    """Horizontal divider line"""
    
    @staticmethod
    def create(parent):
        """Create a horizontal divider"""
        line = tk.Frame(
            parent,
            bg=Colors.DIVIDER,
            height=1
        )
        return line