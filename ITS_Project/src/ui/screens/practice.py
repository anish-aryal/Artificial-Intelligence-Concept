"""
Practice Screen - Code editor with validation
"""

import customtkinter as ctk
from src.ui.components import Button, Card, Badge, CodeDisplay, Alert
from src.ui.styles import Colors, Typography, Spacing, Effects
from src.ui.icons import Icons, IconHelper


class PracticeScreen:
    """Practice screen - results inline"""
    
    @staticmethod
    def create(parent, manager, current_index=0, on_back=None, gamification=None, on_progress_update=None):
        """Create practice screen with callback support"""
        for widget in parent.winfo_children():
            widget.destroy()
        
        problems = manager.get_problems()
        
        if not problems or current_index >= len(problems):
            Alert.create(parent, "No problems available", variant='warning').pack(pady=50)
            return
        
        problem = problems[current_index]
        details = manager.get_problem_details(problem)
        
        # Check if problem was solved
        is_solved = False
        if gamification:
            solved_problems = gamification.solved_problems
            is_solved = details['name'] in solved_problems
        
        # Count solved problems
        solved_count = 0
        if gamification:
            solved_count = len(gamification.solved_problems)
        
        # Header - MODERN DESIGN
        header = ctk.CTkFrame(parent, fg_color=Colors.BACKGROUND)
        header.pack(fill='x', side='top')
        
        hcontent = ctk.CTkFrame(header, fg_color='transparent')
        hcontent.pack(fill='x', padx=Spacing.XXL, pady=Spacing.BASE)
        
        # Back button
        if on_back:
            Button.create(hcontent, f"{Icons.ARROW_LEFT} Back", on_back, variant='ghost', size='sm').pack(anchor='w', pady=(0, Spacing.BASE))
        
        # Progress header row
        progress_header = ctk.CTkFrame(hcontent, fg_color='transparent')
        progress_header.pack(fill='x', pady=(0, Spacing.BASE))
        
        # Left side - Problem info
        left_info = ctk.CTkFrame(progress_header, fg_color='transparent')
        left_info.pack(side='left')
        
        ctk.CTkLabel(
            left_info,
            text=f"Problem {current_index + 1} of {len(problems)}",
            font=(Typography.FALLBACK, Typography.H5, 'bold'),
            text_color=Colors.TEXT_PRIMARY
        ).pack(side='left')
        
        # Right side - Solved count with badge
        right_info = ctk.CTkFrame(progress_header, fg_color='transparent')
        right_info.pack(side='right')
        
        # Solved count badge
        solved_badge_container = ctk.CTkFrame(
            right_info,
            fg_color=Colors.SUCCESS if solved_count > 0 else Colors.GRAY_200,
            corner_radius=12,
            height=24
        )
        solved_badge_container.pack()
        
        solved_badge_content = ctk.CTkFrame(solved_badge_container, fg_color='transparent')
        solved_badge_content.pack(padx=12, pady=4)
        
        ctk.CTkLabel(
            solved_badge_content,
            text=f"✓ {solved_count}/{len(problems)} Solved",
            font=(Typography.FALLBACK, Typography.BODY_SMALL, 'bold'),
            text_color=Colors.TEXT_INVERSE if solved_count > 0 else Colors.TEXT_MUTED
        ).pack()
        
        # SEGMENTED PROGRESS BAR - Full width per problem (3 states: green/blue/gray)
        progress_container = ctk.CTkFrame(hcontent, fg_color='transparent', height=12)
        progress_container.pack(fill='x', pady=(0, Spacing.BASE))
        progress_container.pack_propagate(False)
        
        # Calculate segment dimensions
        total_problems = len(problems)
        segment_width = 1.0 / total_problems if total_problems > 0 else 0
        gap = 0.01  # 1% gap between segments
        
        # Draw each problem as a full-width segment
        for i in range(total_problems):
            problem_obj = problems[i]
            problem_details = manager.get_problem_details(problem_obj)
            is_problem_solved = problem_details['name'] in gamification.solved_problems if gamification else False
            
            # Determine segment color based on state
            if is_problem_solved:
                # Solved = Green
                segment_color = Colors.SUCCESS
            elif i <= current_index:
                # Current or visited but unsolved = Blue
                segment_color = Colors.PRIMARY
            else:
                # Not yet reached = Gray
                segment_color = Colors.GRAY_300
            
            # Current problem gets border highlight
            if i == current_index:
                # Current problem - with dark border
                segment = ctk.CTkFrame(
                    progress_container,
                    fg_color=segment_color,
                    height=12,
                    corner_radius=4,
                    border_width=2,
                    border_color=Colors.GRAY_800
                )
                segment.place(
                    relx=i * segment_width + gap/2, 
                    rely=0, 
                    relwidth=segment_width - gap, 
                    relheight=1
                )
            else:
                # Regular problem segment
                segment = ctk.CTkFrame(
                    progress_container,
                    fg_color=segment_color,
                    height=10,
                    corner_radius=4
                )
                segment.place(
                    relx=i * segment_width + gap/2, 
                    rely=0.1, 
                    relwidth=segment_width - gap, 
                    relheight=0.83
                )
        
        # Divider
        ctk.CTkFrame(header, fg_color=Colors.BORDER, height=1).pack(fill='x')
        
        # Middle
        mid = ctk.CTkScrollableFrame(parent, fg_color=Colors.BACKGROUND)
        mid.pack(fill='both', expand=True, side='top')
        
        cont = ctk.CTkFrame(mid, fg_color='transparent')
        cont.pack(fill='both', expand=True, padx=Spacing.XXL, pady=Spacing.BASE)
        cont.grid_columnconfigure(0, weight=2)
        cont.grid_columnconfigure(1, weight=3)
        
        # Left
        left = ctk.CTkFrame(cont, fg_color='transparent')
        left.grid(row=0, column=0, sticky='nsew', padx=(0, Spacing.BASE))
        
        # Title row with solved badge
        title_row = ctk.CTkFrame(left, fg_color='transparent')
        title_row.pack(fill='x', pady=(0, Spacing.SM))
        
        ctk.CTkLabel(
            title_row, 
            text=details['name'], 
            font=(Typography.FALLBACK, Typography.H3, 'bold'), 
            text_color=Colors.TEXT_PRIMARY
        ).pack(side='left', anchor='w')
        
        # Solved badge
        if is_solved:
            solved_badge = Badge.create(title_row, "✓ Solved", variant='success')
            solved_badge.pack(side='left', padx=(Spacing.SM, 0))
        
        # Difficulty badge
        if details.get('difficulty'):
            dt, dv = IconHelper.get_difficulty_badge(details['difficulty'])
            Badge.create(left, dt, variant=dv).pack(anchor='w', pady=(0, Spacing.BASE))
        
        ic = Card.create(left)
        ic.pack(fill='x', pady=(0, Spacing.SM))
        ctk.CTkLabel(ic, text="Instructions", font=(Typography.FALLBACK, Typography.H5, 'bold'), text_color=Colors.TEXT_PRIMARY).pack(anchor='w', padx=Spacing.BASE, pady=(Spacing.BASE, Spacing.XS))
        ctk.CTkLabel(ic, text=details['description'], font=(Typography.FALLBACK, Typography.BODY), text_color=Colors.TEXT_SECONDARY, wraplength=340, justify='left').pack(anchor='w', padx=Spacing.BASE, pady=(0, Spacing.BASE))
        
        if details.get('expected_output'):
            oc = Card.create(left)
            oc.pack(fill='x')
            ctk.CTkLabel(oc, text="Expected Output", font=(Typography.FALLBACK, Typography.H5, 'bold'), text_color=Colors.TEXT_PRIMARY).pack(anchor='w', padx=Spacing.BASE, pady=(Spacing.BASE, Spacing.XS))
            ob = ctk.CTkTextbox(oc, height=70, fg_color=Colors.GRAY_100, text_color=Colors.TEXT_PRIMARY, font=(Typography.MONO_FALLBACK, 11), border_width=0)
            ob.pack(fill='x', padx=Spacing.BASE, pady=(0, Spacing.BASE))
            ob.insert('1.0', details['expected_output'])
            ob.configure(state='disabled')
        
        # Right
        right = ctk.CTkFrame(cont, fg_color='transparent')
        right.grid(row=0, column=1, sticky='nsew', padx=(Spacing.BASE, 0))
        
        ctk.CTkLabel(right, text="Your Code", font=(Typography.FALLBACK, Typography.H5, 'bold'), text_color=Colors.TEXT_PRIMARY).pack(anchor='w', pady=(0, Spacing.SM))
        
        editor = ctk.CTkTextbox(right, fg_color=Colors.CODE_BG, text_color=Colors.CODE_TEXT, font=(Typography.MONO_FALLBACK, 13), border_width=1, border_color=Colors.BORDER, corner_radius=Effects.RADIUS_MD, height=280)
        editor.pack(fill='x', pady=(0, Spacing.SM))
        editor.insert('1.0', details.get('starter_code', '# Write your code here\n'))
        
        btns = ctk.CTkFrame(right, fg_color='transparent')
        btns.pack(fill='x', pady=(0, Spacing.SM))
        
        # RESULTS AREA - INSIDE RIGHT PANEL
        res = ctk.CTkFrame(right, fg_color='transparent')
        res.pack(fill='x')
        
        ctk.CTkLabel(res, text="Write code and click Run!", font=(Typography.FALLBACK, Typography.BODY_SMALL), text_color=Colors.TEXT_MUTED).pack(pady=Spacing.SM)
        
        def run():
            from src.core.validator import CodeValidator
            c = editor.get('1.0', 'end-1c')
            if not c.strip() or c.strip() == '# Write your code here':
                for w in res.winfo_children():
                    w.destroy()
                Alert.create(res, "Write code first!", variant='warning').pack()
                return
            for w in res.winfo_children():
                w.destroy()
            l = ctk.CTkLabel(res, text="Running...", font=(Typography.FALLBACK, Typography.BODY), text_color=Colors.TEXT_MUTED)
            l.pack()
            res.update()
            s = manager.get_solution(problem)
            if not s or not s.get('code'):
                l.destroy()
                Alert.create(res, "No solution", variant='danger').pack()
                return
            v = CodeValidator()
            r = v.validate_with_test_cases(c, details, s['code'])
            l.destroy()
            PracticeScreen._show_result(res, r, gamification, details['name'], parent, manager, current_index, on_back, on_progress_update)
        
        def hint():
            # Record hint usage
            if gamification:
                gamification.record_hint_used()
                if on_progress_update:
                    on_progress_update()
            
            for w in res.winfo_children():
                w.destroy()
            Alert.create(res, f"💡 {details.get('hint', 'Try step by step!')}", variant='info').pack()
        
        def sol():
            # Record solution viewed
            if gamification:
                gamification.record_solution_viewed()
                if on_progress_update:
                    on_progress_update()
            
            s = manager.get_solution(problem)
            if not s or not s.get('code'):
                for w in res.winfo_children():
                    w.destroy()
                Alert.create(res, "No solution", variant='danger').pack()
                return
            for w in res.winfo_children():
                w.destroy()
            sc = Card.create(res)
            sc.pack(fill='x')
            ctk.CTkLabel(sc, text="Solution", font=(Typography.FALLBACK, Typography.H5, 'bold'), text_color=Colors.TEXT_PRIMARY).pack(anchor='w', padx=Spacing.BASE, pady=(Spacing.BASE, Spacing.XS))
            CodeDisplay.create(sc, s['code'], height=120).pack(padx=Spacing.BASE, pady=(0, Spacing.BASE))
        
        Button.create(btns, "Run Code", run, variant='success', size='md', width=110).pack(side='left', padx=(0, Spacing.XS))
        Button.create(btns, "Hint", hint, variant='secondary', size='md', width=90).pack(side='left', padx=(0, Spacing.XS))
        Button.create(btns, "Solution", sol, variant='ghost', size='md', width=100).pack(side='left')
        
        # Footer
        foot = ctk.CTkFrame(parent, fg_color=Colors.SURFACE)
        foot.pack(fill='x', side='bottom')
        fc = ctk.CTkFrame(foot, fg_color='transparent')
        fc.pack(fill='x', padx=Spacing.XXL, pady=Spacing.BASE)
        
        if current_index > 0:
            Button.create(fc, f"{Icons.ARROW_LEFT} Previous", lambda: PracticeScreen.create(parent, manager, current_index - 1, on_back, gamification, on_progress_update), variant='secondary', size='md').pack(side='left')
        if current_index < len(problems) - 1:
            Button.create(fc, f"Next {Icons.ARROW_RIGHT}", lambda: PracticeScreen.create(parent, manager, current_index + 1, on_back, gamification, on_progress_update), variant='primary', size='md').pack(side='right')
    
    @staticmethod
    def _show_result(area, result, gam, problem_name, parent, manager, current_index, on_back, on_progress_update=None):
        for w in area.winfo_children():
            w.destroy()
        
        # Main results card
        results_card = Card.create(area)
        results_card.pack(fill='x')
        
        # HORIZONTAL LAYOUT
        content = ctk.CTkFrame(results_card, fg_color='transparent')
        content.pack(fill='x', padx=Spacing.LG, pady=Spacing.LG)
        
        sc = result['score']
        
        # Success or failure state
        if result['valid'] and sc >= 70:
            # SUCCESS STATE
            icon_color = Colors.SUCCESS if sc == 100 else Colors.INFO
            
            # Left: Status icon
            status_frame = ctk.CTkFrame(content, fg_color=icon_color, corner_radius=30, width=50, height=50)
            status_frame.pack(side='left', padx=(0, Spacing.BASE))
            status_frame.pack_propagate(False)
            
            status_icon = ctk.CTkLabel(
                status_frame,
                text="✓",
                font=(Typography.FALLBACK, Typography.H2, 'bold'),
                text_color=Colors.TEXT_INVERSE
            )
            status_icon.pack(expand=True)
            
            # Middle: Score and message
            text_content = ctk.CTkFrame(content, fg_color='transparent')
            text_content.pack(side='left', fill='both', expand=True, padx=(0, Spacing.BASE))
            
            # Score
            ctk.CTkLabel(
                text_content,
                text=f"Score: {sc}%",
                font=(Typography.FALLBACK, Typography.H2, 'bold'),
                text_color=icon_color
            ).pack(anchor='w')
            
            # Message
            msg = "Perfect Solution!" if sc == 100 else "Well Done!"
            ctk.CTkLabel(
                text_content,
                text=msg,
                font=(Typography.FALLBACK, Typography.BODY),
                text_color=Colors.TEXT_SECONDARY
            ).pack(anchor='w')
            
            # Right: XP badge
            if gam:
                xp_result = gam.record_problem_attempt(problem_name, sc, perfect=(sc == 100))
                if xp_result['xp_gained'] > 0:
                    xp_badge = ctk.CTkFrame(
                        content,
                        fg_color=Colors.SUCCESS_SUBTLE,
                        corner_radius=20
                    )
                    xp_badge.pack(side='right')
                    
                    xp_label = ctk.CTkLabel(
                        xp_badge,
                        text=f"+{xp_result['xp_gained']} XP",
                        font=(Typography.FALLBACK, Typography.BODY, 'bold'),
                        text_color=Colors.SUCCESS_DARK
                    )
                    xp_label.pack(padx=Spacing.BASE, pady=Spacing.SM)
                    
                    # NEW: Trigger callback to notify that progress changed
                    if on_progress_update:
                        on_progress_update()
                    
                    # Check for level up and show popup
                    if xp_result.get('leveled_up', False):
                        parent.after(800, lambda: PracticeScreen._show_level_up_popup(
                            parent,
                            xp_result.get('leveled_up_from', xp_result['new_level'] - 1),
                            xp_result['new_level'],
                            gam.current_xp
                        ))
        else:
            # FAILURE STATE
            # Left: Status icon
            status_frame = ctk.CTkFrame(content, fg_color=Colors.DANGER, corner_radius=30, width=50, height=50)
            status_frame.pack(side='left', padx=(0, Spacing.BASE))
            status_frame.pack_propagate(False)
            
            status_icon = ctk.CTkLabel(
                status_frame,
                text="✕",
                font=(Typography.FALLBACK, Typography.H2, 'bold'),
                text_color=Colors.TEXT_INVERSE
            )
            status_icon.pack(expand=True)
            
            # Middle: Score and error
            text_content = ctk.CTkFrame(content, fg_color='transparent')
            text_content.pack(side='left', fill='both', expand=True)
            
            # Score
            ctk.CTkLabel(
                text_content,
                text=f"Score: {sc}%",
                font=(Typography.FALLBACK, Typography.H2, 'bold'),
                text_color=Colors.DANGER
            ).pack(anchor='w')
            
            # Error message
            if result['errors']:
                error_text = result['errors'][0]
                if len(error_text) > 60:
                    error_text = error_text[:60] + "..."
                
                ctk.CTkLabel(
                    text_content,
                    text=f"Error: {error_text}",
                    font=(Typography.FALLBACK, Typography.BODY_SMALL),
                    text_color=Colors.DANGER,
                    wraplength=400,
                    justify='left'
                ).pack(anchor='w')
            else:
                ctk.CTkLabel(
                    text_content,
                    text="Try Again",
                    font=(Typography.FALLBACK, Typography.BODY),
                    text_color=Colors.TEXT_SECONDARY
                ).pack(anchor='w')
            
            # CRITICAL: Record failed attempt - THIS IS THE FIX!
            if gam:
                gam.record_problem_attempt(problem_name, sc, perfect=False)
                if on_progress_update:
                    on_progress_update()
    
    @staticmethod
    def _show_level_up_popup(parent, old_level, new_level, current_xp):
        """Show level up celebration popup"""
        # Overlay background (semi-transparent)
        overlay = ctk.CTkFrame(
            parent,
            fg_color=("gray80", "gray20"),
            bg_color='transparent'
        )
        overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        # Make overlay semi-transparent by binding click to close
        overlay.bind('<Button-1>', lambda e: overlay.destroy())
        
        # Popup card (centered)
        popup = ctk.CTkFrame(
            overlay,
            fg_color=Colors.SURFACE,
            corner_radius=Effects.RADIUS_XL,
            width=400,
            height=300,
            border_width=2,
            border_color=Colors.PRIMARY
        )
        popup.place(relx=0.5, rely=0.5, anchor='center')
        
        # Content container
        content = ctk.CTkFrame(popup, fg_color='transparent')
        content.pack(fill='both', expand=True, padx=Spacing.XXL, pady=Spacing.XXL)
        
        # Celebration icon
        icon_frame = ctk.CTkFrame(
            content,
            fg_color=Colors.PRIMARY,
            corner_radius=50,
            width=80,
            height=80
        )
        icon_frame.pack(pady=(0, Spacing.BASE))
        icon_frame.pack_propagate(False)
        
        icon_label = ctk.CTkLabel(
            icon_frame,
            text=Icons.STAR,
            font=(Typography.FALLBACK, Typography.DISPLAY, 'bold'),
            text_color=Colors.TEXT_INVERSE
        )
        icon_label.pack(expand=True)
        
        # "Level Up!" text
        ctk.CTkLabel(
            content,
            text="Level Up!",
            font=(Typography.FALLBACK, Typography.H1, 'bold'),
            text_color=Colors.PRIMARY
        ).pack(pady=(0, Spacing.XS))
        
        # Level progress
        level_text = ctk.CTkLabel(
            content,
            text=f"Level {old_level} {Icons.ARROW_RIGHT} Level {new_level}",
            font=(Typography.FALLBACK, Typography.H3),
            text_color=Colors.TEXT_PRIMARY
        )
        level_text.pack(pady=(0, Spacing.BASE))
        
        # Congratulations message
        ctk.CTkLabel(
            content,
            text="Congratulations! Keep up the great work!",
            font=(Typography.FALLBACK, Typography.BODY),
            text_color=Colors.TEXT_SECONDARY,
            wraplength=300
        ).pack(pady=(0, Spacing.LG))
        
        # XP display
        xp_frame = ctk.CTkFrame(
            content,
            fg_color=Colors.PRIMARY_SUBTLE,
            corner_radius=8
        )
        xp_frame.pack(fill='x', pady=(0, Spacing.LG))
        
        ctk.CTkLabel(
            xp_frame,
            text=f"Current XP: {current_xp}",
            font=(Typography.FALLBACK, Typography.BODY, 'bold'),
            text_color=Colors.PRIMARY_DARK
        ).pack(pady=Spacing.SM)
        
        # Continue button
        continue_btn = Button.create(
            content,
            "Continue",
            lambda: overlay.destroy(),
            variant='primary',
            size='md'
        )
        continue_btn.pack()