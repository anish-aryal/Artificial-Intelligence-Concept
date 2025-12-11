"""
Learn Screen - Concept explanation with examples
"""

import customtkinter as ctk
from src.ui.components import Button, Card, Badge, ProgressBar, CodeDisplay, Alert
from src.ui.styles import Colors, Typography, Spacing
from src.ui.icons import Icons


class LearnScreen:
    """Modern Learn Screen with Sticky Header"""
    
    @staticmethod
    def create(parent, manager, current_index=0, on_back=None, on_practice=None):
        """Create learning screen"""
        for widget in parent.winfo_children():
            widget.destroy()
        
        concepts = manager.get_concepts()
        
        if not concepts or current_index >= len(concepts):
            Alert.create(parent, "No concepts available", variant='warning').pack(pady=50)
            return
        
        concept = concepts[current_index]
        details = manager.get_concept_details(concept)
        
        header_container = ctk.CTkFrame(parent, fg_color=Colors.BACKGROUND)
        header_container.pack(fill='x', side='top', padx=Spacing.GIANT, pady=(Spacing.XXL, 0))
        
        if on_back:
            back_row = ctk.CTkFrame(header_container, fg_color='transparent')
            back_row.pack(fill='x', pady=(0, Spacing.BASE))
            
            Button.create(
                back_row,
                f"{Icons.ARROW_LEFT} Back to Dashboard",
                on_back,
                variant='ghost',
                size='md',
                width=180
            ).pack(side='left')
        
        progress_text = f"Topic {current_index + 1} of {len(concepts)}"
        progress_label = ctk.CTkLabel(
            header_container,
            text=progress_text,
            font=(Typography.FALLBACK, Typography.BODY),
            text_color=Colors.TEXT_MUTED
        )
        progress_label.pack(anchor='w', pady=(0, Spacing.SM))
        
        _, prog_bar = ProgressBar.create(header_container, current_index + 1, len(concepts), show_label=False)
        prog_bar.master.pack(fill='x', pady=(0, Spacing.BASE))
        
        title = ctk.CTkLabel(
            header_container,
            text=details['name'],
            font=(Typography.FALLBACK, Typography.H1, 'bold'),
            text_color=Colors.TEXT_PRIMARY
        )
        title.pack(anchor='w', pady=(0, Spacing.BASE))
        
        badge_row = ctk.CTkFrame(header_container, fg_color='transparent')
        badge_row.pack(anchor='w', pady=(0, Spacing.BASE))
        
        if details.get('iterable'):
            Badge.create(
                badge_row,
                details['iterable']['name'],
                variant='primary'
            ).pack(side='left', padx=(0, Spacing.SM))
        
        if details.get('method'):
            Badge.create(
                badge_row,
                details['method']['name'],
                variant='success'
            ).pack(side='left')
        
        divider = ctk.CTkFrame(header_container, fg_color=Colors.BORDER, height=1)
        divider.pack(fill='x', pady=(Spacing.BASE, 0))
        
        scroll = ctk.CTkScrollableFrame(parent, fg_color=Colors.BACKGROUND)
        scroll.pack(fill='both', expand=True, side='top', padx=Spacing.GIANT, pady=(Spacing.BASE, Spacing.XXL))
        
        explain_card = Card.create(scroll)
        explain_card.pack(fill='x', pady=(0, Spacing.XXL))
        
        explain_header = ctk.CTkLabel(
            explain_card,
            text="What You'll Learn",
            font=(Typography.FALLBACK, Typography.H3, 'bold'),
            text_color=Colors.TEXT_PRIMARY
        )
        explain_header.pack(anchor='w', padx=Spacing.LG, pady=(Spacing.LG, Spacing.BASE))
        
        explain_text = ctk.CTkLabel(
            explain_card,
            text=details['explanation'],
            font=(Typography.FALLBACK, Typography.BODY_LARGE),
            text_color=Colors.TEXT_SECONDARY,
            wraplength=900,
            justify='left'
        )
        explain_text.pack(anchor='w', padx=Spacing.LG, pady=(0, Spacing.LG))
        
        syntax_card = Card.create(scroll)
        syntax_card.pack(fill='x', pady=(0, Spacing.XXL))
        
        syntax_header = ctk.CTkLabel(
            syntax_card,
            text="Syntax Pattern",
            font=(Typography.FALLBACK, Typography.H3, 'bold'),
            text_color=Colors.TEXT_PRIMARY
        )
        syntax_header.pack(anchor='w', padx=Spacing.LG, pady=(Spacing.LG, Spacing.BASE))
        
        syntax_desc = ctk.CTkLabel(
            syntax_card,
            text="This is the pattern you'll use:",
            font=(Typography.FALLBACK, Typography.BODY),
            text_color=Colors.TEXT_MUTED
        )
        syntax_desc.pack(anchor='w', padx=Spacing.LG, pady=(0, Spacing.MD))
        
        CodeDisplay.create(
            syntax_card,
            details['syntax'],
            height=80,
            width=800
        ).pack(padx=Spacing.LG, pady=(0, Spacing.LG))
        
        code_card = Card.create(scroll)
        code_card.pack(fill='x', pady=(0, Spacing.XXL))
        
        code_header = ctk.CTkLabel(
            code_card,
            text="Complete Example",
            font=(Typography.FALLBACK, Typography.H3, 'bold'),
            text_color=Colors.TEXT_PRIMARY
        )
        code_header.pack(anchor='w', padx=Spacing.LG, pady=(Spacing.LG, Spacing.BASE))
        
        code_desc = ctk.CTkLabel(
            code_card,
            text="Here's a working example:",
            font=(Typography.FALLBACK, Typography.BODY),
            text_color=Colors.TEXT_MUTED
        )
        code_desc.pack(anchor='w', padx=Spacing.LG, pady=(0, Spacing.MD))
        
        CodeDisplay.create(
            code_card,
            details['code'],
            height=250,
            width=800
        ).pack(padx=Spacing.LG, pady=(0, Spacing.LG))
        
        nav_card = Card.create(scroll)
        nav_card.pack(fill='x')
        
        nav_frame = ctk.CTkFrame(nav_card, fg_color='transparent')
        nav_frame.pack(fill='x', padx=Spacing.LG, pady=Spacing.LG)
        
        left_nav = ctk.CTkFrame(nav_frame, fg_color='transparent')
        left_nav.pack(side='left')
        
        if current_index > 0:
            Button.create(
                left_nav,
                f"{Icons.ARROW_LEFT} Previous",
                lambda: LearnScreen.create(parent, manager, current_index - 1, on_back, on_practice),
                variant='secondary',
                size='md',
                width=150
            ).pack(side='left')
        
        center_nav = ctk.CTkFrame(nav_frame, fg_color='transparent')
        center_nav.pack(side='left', expand=True)
        
        if on_practice:
            Button.create(
                center_nav,
                "Start Practicing",
                on_practice,
                variant='success',
                size='md',
                width=180
            ).pack()
        
        right_nav = ctk.CTkFrame(nav_frame, fg_color='transparent')
        right_nav.pack(side='right')
        
        if current_index < len(concepts) - 1:
            Button.create(
                right_nav,
                f"Next {Icons.ARROW_RIGHT}",
                lambda: LearnScreen.create(parent, manager, current_index + 1, on_back, on_practice),
                variant='primary',
                size='md',
                width=150
            ).pack(side='left')