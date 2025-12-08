"""
Screen Modules
Different screens for the tutoring system
"""

import tkinter as tk
from .components import Button, Card, Label, CodeBlock, InputBox, Badge, Divider
from .styles import Colors, Fonts, Spacing


class WelcomeScreen:
    """Welcome/Home screen with introduction"""
    
    @staticmethod
    def create(parent, manager, on_learn, on_practice):
        """
        Create welcome screen
        
        Args:
            parent: Parent widget
            manager: OntologyManager instance
            on_learn: Callback for Learn button
            on_practice: Callback for Practice button
        """
        # Clear parent
        for widget in parent.winfo_children():
            widget.destroy()
        
        # Main container
        container = tk.Frame(parent, bg=Colors.BACKGROUND)
        container.pack(fill='both', expand=True, padx=40, pady=40)
        
        # Welcome card
        welcome_card = Card.create(container)
        welcome_card.pack(fill='x', pady=20)
        
        # Title
        title = Label.title(welcome_card, "🐍 Welcome to Python Iteration Tutor!")
        title.pack(pady=(30, 10))
        
        # Subtitle
        subtitle = Label.body(
            welcome_card, 
            "Master Python iteration through interactive learning and practice"
        )
        subtitle.pack(pady=(0, 30))
        
        # Stats card
        stats_card = Card.create(container)
        stats_card.pack(fill='x', pady=20)
        
        stats_title = Label.heading(stats_card, "📊 What You'll Learn")
        stats_title.pack(pady=(20, 15))
        
        # Get statistics
        stats = manager.get_statistics()
        
        # Stats grid
        stats_frame = tk.Frame(stats_card, bg=Colors.SURFACE)
        stats_frame.pack(pady=(0, 20))
        
        # Concepts stat
        concept_frame = tk.Frame(stats_frame, bg=Colors.SURFACE)
        concept_frame.pack(side='left', padx=30)
        
        concept_num = tk.Label(
            concept_frame,
            text=str(stats['concepts']),
            font=('Arial', 48, 'bold'),
            bg=Colors.SURFACE,
            fg=Colors.PRIMARY
        )
        concept_num.pack()
        
        concept_label = Label.muted(concept_frame, "Concepts")
        concept_label.pack()
        
        # Problems stat
        problem_frame = tk.Frame(stats_frame, bg=Colors.SURFACE)
        problem_frame.pack(side='left', padx=30)
        
        problem_num = tk.Label(
            problem_frame,
            text=str(stats['problems']),
            font=('Arial', 48, 'bold'),
            bg=Colors.SURFACE,
            fg=Colors.SUCCESS
        )
        problem_num.pack()
        
        problem_label = Label.muted(problem_frame, "Practice Problems")
        problem_label.pack()
        
        # Test cases stat
        test_frame = tk.Frame(stats_frame, bg=Colors.SURFACE)
        test_frame.pack(side='left', padx=30)
        
        test_num = tk.Label(
            test_frame,
            text=str(stats['test_cases']),
            font=('Arial', 48, 'bold'),
            bg=Colors.SURFACE,
            fg=Colors.INFO
        )
        test_num.pack()
        
        test_label = Label.muted(test_frame, "Test Cases")
        test_label.pack()
        
        # Action buttons
        button_card = Card.create(container)
        button_card.pack(fill='x', pady=20)
        
        button_title = Label.heading(button_card, "🚀 Get Started")
        button_title.pack(pady=(20, 15))
        
        button_frame = tk.Frame(button_card, bg=Colors.SURFACE)
        button_frame.pack(pady=(0, 25))
        
        learn_btn = Button.create(
            button_frame, 
            "📚 Start Learning", 
            on_learn, 
            style='primary',
            width=180
        )
        learn_btn.pack(side='left', padx=10)
        
        practice_btn = Button.create(
            button_frame, 
            "✏️ Practice Now", 
            on_practice, 
            style='success',
            width=180
        )
        practice_btn.pack(side='left', padx=10)


