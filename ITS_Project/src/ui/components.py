"""
Modern UI Components
"""

import customtkinter as ctk
from src.ui.styles import Colors, Typography, Spacing, Layout, Effects


class Button:
    """Modern button component"""
    
    @staticmethod
    def create(parent, text, command, variant='primary', size='md', width=None):
        """Create button"""
        
        sizes = {
            'sm': {'height': Layout.BUTTON_HEIGHT_SM, 'font_size': 13, 'width': 120},
            'md': {'height': Layout.BUTTON_HEIGHT_MD, 'font_size': 14, 'width': 160},
            'lg': {'height': Layout.BUTTON_HEIGHT_LG, 'font_size': 16, 'width': 200}
        }
        
        size_config = sizes.get(size, sizes['md'])
        button_width = width or size_config['width']
        
        variants = {
            'primary': {
                'fg_color': Colors.PRIMARY,
                'hover_color': Colors.PRIMARY_DARK,
                'text_color': Colors.TEXT_INVERSE,
                'border_width': 0
            },
            'secondary': {
                'fg_color': Colors.GRAY_200,
                'hover_color': Colors.GRAY_300,
                'text_color': Colors.TEXT_PRIMARY,
                'border_width': 0
            },
            'success': {
                'fg_color': Colors.SUCCESS,
                'hover_color': Colors.SUCCESS_DARK,
                'text_color': Colors.TEXT_INVERSE,
                'border_width': 0
            },
            'ghost': {
                'fg_color': 'transparent',
                'hover_color': Colors.GRAY_100,
                'text_color': Colors.TEXT_PRIMARY,
                'border_width': 0
            }
        }
        
        style = variants.get(variant, variants['primary'])
        
        button = ctk.CTkButton(
            parent,
            text=text,
            command=command,
            width=button_width,
            height=size_config['height'],
            corner_radius=Effects.RADIUS_MD,
            font=(Typography.FALLBACK, size_config['font_size'], 'bold'),
            **style
        )
        
        return button


class Card:
    """Card container"""
    
    @staticmethod
    def create(parent, padding=Layout.CARD_PADDING, hover=False):
        """Create card"""
        
        card = ctk.CTkFrame(
            parent,
            fg_color=Colors.SURFACE,
            corner_radius=Effects.RADIUS_LG,
            border_width=1,
            border_color=Colors.BORDER
        )
        
        if hover:
            def on_enter(e):
                card.configure(border_color=Colors.PRIMARY_LIGHT)
            
            def on_leave(e):
                card.configure(border_color=Colors.BORDER)
            
            card.bind('<Enter>', on_enter)
            card.bind('<Leave>', on_leave)
        
        return card


class Badge:
    """Small badge"""
    
    @staticmethod
    def create(parent, text, variant='default'):
        """Create badge"""
        
        variants = {
            'default': (Colors.GRAY_200, Colors.TEXT_SECONDARY),
            'primary': (Colors.PRIMARY_SUBTLE, Colors.PRIMARY),
            'success': (Colors.SUCCESS_SUBTLE, Colors.SUCCESS),
            'warning': (Colors.WARNING_SUBTLE, Colors.WARNING),
            'danger': (Colors.DANGER_SUBTLE, Colors.DANGER),
            'info': (Colors.INFO_SUBTLE, Colors.INFO)
        }
        
        bg, fg = variants.get(variant, variants['default'])
        
        badge = ctk.CTkLabel(
            parent,
            text=text,
            font=(Typography.FALLBACK, Typography.CAPTION, 'bold'),
            fg_color=bg,
            text_color=fg,
            corner_radius=Effects.RADIUS_SM,
            padx=Spacing.MD,
            pady=Spacing.XS
        )
        
        return badge


