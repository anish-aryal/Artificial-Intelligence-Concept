"""
Progress Screen - User statistics and achievements
"""

import customtkinter as ctk
from src.ui.components import Button, Card, Badge, ProgressBar
from src.ui.styles import Colors, Typography, Spacing, Effects
from src.ui.icons import Icons


class ProgressScreen:
    """Progress screen with statistics and achievements"""
    
    @staticmethod
    def create(parent, manager, gamification=None, on_back=None):
        """Create progress screen"""
        for widget in parent.winfo_children():
            widget.destroy()
        
        if not gamification:
            # No gamification available
            container = ctk.CTkFrame(parent, fg_color=Colors.BACKGROUND)
            container.pack(fill='both', expand=True)
            
            ctk.CTkLabel(
                container,
                text="Progress tracking not available",
                font=(Typography.FALLBACK, Typography.H2),
                text_color=Colors.TEXT_SECONDARY
            ).pack(expand=True)
            return
        
        # Get statistics
        stats = gamification.get_stats()
        xp_progress = gamification.get_xp_progress()
        
        # Main container
        scroll = ctk.CTkScrollableFrame(parent, fg_color=Colors.BACKGROUND)
        scroll.pack(fill='both', expand=True, padx=Spacing.GIANT, pady=Spacing.XXL)
        
        # Header with back button
        if on_back:
            back_button = Button.create(
                scroll,
                f"{Icons.ARROW_LEFT} Back to Dashboard",
                on_back,
                variant='ghost',
                size='sm'
            )
            back_button.pack(anchor='w', pady=(0, Spacing.BASE))
        
        # Page title
        title_label = ctk.CTkLabel(
            scroll,
            text="Your Progress",
            font=(Typography.FALLBACK, Typography.H1, 'bold'),
            text_color=Colors.TEXT_PRIMARY
        )
        title_label.pack(anchor='w', pady=(0, Spacing.XS))
        
        subtitle_label = ctk.CTkLabel(
            scroll,
            text="Track your learning journey and achievements",
            font=(Typography.FALLBACK, Typography.BODY_LARGE),
            text_color=Colors.TEXT_SECONDARY
        )
        subtitle_label.pack(anchor='w', pady=(0, Spacing.XXL))
        
        # === LEVEL & XP CARD ===
        level_card = Card.create(scroll)
        level_card.pack(fill='x', pady=(0, Spacing.XL))
        
        level_content = ctk.CTkFrame(level_card, fg_color='transparent')
        level_content.pack(fill='x', padx=Spacing.XXL, pady=Spacing.XXL)
        
        # Level badge (large circle)
        level_badge_container = ctk.CTkFrame(level_content, fg_color='transparent')
        level_badge_container.pack(pady=(0, Spacing.BASE))
        
        level_circle = ctk.CTkFrame(
            level_badge_container,
            fg_color=Colors.PRIMARY,
            corner_radius=60,
            width=120,
            height=120
        )
        level_circle.pack()
        level_circle.pack_propagate(False)
        
        level_number = ctk.CTkLabel(
            level_circle,
            text=str(stats['level']),
            font=(Typography.FALLBACK, Typography.DISPLAY, 'bold'),
            text_color=Colors.TEXT_INVERSE
        )
        level_number.pack(expand=True)
        
        # Level text
        ctk.CTkLabel(
            level_content,
            text=f"Level {stats['level']}",
            font=(Typography.FALLBACK, Typography.H2, 'bold'),
            text_color=Colors.TEXT_PRIMARY
        ).pack(pady=(0, Spacing.XXS))
        
        # XP progress
        xp_text = f"{stats['xp']} / {stats['xp_for_next']} XP"
        ctk.CTkLabel(
            level_content,
            text=xp_text,
            font=(Typography.FALLBACK, Typography.BODY),
            text_color=Colors.TEXT_SECONDARY
        ).pack(pady=(0, Spacing.BASE))
        
        # Progress bar
        progress_bar_container = ctk.CTkFrame(
            level_content,
            fg_color=Colors.GRAY_200,
            height=12,
            corner_radius=6
        )
        progress_bar_container.pack(fill='x', pady=(0, Spacing.SM))
        progress_bar_container.pack_propagate(False)
        
        percentage = min(xp_progress['percentage'], 100)
        progress_fill = ctk.CTkFrame(
            progress_bar_container,
            fg_color=Colors.PRIMARY,
            height=12,
            corner_radius=6
        )
        progress_fill.place(relx=0, rely=0, relwidth=percentage/100, relheight=1)
        
        # XP to next level
        xp_needed = stats['xp_for_next'] - stats['xp']
        if xp_needed > 0:
            ctk.CTkLabel(
                level_content,
                text=f"{xp_needed} XP until Level {stats['level'] + 1}",
                font=(Typography.FALLBACK, Typography.BODY_SMALL),
                text_color=Colors.TEXT_MUTED
            ).pack()
        else:
            ctk.CTkLabel(
                level_content,
                text="Max level reached!",
                font=(Typography.FALLBACK, Typography.BODY_SMALL, 'bold'),
                text_color=Colors.PRIMARY
            ).pack()
        
        # === STATISTICS GRID ===
        stats_title = ctk.CTkLabel(
            scroll,
            text="Statistics",
            font=(Typography.FALLBACK, Typography.H3, 'bold'),
            text_color=Colors.TEXT_PRIMARY
        )
        stats_title.pack(anchor='w', pady=(0, Spacing.BASE))
        
        stats_grid = ctk.CTkFrame(scroll, fg_color='transparent')
        stats_grid.pack(fill='x', pady=(0, Spacing.XL))
        
        # Configure grid
        stats_grid.grid_columnconfigure(0, weight=1)
        stats_grid.grid_columnconfigure(1, weight=1)
        stats_grid.grid_columnconfigure(2, weight=1)
        
        # Stat cards data
        stat_items = [
            {
                'value': stats['problems_solved'],
                'label': 'Problems Solved',
                'icon': Icons.CHECK,
                'color': Colors.SUCCESS,
                'row': 0,
                'col': 0
            },
            {
                'value': stats['problems_attempted'],
                'label': 'Problems Attempted',
                'icon': Icons.CIRCLE,
                'color': Colors.INFO,
                'row': 0,
                'col': 1
            },
            {
                'value': f"{stats['success_rate']:.0f}%",
                'label': 'Success Rate',
                'icon': Icons.STAR,
                'color': Colors.PRIMARY,
                'row': 0,
                'col': 2
            },
            {
                'value': stats['perfect_scores'],
                'label': 'Perfect Scores',
                'icon': Icons.STAR,
                'color': Colors.WARNING,
                'row': 1,
                'col': 0
            },
            {
                'value': stats['concepts_completed'],
                'label': 'Concepts Learned',
                'icon': Icons.CHECK,
                'color': Colors.INFO,
                'row': 1,
                'col': 1
            },
            {
                'value': stats['hints_used'],
                'label': 'Hints Used',
                'icon': Icons.CIRCLE,
                'color': Colors.TEXT_MUTED,
                'row': 1,
                'col': 2
            }
        ]
        
        # Create stat cards
        for item in stat_items:
            stat_card = Card.create(stats_grid)
            stat_card.grid(
                row=item['row'],
                column=item['col'],
                padx=Spacing.SM,
                pady=Spacing.SM,
                sticky='nsew'
            )
            
            stat_content = ctk.CTkFrame(stat_card, fg_color='transparent')
            stat_content.pack(fill='both', expand=True, padx=Spacing.LG, pady=Spacing.LG)
            
            # Icon
            icon_label = ctk.CTkLabel(
                stat_content,
                text=item['icon'],
                font=(Typography.FALLBACK, Typography.DISPLAY, 'bold'),
                text_color=item['color']
            )
            icon_label.pack(pady=(0, Spacing.XS))
            
            # Value
            value_label = ctk.CTkLabel(
                stat_content,
                text=str(item['value']),
                font=(Typography.FALLBACK, Typography.H1, 'bold'),
                text_color=item['color']
            )
            value_label.pack(pady=(0, Spacing.XXS))
            
            # Label
            label_label = ctk.CTkLabel(
                stat_content,
                text=item['label'],
                font=(Typography.FALLBACK, Typography.BODY_SMALL),
                text_color=Colors.TEXT_SECONDARY
            )
            label_label.pack()
        
        # === SOLVED PROBLEMS LIST ===
        if stats['solved_problems']:
            solved_title = ctk.CTkLabel(
                scroll,
                text="Solved Problems",
                font=(Typography.FALLBACK, Typography.H3, 'bold'),
                text_color=Colors.TEXT_PRIMARY
            )
            solved_title.pack(anchor='w', pady=(0, Spacing.BASE))
            
            solved_card = Card.create(scroll)
            solved_card.pack(fill='x', pady=(0, Spacing.XL))
            
            solved_content = ctk.CTkFrame(solved_card, fg_color='transparent')
            solved_content.pack(fill='x', padx=Spacing.LG, pady=Spacing.LG)
            
            for idx, problem_name in enumerate(stats['solved_problems']):
                problem_row = ctk.CTkFrame(solved_content, fg_color='transparent')
                problem_row.pack(fill='x', pady=Spacing.XS)
                
                # Checkmark
                check_icon = ctk.CTkLabel(
                    problem_row,
                    text=Icons.CHECK,
                    font=(Typography.FALLBACK, Typography.BODY_LARGE, 'bold'),
                    text_color=Colors.SUCCESS,
                    width=30
                )
                check_icon.pack(side='left')
                
                # Problem name
                problem_label = ctk.CTkLabel(
                    problem_row,
                    text=problem_name,
                    font=(Typography.FALLBACK, Typography.BODY),
                    text_color=Colors.TEXT_PRIMARY
                )
                problem_label.pack(side='left', padx=(Spacing.XS, 0))
        
        # === ACHIEVEMENTS SECTION ===
        achievements_title = ctk.CTkLabel(
            scroll,
            text="Achievements",
            font=(Typography.FALLBACK, Typography.H3, 'bold'),
            text_color=Colors.TEXT_PRIMARY
        )
        achievements_title.pack(anchor='w', pady=(0, Spacing.BASE))
        
        achievements_grid = ctk.CTkFrame(scroll, fg_color='transparent')
        achievements_grid.pack(fill='x', pady=(0, Spacing.XL))
        
        achievements_grid.grid_columnconfigure(0, weight=1)
        achievements_grid.grid_columnconfigure(1, weight=1)
        
        # Achievement cards
        achievements = [
            {
                'icon': Icons.CHECK,
                'title': 'First Steps',
                'description': 'Solve your first problem',
                'unlocked': stats['problems_solved'] >= 1,
                'row': 0,
                'col': 0
            },
            {
                'icon': Icons.STAR,
                'title': 'Problem Solver',
                'description': 'Solve 5 problems',
                'unlocked': stats['problems_solved'] >= 5,
                'row': 0,
                'col': 1
            },
            {
                'icon': Icons.STAR,
                'title': 'Perfectionist',
                'description': 'Get 3 perfect scores',
                'unlocked': stats['perfect_scores'] >= 3,
                'row': 1,
                'col': 0
            },
            {
                'icon': Icons.STAR,
                'title': 'Level Master',
                'description': 'Reach Level 3',
                'unlocked': stats['level'] >= 3,
                'row': 1,
                'col': 1
            }
        ]
        
        for achievement in achievements:
            achievement_card = Card.create(achievements_grid)
            achievement_card.grid(
                row=achievement['row'],
                column=achievement['col'],
                padx=Spacing.SM,
                pady=Spacing.SM,
                sticky='nsew'
            )
            
            # Dim if locked
            card_color = Colors.SURFACE if achievement['unlocked'] else Colors.GRAY_100
            achievement_card.configure(fg_color=card_color)
            
            achievement_content = ctk.CTkFrame(achievement_card, fg_color='transparent')
            achievement_content.pack(fill='both', expand=True, padx=Spacing.BASE, pady=Spacing.BASE)
            
            # Icon (different color if locked)
            icon_color = Colors.SUCCESS if achievement['unlocked'] else Colors.TEXT_MUTED
            icon_label = ctk.CTkLabel(
                achievement_content,
                text=achievement['icon'],
                font=(Typography.FALLBACK, Typography.DISPLAY, 'bold'),
                text_color=icon_color
            )
            icon_label.pack(pady=(Spacing.SM, Spacing.XS))
            
            # Status badge
            if achievement['unlocked']:
                status_badge = ctk.CTkFrame(
                    achievement_content,
                    fg_color=Colors.SUCCESS_SUBTLE,
                    corner_radius=12
                )
                status_badge.pack(pady=(0, Spacing.SM))
                
                ctk.CTkLabel(
                    status_badge,
                    text="UNLOCKED",
                    font=(Typography.FALLBACK, Typography.CAPTION, 'bold'),
                    text_color=Colors.SUCCESS_DARK
                ).pack(padx=Spacing.SM, pady=Spacing.XXS)
            else:
                status_badge = ctk.CTkFrame(
                    achievement_content,
                    fg_color=Colors.GRAY_200,
                    corner_radius=12
                )
                status_badge.pack(pady=(0, Spacing.SM))
                
                ctk.CTkLabel(
                    status_badge,
                    text="LOCKED",
                    font=(Typography.FALLBACK, Typography.CAPTION, 'bold'),
                    text_color=Colors.TEXT_MUTED
                ).pack(padx=Spacing.SM, pady=Spacing.XXS)
            
            # Title
            title_color = Colors.TEXT_PRIMARY if achievement['unlocked'] else Colors.TEXT_MUTED
            title_label = ctk.CTkLabel(
                achievement_content,
                text=achievement['title'],
                font=(Typography.FALLBACK, Typography.BODY, 'bold'),
                text_color=title_color
            )
            title_label.pack(pady=(0, Spacing.XXS))
            
            # Description
            desc_label = ctk.CTkLabel(
                achievement_content,
                text=achievement['description'],
                font=(Typography.FALLBACK, Typography.BODY_SMALL),
                text_color=Colors.TEXT_MUTED,
                wraplength=200
            )
            desc_label.pack()
        
        # === RESET BUTTON ===
        reset_section = ctk.CTkFrame(scroll, fg_color='transparent')
        reset_section.pack(fill='x', pady=(Spacing.XL, 0))
        
        def confirm_reset():
            # Create confirmation dialog
            dialog = ctk.CTkToplevel(parent)
            dialog.title("Reset Progress")
            dialog.geometry("400x200")
            dialog.transient(parent)
            dialog.grab_set()
            
            # Center dialog
            dialog.update_idletasks()
            x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
            y = (dialog.winfo_screenheight() // 2) - (200 // 2)
            dialog.geometry(f"400x200+{x}+{y}")
            
            dialog_content = ctk.CTkFrame(dialog, fg_color=Colors.BACKGROUND)
            dialog_content.pack(fill='both', expand=True, padx=Spacing.XXL, pady=Spacing.XXL)
            
            ctk.CTkLabel(
                dialog_content,
                text="Reset All Progress?",
                font=(Typography.FALLBACK, Typography.H3, 'bold'),
                text_color=Colors.TEXT_PRIMARY
            ).pack(pady=(0, Spacing.BASE))
            
            ctk.CTkLabel(
                dialog_content,
                text="This will delete all your progress,\nXP, levels, and solved problems.\nThis action cannot be undone!",
                font=(Typography.FALLBACK, Typography.BODY),
                text_color=Colors.TEXT_SECONDARY,
                justify='center'
            ).pack(pady=(0, Spacing.XL))
            
            button_row = ctk.CTkFrame(dialog_content, fg_color='transparent')
            button_row.pack()
            
            def do_reset():
                gamification.reset_progress()
                dialog.destroy()
                ProgressScreen.create(parent, manager, gamification, on_back)
            
            Button.create(
                button_row,
                "Cancel",
                dialog.destroy,
                variant='secondary',
                size='md'
            ).pack(side='left', padx=(0, Spacing.SM))
            
            Button.create(
                button_row,
                "Reset Progress",
                do_reset,
                variant='ghost',
                size='md'
            ).pack(side='left')
        
        reset_btn = Button.create(
            reset_section,
            "Reset All Progress",
            confirm_reset,
            variant='ghost',
            size='sm'
        )
        reset_btn.pack(anchor='center')