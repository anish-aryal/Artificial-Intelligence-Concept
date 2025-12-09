"""
Screen Modules
Different screens using CustomTkinter for modern UI
"""

import customtkinter as ctk
from .components import Button, Card, Label, CodeBlock, InputBox, Badge, Divider
from .styles import Colors


class WelcomeScreen:
    """Modern welcome screen"""
    
    @staticmethod
    def create(parent, manager, on_learn, on_practice):
        """Create welcome screen"""
        # Clear parent
        for widget in parent.winfo_children():
            widget.destroy()
        
        # Scrollable container
        scroll = ctk.CTkScrollableFrame(
            parent,
            fg_color=Colors.BACKGROUND
        )
        scroll.pack(fill='both', expand=True, padx=50, pady=40)
        
        # Hero section
        hero = ctk.CTkFrame(scroll, fg_color='transparent')
        hero.pack(fill='x', pady=(0, 40))
        
        # Title
        title = Label.title(hero, "Master Python Iteration")
        title.pack(pady=(0, 12))
        
        # Subtitle
        subtitle = Label.body(hero, "Interactive learning system powered by ontology")
        subtitle.pack()
        
        # Stats section
        stats_frame = ctk.CTkFrame(scroll, fg_color='transparent')
        stats_frame.pack(fill='x', pady=(0, 40))
        
        stats = manager.get_statistics()
        stat_data = [
            (stats['concepts'], "Concepts", Colors.PRIMARY),
            (stats['problems'], "Problems", Colors.SUCCESS),
            (stats['test_cases'], "Test Cases", Colors.INFO)
        ]
        
        for value, label, color in stat_data:
            # Stat card
            card = Card.create(stats_frame)
            card.pack(side='left', padx=10, expand=True, fill='both')
            
            # Number
            num = ctk.CTkLabel(
                card,
                text=str(value),
                font=('Arial', 48, 'bold'),
                text_color=color
            )
            num.pack(pady=(20, 5))
            
            # Label
            lbl = Label.muted(card, label)
            lbl.pack(pady=(0, 20))
        
        # Buttons
        btn_frame = ctk.CTkFrame(scroll, fg_color='transparent')
        btn_frame.pack()
        
        learn_btn = Button.create(
            btn_frame,
            "Start Learning →",
            on_learn,
            style='primary'
        )
        learn_btn.pack(side='left', padx=10)
        
        practice_btn = Button.create(
            btn_frame,
            "Practice Problems",
            on_practice,
            style='success'
        )
        practice_btn.pack(side='left', padx=10)


class LearnScreen:
    """Modern learning screen"""
    
    @staticmethod
    def create(parent, manager, current_concept_index=0):
        """Create learn screen"""
        # Clear parent
        for widget in parent.winfo_children():
            widget.destroy()
        
        concepts = manager.get_concepts()
        
        if not concepts or current_concept_index >= len(concepts):
            Label.heading(parent, "No concepts available").pack(pady=50)
            return
        
        concept = concepts[current_concept_index]
        details = manager.get_concept_details(concept)
        
        # Scrollable content
        scroll = ctk.CTkScrollableFrame(parent, fg_color=Colors.BACKGROUND)
        scroll.pack(fill='both', expand=True, padx=50, pady=30)
        
        # Progress
        progress = Label.muted(scroll, f"Concept {current_concept_index + 1} of {len(concepts)}")
        progress.pack(pady=(0, 10))
        
        # Title
        title = Label.title(scroll, details['name'])
        title.pack(pady=(0, 20))
        
        # Badges
        badge_frame = ctk.CTkFrame(scroll, fg_color='transparent')
        badge_frame.pack(pady=(0, 30))
        
        if details.get('iterable'):
            Badge.create(
                badge_frame, 
                f"📦 {details['iterable']['name']}"
            ).pack(side='left', padx=5)
        
        if details.get('method'):
            Badge.create(
                badge_frame,
                f"⚙️ {details['method']['name']}",
                bg_color=Colors.SUCCESS_SUBTLE,
                fg_color=Colors.SUCCESS
            ).pack(side='left', padx=5)
        
        # Explanation card
        explain_card = Card.create(scroll)
        explain_card.pack(fill='x', pady=(0, 20))
        
        Label.heading(explain_card, "📖 Explanation").pack(anchor='w', padx=25, pady=(25, 10))
        Label.body(explain_card, details['explanation']).pack(anchor='w', padx=25, pady=(0, 25))
        
        # Syntax card
        syntax_card = Card.create(scroll)
        syntax_card.pack(fill='x', pady=(0, 20))
        
        Label.heading(syntax_card, "✏️ Syntax Pattern").pack(anchor='w', padx=25, pady=(25, 10))
        CodeBlock.create(syntax_card, details['syntax'], height=80).pack(padx=25, pady=(0, 25))
        
        # Code example card
        code_card = Card.create(scroll)
        code_card.pack(fill='x', pady=(0, 30))
        
        Label.heading(code_card, "💻 Code Example").pack(anchor='w', padx=25, pady=(25, 10))
        CodeBlock.create(code_card, details['code'], height=200).pack(padx=25, pady=(0, 25))
        
        # Navigation
        nav_frame = ctk.CTkFrame(scroll, fg_color='transparent')
        nav_frame.pack()
        
        if current_concept_index > 0:
            Button.create(
                nav_frame,
                "← Previous",
                lambda: LearnScreen.create(parent, manager, current_concept_index - 1),
                style='secondary',
                width=150
            ).pack(side='left', padx=10)
        
        if current_concept_index < len(concepts) - 1:
            Button.create(
                nav_frame,
                "Next →",
                lambda: LearnScreen.create(parent, manager, current_concept_index + 1),
                style='primary',
                width=150
            ).pack(side='left', padx=0)


class PracticeScreen:
    """Practice screen (placeholder)"""
    
    @staticmethod
    def create(parent, manager):
        """Create practice screen"""
        for widget in parent.winfo_children():
            widget.destroy()
        
        Label.title(parent, "✏️ Practice Problems").pack(pady=50)
        Label.body(parent, "Coming next!").pack()


class ProgressScreen:
    """Progress screen (placeholder)"""
    
    @staticmethod
    def create(parent, manager):
        """Create progress screen"""
        for widget in parent.winfo_children():
            widget.destroy()
        
        Label.title(parent, "📊 Your Progress").pack(pady=50)
        Label.body(parent, "Coming soon!").pack()