class ProgressBar:
    """Progress bar"""
    
    @staticmethod
    def create(parent, value=0, max_value=100, show_label=True):
        """Create progress bar"""
        
        container = ctk.CTkFrame(parent, fg_color='transparent')
        
        progress = ctk.CTkProgressBar(
            container,
            height=12,
            corner_radius=Effects.RADIUS_FULL,
            fg_color=Colors.GRAY_200,
            progress_color=Colors.SUCCESS
        )
        progress.pack(fill='x', pady=(0, Spacing.XS) if show_label else 0)
        progress.set(value / max_value)
        
        if show_label:
            percentage = int((value / max_value) * 100)
            label = ctk.CTkLabel(
                container,
                text=f"{value}/{max_value} ({percentage}%)",
                font=(Typography.FALLBACK, Typography.CAPTION),
                text_color=Colors.TEXT_MUTED
            )
            label.pack()
        
        return container, progress


class CodeDisplay:
    """Read-only code display"""
    
    @staticmethod
    def create(parent, code, height=200, width=600):
        """Create code display"""
        
        display = ctk.CTkTextbox(
            parent,
            height=height,
            width=width,
            corner_radius=Effects.RADIUS_MD,
            fg_color=Colors.CODE_BG,
            text_color=Colors.CODE_TEXT,
            font=(Typography.MONO_FALLBACK, 13),
            border_width=0
        )
        
        display.insert('1.0', code)
        display.configure(state='disabled')
        
        return display


class Alert:
    """Alert component"""
    
    @staticmethod
    def create(parent, message, variant='info'):
        """Create alert"""
        
        variants = {
            'info': (Colors.INFO_SUBTLE, Colors.INFO),
            'success': (Colors.SUCCESS_SUBTLE, Colors.SUCCESS),
            'warning': (Colors.WARNING_SUBTLE, Colors.WARNING),
            'danger': (Colors.DANGER_SUBTLE, Colors.DANGER)
        }
        
        bg, fg = variants.get(variant, variants['info'])
        
        alert = ctk.CTkFrame(
            parent,
            fg_color=bg,
            corner_radius=Effects.RADIUS_MD
        )
        
        label = ctk.CTkLabel(
            alert,
            text=message,
            font=(Typography.FALLBACK, Typography.BODY),
            text_color=fg
        )
        label.pack(padx=Spacing.BASE, pady=Spacing.MD)
        
        return alert


class LevelIndicator:
    """Level indicator with progress"""
    
    @staticmethod
    def create(parent, level, current_xp, xp_for_next):
        """Create level indicator"""
        
        container = ctk.CTkFrame(parent, fg_color='transparent')
        
        # Level badge
        level_badge = ctk.CTkFrame(
            container,
            fg_color='#8b5cf6',
            corner_radius=Effects.RADIUS_MD,
            width=60,
            height=60
        )
        level_badge.pack_propagate(False)
        level_badge.pack(side='left', padx=(0, Spacing.MD))
        
        level_label = ctk.CTkLabel(
            level_badge,
            text=f"L{level}",
            font=(Typography.FALLBACK, Typography.H4, 'bold'),
            text_color='white'
        )
        level_label.place(relx=0.5, rely=0.5, anchor='center')
        
        # Progress info
        info_frame = ctk.CTkFrame(container, fg_color='transparent')
        info_frame.pack(side='left', fill='x', expand=True)
        
        progress_label = ctk.CTkLabel(
            info_frame,
            text=f"{current_xp} / {xp_for_next} XP to Level {level + 1}",
            font=(Typography.FALLBACK, Typography.BODY_SMALL),
            text_color=Colors.TEXT_SECONDARY
        )
        progress_label.pack(anchor='w')
        
        progress_bar = ctk.CTkProgressBar(
            info_frame,
            height=8,
            corner_radius=Effects.RADIUS_FULL,
            fg_color=Colors.GRAY_200,
            progress_color='#8b5cf6'
        )
        progress_bar.pack(fill='x', pady=(Spacing.XS, 0))
        progress_bar.set(current_xp / xp_for_next if xp_for_next > 0 else 0)
        
        return container


class Divider:
    """Horizontal divider"""
    
    @staticmethod
    def create(parent):
        """Create divider"""
        line = ctk.CTkFrame(parent, fg_color=Colors.BORDER, height=1)
        return line