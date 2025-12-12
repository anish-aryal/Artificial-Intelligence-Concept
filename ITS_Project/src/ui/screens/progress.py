"""
Progress Screen - User statistics and achievements
"""

import customtkinter as ctk
from src.ui.components import Button, Card, Badge
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
        main = ctk.CTkFrame(parent, fg_color=Colors.BACKGROUND)
        main.pack(fill='both', expand=True, padx=Spacing.GIANT, pady=Spacing.XL)
        
        # === HEADER ROW ===
        header_row = ctk.CTkFrame(main, fg_color='transparent')
        header_row.pack(fill='x', pady=(0, Spacing.XL))
        
        # Left: Back button + Title
        left_header = ctk.CTkFrame(header_row, fg_color='transparent')
        left_header.pack(side='left')
        
        if on_back:
            Button.create(
                left_header,
                f"{Icons.ARROW_LEFT} Back",
                on_back,
                variant='ghost',
                size='sm'
            ).pack(anchor='w', pady=(0, Spacing.SM))
        
        ctk.CTkLabel(
            left_header,
            text="Your Progress",
            font=(Typography.FALLBACK, Typography.H1, 'bold'),
            text_color=Colors.TEXT_PRIMARY
        ).pack(anchor='w')
        
        # Right: Refresh button
        right_header = ctk.CTkFrame(header_row, fg_color='transparent')
        right_header.pack(side='right')

        #frame to keep both buttons together sideby side
        right_header_frame = ctk.CTkFrame( right_header, fg_color='transparent')
        right_header_frame.pack()
        
        Button.create(
            right_header_frame,
            f"{Icons.CIRCLE} Refresh",
            lambda: ProgressScreen.create(parent, manager, gamification, on_back),
            variant='secondary',
            size='sm'
        ).pack(side='left', padx=(0, Spacing.SM))


        def confirm_reset():
            # --- Dialog Window ---
            dialog = ctk.CTkToplevel(parent)
            dialog.title("Reset Progress")
            dialog.geometry("600x440")
            dialog.transient(parent)
            dialog.grab_set()

            # Center the dialog
            dialog.update_idletasks()
            x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
            y = (dialog.winfo_screenheight() // 2) - (440 // 2)
            dialog.geometry(f"400x440+{x}+{y}")

            # --- Content Container ---
            dialog_content = ctk.CTkFrame(dialog, fg_color=Colors.BACKGROUND)
            dialog_content.pack(fill="both", expand=True, padx=Spacing.XL, pady=Spacing.XL)

            # Title
            ctk.CTkLabel(
                dialog_content,
                text="Reset All Progress?",
                font=(Typography.FALLBACK, Typography.H3, "bold"),
                text_color=Colors.TEXT_PRIMARY,
            ).pack(pady=(0, Spacing.SM))

            # Message
            ctk.CTkLabel(
                dialog_content,
                text="This will permanently delete:\n"
                    "• All XP and levels\n"
                    "• Solved problems\n"
                    "• Achievements\n\n"
                    "This action cannot be undone.",
                font=(Typography.FALLBACK, Typography.BODY),
                text_color=Colors.TEXT_SECONDARY,
                justify="left",
            ).pack(pady=(0, Spacing.LG))

            # --- Buttons Row ---
            button_row = ctk.CTkFrame(dialog_content, fg_color="transparent")
            button_row.pack(pady=(Spacing.SM, 0))

            # Action handlers
            def do_reset():
                gamification.reset_progress()
                dialog.destroy()
                ProgressScreen.create(parent, manager, gamification, on_back)

            # Cancel Button
            Button.create(
                button_row,
                "Cancel",
                dialog.destroy,
                variant="secondary",
                size="md",
            ).pack(side="left", padx=(0, Spacing.SM))

            # Reset Button
            Button.create(
                button_row,
                "Reset Progress",
                do_reset,
                variant="ghost",
                size="md",
            ).pack(side="left")

        Button.create(
            right_header_frame,
            "Reset All Progress",
            confirm_reset,
            variant='ghost',
            size='sm'
        ).pack(side="left")
        

        
        # === CONTENT GRID ===
        content = ctk.CTkFrame(main, fg_color='transparent')
        content.pack(fill='both', expand=True)
        
        content.grid_columnconfigure(0, weight=2, minsize=500)
        content.grid_columnconfigure(1, weight=1, minsize=350)
        content.grid_rowconfigure(0, weight=1)
        
        # === LEFT COLUMN ===
        left_col = ctk.CTkFrame(content, fg_color='transparent')
        left_col.grid(row=0, column=0, sticky='nsew', padx=(0, Spacing.LG))
        
        # === COMBINED LEVEL + XP CARD ===
        level_xp_card = Card.create(left_col)
        level_xp_card.pack(fill='x', pady=(0, Spacing.LG))
        
        level_xp_content = ctk.CTkFrame(level_xp_card, fg_color='transparent')
        level_xp_content.pack(fill='x', padx=Spacing.XL, pady=Spacing.LG)
        
        # Top row: Level circle + XP info
        top_row = ctk.CTkFrame(level_xp_content, fg_color='transparent')
        top_row.pack(fill='x', pady=(0, Spacing.BASE))
        
        # Left: Level circle
        level_circle = ctk.CTkFrame(
            top_row,
            fg_color=Colors.PRIMARY,
            corner_radius=40,
            width=80,
            height=80
        )
        level_circle.pack(side='left', padx=(0, Spacing.LG))
        level_circle.pack_propagate(False)
        
        ctk.CTkLabel(
            level_circle,
            text=str(stats['level']),
            font=(Typography.FALLBACK, Typography.DISPLAY, 'bold'),
            text_color=Colors.TEXT_INVERSE
        ).pack(expand=True)
        
        # Right: XP details
        xp_info = ctk.CTkFrame(top_row, fg_color='transparent')
        xp_info.pack(side='left', fill='both', expand=True)
        
        ctk.CTkLabel(
            xp_info,
            text=f"Level {stats['level']}",
            font=(Typography.FALLBACK, Typography.H3, 'bold'),
            text_color=Colors.TEXT_PRIMARY
        ).pack(anchor='w')
        
        xp_needed = stats['xp_for_next'] - stats['xp']
        if xp_needed > 0:
            ctk.CTkLabel(
                xp_info,
                text=f"{stats['xp']} / {stats['xp_for_next']} XP",
                font=(Typography.FALLBACK, Typography.BODY),
                text_color=Colors.TEXT_SECONDARY
            ).pack(anchor='w', pady=(Spacing.XXS, 0))
            
            ctk.CTkLabel(
                xp_info,
                text=f"{xp_needed} XP until Level {stats['level'] + 1}",
                font=(Typography.FALLBACK, Typography.BODY_SMALL),
                text_color=Colors.TEXT_MUTED
            ).pack(anchor='w', pady=(Spacing.XXS, 0))
        else:
            ctk.CTkLabel(
                xp_info,
                text=f"{stats['xp']} XP • Max Level!",
                font=(Typography.FALLBACK, Typography.BODY, 'bold'),
                text_color=Colors.PRIMARY
            ).pack(anchor='w')
        
        # Progress bar
        progress_bg = ctk.CTkFrame(
            level_xp_content,
            fg_color=Colors.GRAY_200,
            height=10,
            corner_radius=5
        )
        progress_bg.pack(fill='x')
        progress_bg.pack_propagate(False)
        
        percentage = min(xp_progress['percentage'], 100)
        progress_fill = ctk.CTkFrame(
            progress_bg,
            fg_color=Colors.PRIMARY,
            corner_radius=5
        )
        progress_fill.place(relx=0, rely=0, relwidth=percentage/100, relheight=1)
        
        # === OPTIMIZED STATISTICS CARD ===
        stats_card = Card.create(left_col)
        stats_card.pack(fill='both', expand=True)
        
        stats_content = ctk.CTkFrame(stats_card, fg_color='transparent')
        stats_content.pack(fill='both', expand=True, padx=Spacing.XL, pady=Spacing.LG)
        
        # Header
        ctk.CTkLabel(
            stats_content,
            text="Statistics",
            font=(Typography.FALLBACK, Typography.H5, 'bold'),
            text_color=Colors.TEXT_PRIMARY
        ).pack(anchor='w', pady=(0, Spacing.BASE))
        
        # Stats grid - 3 columns, 2 rows
        stats_grid = ctk.CTkFrame(stats_content, fg_color='transparent')
        stats_grid.pack(fill='both', expand=True)
        
        # Equal column distribution
        for i in range(3):
            stats_grid.grid_columnconfigure(i, weight=1, uniform='stat')
        for i in range(2):
            stats_grid.grid_rowconfigure(i, weight=1, uniform='stat')
        
        # Stat items with better visual design
        stat_items = [
            {
                'value': stats['problems_solved'],
                'label': 'Solved',
                'icon': Icons.CHECK,
                'bg_color': Colors.SUCCESS_SUBTLE,
                'icon_color': Colors.SUCCESS,
                'row': 0,
                'col': 0
            },
            {
                'value': stats['problems_attempted'],
                'label': 'Attempted',
                'icon': Icons.CIRCLE,
                'bg_color': Colors.INFO_SUBTLE,
                'icon_color': Colors.INFO,
                'row': 0,
                'col': 1
            },
            {
                'value': f"{stats['success_rate']:.0f}%",
                'label': 'Success Rate',
                'icon': Icons.STAR,
                'bg_color': Colors.PRIMARY_SUBTLE,
                'icon_color': Colors.PRIMARY,
                'row': 0,
                'col': 2
            },
            {
                'value': stats['perfect_scores'],
                'label': 'Perfect',
                'icon': Icons.STAR,
                'bg_color': Colors.WARNING_SUBTLE,
                'icon_color': Colors.WARNING,
                'row': 1,
                'col': 0
            },
            {
                'value': stats['concepts_completed'],
                'label': 'Learned',
                'icon': Icons.CHECK,
                'bg_color': Colors.INFO_SUBTLE,
                'icon_color': Colors.INFO,
                'row': 1,
                'col': 1
            },
            {
                'value': stats['hints_used'],
                'label': 'Hints',
                'icon': Icons.CIRCLE,
                'bg_color': Colors.GRAY_100,
                'icon_color': Colors.TEXT_MUTED,
                'row': 1,
                'col': 2
            }
        ]
        
        # Create modern stat cards
        for item in stat_items:
            # Card container
            stat_container = ctk.CTkFrame(
                stats_grid,
                fg_color=item['bg_color'],
                corner_radius=Effects.RADIUS_MD
            )
            stat_container.grid(
                row=item['row'],
                column=item['col'],
                padx=Spacing.SM,
                pady=Spacing.SM,
                sticky='nsew'
            )
            
            # Inner content
            stat_inner = ctk.CTkFrame(stat_container, fg_color='transparent')
            stat_inner.pack(expand=True, pady=Spacing.BASE)
            
            # Icon and value in horizontal layout
            top_section = ctk.CTkFrame(stat_inner, fg_color='transparent')
            top_section.pack()
            
            ctk.CTkLabel(
                top_section,
                text=item['icon'],
                font=(Typography.FALLBACK, Typography.H3, 'bold'),
                text_color=item['icon_color']
            ).pack(side='left', padx=(0, Spacing.SM))
            
            ctk.CTkLabel(
                top_section,
                text=str(item['value']),
                font=(Typography.FALLBACK, Typography.H2, 'bold'),
                text_color=item['icon_color']
            ).pack(side='left')
            
            # Label below
            ctk.CTkLabel(
                stat_inner,
                text=item['label'],
                font=(Typography.FALLBACK, Typography.BODY_SMALL),
                text_color=Colors.TEXT_SECONDARY
            ).pack(pady=(Spacing.XXS, 0))
        
        # === RIGHT COLUMN ===
        right_col = ctk.CTkFrame(content, fg_color='transparent')
        right_col.grid(row=0, column=1, sticky='nsew')
        
        # Achievements Card (ribbon/list style)
        ach_card = Card.create(right_col)
        ach_card.pack(fill='x', pady=(0, Spacing.LG))
        
        ach_content = ctk.CTkFrame(ach_card, fg_color='transparent')
        ach_content.pack(fill='x', padx=Spacing.XL, pady=Spacing.LG)
        
        # Header
        ctk.CTkLabel(
            ach_content,
            text="Achievements",
            font=(Typography.FALLBACK, Typography.H5, 'bold'),
            text_color=Colors.TEXT_PRIMARY
        ).pack(anchor='w', pady=(0, Spacing.BASE))
        
        # Achievement list
        achievements = [
            {
                'icon': Icons.CHECK,
                'title': 'First Steps',
                'desc': 'Solve your first problem',
                'unlocked': stats['problems_solved'] >= 1
            },
            {
                'icon': Icons.STAR,
                'title': 'Problem Solver',
                'desc': 'Solve 5 problems',
                'unlocked': stats['problems_solved'] >= 5
            },
            {
                'icon': Icons.STAR,
                'title': 'Perfectionist',
                'desc': 'Get 3 perfect scores',
                'unlocked': stats['perfect_scores'] >= 3
            },
            {
                'icon': Icons.STAR,
                'title': 'Level Master',
                'desc': 'Reach Level 3',
                'unlocked': stats['level'] >= 3
            }
        ]
        
        # Create ribbon-style list
        for idx, ach in enumerate(achievements):
            # Achievement row
            ach_row = ctk.CTkFrame(
                ach_content,
                fg_color=Colors.SUCCESS_SUBTLE if ach['unlocked'] else Colors.GRAY_50,
                corner_radius=Effects.RADIUS_SM,
                height=60
            )
            ach_row.pack(fill='x', pady=Spacing.XS)
            ach_row.pack_propagate(False)
            
            # Inner content with horizontal layout
            ach_inner = ctk.CTkFrame(ach_row, fg_color='transparent')
            ach_inner.pack(fill='both', expand=True, padx=Spacing.BASE, pady=Spacing.SM)
            
            # Left: Icon in circle
            icon_container = ctk.CTkFrame(
                ach_inner,
                fg_color=Colors.SUCCESS if ach['unlocked'] else Colors.GRAY_200,
                corner_radius=20,
                width=40,
                height=40
            )
            icon_container.pack(side='left', padx=(0, Spacing.BASE))
            icon_container.pack_propagate(False)
            
            icon_color = Colors.TEXT_INVERSE if ach['unlocked'] else Colors.TEXT_MUTED
            ctk.CTkLabel(
                icon_container,
                text=ach['icon'],
                font=(Typography.FALLBACK, Typography.H4, 'bold'),
                text_color=icon_color
            ).pack(expand=True)
            
            # Middle: Title and description
            text_container = ctk.CTkFrame(ach_inner, fg_color='transparent')
            text_container.pack(side='left', fill='both', expand=True)
            
            title_color = Colors.TEXT_PRIMARY if ach['unlocked'] else Colors.TEXT_MUTED
            ctk.CTkLabel(
                text_container,
                text=ach['title'],
                font=(Typography.FALLBACK, Typography.BODY, 'bold'),
                text_color=title_color
            ).pack(anchor='w')
            
            ctk.CTkLabel(
                text_container,
                text=ach['desc'],
                font=(Typography.FALLBACK, Typography.CAPTION),
                text_color=Colors.TEXT_MUTED
            ).pack(anchor='w')
            
            # Right: Status badge (if unlocked)
            if ach['unlocked']:
                status_badge = ctk.CTkFrame(
                    ach_inner,
                    fg_color=Colors.SUCCESS,
                    corner_radius=12
                )
                status_badge.pack(side='right')
                
                ctk.CTkLabel(
                    status_badge,
                    text="✓",
                    font=(Typography.FALLBACK, Typography.BODY, 'bold'),
                    text_color=Colors.TEXT_INVERSE
                ).pack(padx=Spacing.SM, pady=Spacing.XXS)
        
        # Solved Problems Card
        if stats['solved_problems']:
            solved_card = Card.create(right_col)
            solved_card.pack(fill='both', expand=True)
            
            solved_content = ctk.CTkFrame(solved_card, fg_color='transparent')
            solved_content.pack(fill='both', expand=True, padx=Spacing.XL, pady=Spacing.LG)
            
            # Header
            ctk.CTkLabel(
                solved_content,
                text=f"Solved Problems ({len(stats['solved_problems'])})",
                font=(Typography.FALLBACK, Typography.H5, 'bold'),
                text_color=Colors.TEXT_PRIMARY
            ).pack(anchor='w', pady=(0, Spacing.BASE))
            
            # Scrollable list
            solved_list = ctk.CTkScrollableFrame(
                solved_content,
                fg_color='transparent',
                height=200
            )
            solved_list.pack(fill='both', expand=True)
            
            for idx, problem_name in enumerate(stats['solved_problems']):
                problem_row = ctk.CTkFrame(
                    solved_list,
                    fg_color=Colors.GRAY_50 if idx % 2 == 0 else 'transparent',
                    corner_radius=Effects.RADIUS_SM
                )
                problem_row.pack(fill='x', pady=Spacing.XXS)
                
                problem_inner = ctk.CTkFrame(problem_row, fg_color='transparent')
                problem_inner.pack(fill='x', padx=Spacing.BASE, pady=Spacing.SM)
                
                ctk.CTkLabel(
                    problem_inner,
                    text=Icons.CHECK,
                    font=(Typography.FALLBACK, Typography.BODY, 'bold'),
                    text_color=Colors.SUCCESS,
                    width=24
                ).pack(side='left')
                
                ctk.CTkLabel(
                    problem_inner,
                    text=problem_name,
                    font=(Typography.FALLBACK, Typography.BODY_SMALL),
                    text_color=Colors.TEXT_PRIMARY
                ).pack(side='left', padx=(Spacing.SM, 0))
        
        # === FOOTER ===
        footer = ctk.CTkFrame(main, fg_color='transparent')
        footer.pack(fill='x', pady=(Spacing.XL, 0))
        
        def confirm_reset():
            dialog = ctk.CTkToplevel(parent)
            dialog.title("Reset Progress")
            dialog.geometry("400x220")
            dialog.transient(parent)
            dialog.grab_set()
            
            dialog.update_idletasks()
            x = (dialog.winfo_screenwidth() // 2) - 200
            y = (dialog.winfo_screenheight() // 2) - 110
            dialog.geometry(f"400x220+{x}+{y}")
            
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
                text="This will permanently delete:\n• All XP and levels\n• Solved problems\n• Achievements\n\nThis action cannot be undone!",
                font=(Typography.FALLBACK, Typography.BODY),
                text_color=Colors.TEXT_SECONDARY,
                justify='left'
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
        
        Button.create(
            footer,
            "Reset All Progress",
            confirm_reset,
            variant='ghost',
            size='sm'
        ).pack(anchor='center')
        
       