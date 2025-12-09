"""
Main GUI Application
Complete tutoring system using CustomTkinter
"""

import customtkinter as ctk
from .screens import WelcomeScreen, LearnScreen, PracticeScreen, ProgressScreen
from .styles import Colors, Sizes


class PythonIterationTutor:
    """Main application class"""
    
    def __init__(self, ontology_manager):
        """Initialize the application"""
        self.manager = ontology_manager
        self.window = None
        self.content_frame = None
        
        # User progress
        self.current_level = 1
        self.problems_solved = 0
        self.total_score = 0
        self.completed_problems = set()
        
    def create_window(self):
        """Create the main window"""
        self.window = ctk.CTk()
        self.window.title("🐍 Python Iteration Tutor")
        self.window.geometry(f"{Sizes.WINDOW_WIDTH}x{Sizes.WINDOW_HEIGHT}")
        
        # Set minimum size
        self.window.minsize(Sizes.WINDOW_MIN_WIDTH, Sizes.WINDOW_MIN_HEIGHT)
        
        # Create header
        self._create_header()
        
        # Create content area
        self.content_frame = ctk.CTkFrame(self.window, fg_color=Colors.BACKGROUND)
        self.content_frame.pack(fill='both', expand=True)
        
        # Show welcome screen
        self.show_welcome()
        
    def _create_header(self):
        """Create navigation header"""
        header = ctk.CTkFrame(
            self.window,
            fg_color=Colors.PRIMARY,
            height=70,
            corner_radius=0 
        )
        header.pack(fill='x', side='top')
        header.pack_propagate(False)
        
        # Title
        title = ctk.CTkLabel(
            header,
            text="🐍 Python Iteration Tutor",
            font=('Arial', 20, 'bold'),
            text_color='white'
        )
        title.pack(side='left', padx=30, pady=20)
        
        # Navigation buttons
        nav_frame = ctk.CTkFrame(header, fg_color='transparent')
        nav_frame.pack(side='right', padx=30)
        
        # Create nav buttons
        nav_buttons = [
            ("🏠 Home", self.show_welcome),
            ("📚 Learn", self.show_learn),
            ("✏️ Practice", self.show_practice),
            ("📊 Progress", self.show_progress)
        ]
        
        for text, command in nav_buttons:
            btn = ctk.CTkButton(
                nav_frame,
                text=text,
                command=command,
                width=100,
                height=36,
                fg_color=Colors.PRIMARY_DARK,
                hover_color='#3730a3',
                corner_radius=2,
                font=('Arial', 11, 'bold')
            )
            btn.pack(side='left', padx=5)
    
    def show_welcome(self):
        """Show welcome screen"""
        WelcomeScreen.create(
            self.content_frame,
            self.manager,
            on_learn=self.show_learn,
            on_practice=self.show_practice
        )
    
    def show_learn(self):
        """Show learning screen"""
        LearnScreen.create(
            self.content_frame,
            self.manager,
            current_concept_index=0
        )
    
    def show_practice(self):
        """Show practice screen"""
        PracticeScreen.create(
            self.content_frame,
            self.manager
        )
    
    def show_progress(self):
        """Show progress screen"""
        ProgressScreen.create(
            self.content_frame,
            self.manager
        )
    
    def run(self):
        """Start the application"""
        self.create_window()
        self.window.mainloop()