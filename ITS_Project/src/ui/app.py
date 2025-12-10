"""
Main GUI Application - Modern & Professional
"""

import customtkinter as ctk
from src.ui.screens import DashboardScreen, LearnScreen, PracticeScreen, ProgressScreen
from src.ui.styles import Colors, Typography, Layout, Spacing
from src.core.gamification import GamificationSystem


class PythonIterationTutor:
    """Main application class"""
    
    def __init__(self, ontology_manager):
        """Initialize application"""
        self.manager = ontology_manager
        self.window = None
        self.content_frame = None
        
        # Initialize gamification
        self.gamification = GamificationSystem()
        
        self.current_screen = 'dashboard'
        
    def create_window(self):
        """Create main window"""
        self.window = ctk.CTk()
        self.window.title("Python Iteration Tutor")
        self.window.geometry(f"{Layout.WINDOW_WIDTH}x{Layout.WINDOW_HEIGHT}")
        
        # Set minimum size
        self.window.minsize(Layout.WINDOW_MIN_WIDTH, Layout.WINDOW_MIN_HEIGHT)
        
        # Configure grid
        self.window.grid_rowconfigure(1, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        
        # Create navbar
        self._create_navbar()
        
        # Create content area
        self.content_frame = ctk.CTkFrame(
            self.window,
            fg_color=Colors.BACKGROUND,
            corner_radius=0
        )
        self.content_frame.grid(row=1, column=0, sticky='nsew')
        
        # Show dashboard
        self.show_dashboard()
        
    def _create_navbar(self):
        """Create navigation bar"""
        navbar = ctk.CTkFrame(
            self.window,
            fg_color=Colors.PRIMARY,
            height=Layout.NAVBAR_HEIGHT,
            corner_radius=0
        )
        navbar.grid(row=0, column=0, sticky='ew')
        navbar.grid_propagate(False)
        
        # Title
        title_frame = ctk.CTkFrame(navbar, fg_color='transparent')
        title_frame.pack(side='left', padx=Spacing.XXL)
        
        title = ctk.CTkLabel(
            title_frame,
            text="Python Iteration Tutor",
            font=(Typography.FALLBACK, Typography.H4, 'bold'),
            text_color='white'
        )
        title.pack()
        
        # Navigation buttons
        nav_buttons = ctk.CTkFrame(navbar, fg_color='transparent')
        nav_buttons.pack(side='right', padx=Spacing.XXL)
        
        buttons = [
            ("Dashboard", self.show_dashboard),
            ("Learn", self.show_learn),
            ("Practice", self.show_practice),
            ("Progress", self.show_progress)
        ]
        
        for text, command in buttons:
            btn = ctk.CTkButton(
                nav_buttons,
                text=text,
                command=command,
                width=100,
                height=36,
                fg_color='transparent',
                hover_color=Colors.PRIMARY_DARK,
                corner_radius=6,
                font=(Typography.FALLBACK, Typography.BODY, 'bold'),
                border_width=0
            )
            btn.pack(side='left', padx=4)
    
    def show_dashboard(self):
        """Show dashboard"""
        self.current_screen = 'dashboard'
        
        user_data = self.gamification.get_stats()
        
        callbacks = {
            'on_learn': self.show_learn,
            'on_practice': self.show_practice,
            'on_progress': self.show_progress
        }
        
        DashboardScreen.create(
            self.content_frame,
            self.manager,
            user_data,
            callbacks
        )
    
    def show_learn(self):
        """Show learning screen"""
        self.current_screen = 'learn'
        LearnScreen.create(
            self.content_frame,
            self.manager,
            current_index=0,
            on_back=self.show_dashboard,
            on_practice=self.show_practice
        )
    
    def show_practice(self):
        """Show practice screen"""
        self.current_screen = 'practice'
        PracticeScreen.create(
            self.content_frame,
            self.manager,
            current_index=0,
            on_back=self.show_dashboard,
            gamification=self.gamification 

        )
    
    def show_progress(self):
        """Show progress screen"""
        self.current_screen = 'progress'
        ProgressScreen.create(
            self.content_frame,
            self.manager
        )
    
    def run(self):
        """Start application"""
        self.create_window()
        self.window.mainloop()