class LearnScreen:
    """Learning screen showing concepts"""
    
    @staticmethod
    def create(parent, manager, current_concept_index=0):
        """
        Create learning screen
        
        Args:
            parent: Parent widget
            manager: OntologyManager instance
            current_concept_index: Which concept to show
        """
        # Clear parent
        for widget in parent.winfo_children():
            widget.destroy()
        
        # Get all concepts
        concepts = manager.get_concepts()
        
        if not concepts or current_concept_index >= len(concepts):
            Label.heading(parent, "No concepts available").pack(pady=50)
            return
        
        current_concept = concepts[current_concept_index]
        details = manager.get_concept_details(current_concept)
        
        # Main container with scrolling
        canvas = tk.Canvas(parent, bg=Colors.BACKGROUND, highlightthickness=0)
        scrollbar = tk.Scrollbar(parent, orient='vertical', command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=Colors.BACKGROUND)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Content
        content = tk.Frame(scrollable_frame, bg=Colors.BACKGROUND)
        content.pack(fill='both', expand=True, padx=40, pady=30)
        
        # Header card
        header_card = Card.create(content)
        header_card.pack(fill='x', pady=(0, 20))
        
        # Progress indicator
        progress_text = f"Concept {current_concept_index + 1} of {len(concepts)}"
        progress_label = Label.muted(header_card, progress_text)
        progress_label.pack(pady=(15, 5))
        
        # Concept name
        concept_title = Label.title(header_card, details['name'])
        concept_title.pack(pady=(5, 15))
        
        # Badges for iterable and method
        badge_frame = tk.Frame(header_card, bg=Colors.SURFACE)
        badge_frame.pack(pady=(0, 20))
        
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
        explain_card = Card.create(content)
        explain_card.pack(fill='x', pady=(0, 20))
        
        Label.heading(explain_card, "📖 Explanation").pack(pady=(20, 10), anchor='w', padx=20)
        Label.body(explain_card, details['explanation']).pack(pady=(0, 20), anchor='w', padx=20)
        
        # Syntax card
        syntax_card = Card.create(content)
        syntax_card.pack(fill='x', pady=(0, 20))
        
        Label.heading(syntax_card, "✏️ Syntax Pattern").pack(pady=(20, 10), anchor='w', padx=20)
        
        syntax_display = CodeBlock.create(syntax_card, details['syntax'], height=3)
        syntax_display.pack(fill='x', padx=20, pady=(0, 20))
        
        # Code example card
        code_card = Card.create(content)
        code_card.pack(fill='x', pady=(0, 20))
        
        Label.heading(code_card, "💻 Code Example").pack(pady=(20, 10), anchor='w', padx=20)
        
        code_display = CodeBlock.create(code_card, details['code'], height=8)
        code_display.pack(fill='x', padx=20, pady=(0, 20))
        
        # Navigation buttons
        nav_card = Card.create(content)
        nav_card.pack(fill='x', pady=(0, 20))
        
        nav_frame = tk.Frame(nav_card, bg=Colors.SURFACE)
        nav_frame.pack(pady=20)
        
        # Previous button
        if current_concept_index > 0:
            prev_btn = Button.create(
                nav_frame,
                "← Previous",
                lambda: LearnScreen.create(parent, manager, current_concept_index - 1),
                style='secondary',
                width=120
            )
            prev_btn.pack(side='left', padx=10)
        
        # Next button
        if current_concept_index < len(concepts) - 1:
            next_btn = Button.create(
                nav_frame,
                "Next →",
                lambda: LearnScreen.create(parent, manager, current_concept_index + 1),
                style='primary',
                width=120
            )
            next_btn.pack(side='left', padx=10)
        
        # Pack canvas and scrollbar
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Mouse wheel scrolling
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", on_mousewheel)


class PracticeScreen:
    """Practice screen with problems (placeholder for now)"""
    
    @staticmethod
    def create(parent, manager):
        """Create practice screen"""
        # Clear parent
        for widget in parent.winfo_children():
            widget.destroy()
        
        Label.title(parent, "✏️ Practice Problems").pack(pady=50)
        Label.body(parent, "Practice screen coming next!").pack(pady=20)


class ProgressScreen:
    """Progress tracking screen (placeholder for now)"""
    
    @staticmethod
    def create(parent, manager):
        """Create progress screen"""
        # Clear parent
        for widget in parent.winfo_children():
            widget.destroy()
        
        Label.title(parent, "📊 Your Progress").pack(pady=50)
        Label.body(parent, "Progress tracking coming soon!").pack(pady=20)