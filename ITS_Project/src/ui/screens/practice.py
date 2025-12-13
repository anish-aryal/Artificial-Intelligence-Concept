"""
Practice Screen - Code editor with validation
Optimized modern design with compact layout
"""

import customtkinter as ctk
from src.ui.components import Button, Card, Badge, CodeDisplay, Alert
from src.ui.styles import Colors, Typography, Spacing, Effects
from src.ui.icons import Icons, IconHelper


class PracticeScreen:
    """Practice screen - compact modern design"""
    
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
        solved_count = 0
        if gamification:
            solved_count = len(gamification.solved_problems)
            is_solved = details['name'] in gamification.solved_problems
        
        # ============================================
        # COMPACT HEADER
        # ============================================
        header = ctk.CTkFrame(parent, fg_color=Colors.SURFACE, height=50)
        header.pack(fill='x', side='top')
        header.pack_propagate(False)
        
        header_content = ctk.CTkFrame(header, fg_color='transparent')
        header_content.pack(fill='both', expand=True, padx=Spacing.LG, pady=Spacing.SM)
        
        # Left: Back + Problem info
        left_header = ctk.CTkFrame(header_content, fg_color='transparent')
        left_header.pack(side='left', fill='y')
        
        if on_back:
            back_btn = ctk.CTkButton(
                left_header,
                text="←",
                command=on_back,
                width=32,
                height=32,
                fg_color='transparent',
                hover_color=Colors.GRAY_100,
                text_color=Colors.TEXT_PRIMARY,
                font=(Typography.FALLBACK, 16)
            )
            back_btn.pack(side='left', padx=(0, Spacing.SM))
        
        ctk.CTkLabel(
            left_header,
            text=f"Problem {current_index + 1}/{len(problems)}",
            font=(Typography.FALLBACK, Typography.BODY, 'bold'),
            text_color=Colors.TEXT_PRIMARY
        ).pack(side='left')
        
        # Difficulty badge (compact)
        if details.get('difficulty'):
            dt, dv = IconHelper.get_difficulty_badge(details['difficulty'])
            diff_colors = {'success': Colors.SUCCESS, 'warning': Colors.WARNING, 'danger': Colors.DANGER}
            ctk.CTkLabel(
                left_header,
                text=f"• {dt}",
                font=(Typography.FALLBACK, Typography.CAPTION, 'bold'),
                text_color=diff_colors.get(dv, Colors.TEXT_MUTED)
            ).pack(side='left', padx=(Spacing.SM, 0))
        
        # Center: Compact progress bar
        center_header = ctk.CTkFrame(header_content, fg_color='transparent')
        center_header.pack(side='left', expand=True, fill='x', padx=Spacing.XL)
        
        progress_bar = ctk.CTkFrame(center_header, fg_color=Colors.GRAY_200, height=6, corner_radius=3)
        progress_bar.pack(fill='x', pady=Spacing.SM)
        
        # Draw segments inside progress bar
        for i in range(len(problems)):
            prob = problems[i]
            prob_details = manager.get_problem_details(prob)
            is_prob_solved = prob_details['name'] in gamification.solved_problems if gamification else False
            
            if is_prob_solved:
                color = Colors.SUCCESS
            elif i == current_index:
                color = Colors.PRIMARY
            elif i < current_index:
                color = Colors.PRIMARY_LIGHT
            else:
                color = Colors.GRAY_300
            
            segment_width = 1.0 / len(problems)
            segment = ctk.CTkFrame(progress_bar, fg_color=color, corner_radius=3)
            segment.place(relx=i * segment_width + 0.005, rely=0.1, relwidth=segment_width - 0.01, relheight=0.8)
        
        # Right: Solved count
        right_header = ctk.CTkFrame(header_content, fg_color='transparent')
        right_header.pack(side='right', fill='y')
        
        solved_color = Colors.SUCCESS if solved_count > 0 else Colors.GRAY_400
        ctk.CTkLabel(
            right_header,
            text=f"✓ {solved_count}/{len(problems)}",
            font=(Typography.FALLBACK, Typography.BODY_SMALL, 'bold'),
            text_color=solved_color
        ).pack(side='right')
        
        # ============================================
        # MAIN CONTENT - TWO COLUMNS
        # ============================================
        main = ctk.CTkFrame(parent, fg_color=Colors.BACKGROUND)
        main.pack(fill='both', expand=True, side='top')
        
        content = ctk.CTkFrame(main, fg_color='transparent')
        content.pack(fill='both', expand=True, padx=Spacing.LG, pady=Spacing.SM)
        content.grid_columnconfigure(0, weight=1, minsize=280)
        content.grid_columnconfigure(1, weight=2, minsize=450)
        content.grid_rowconfigure(0, weight=1)
        
        # ============================================
        # LEFT COLUMN - Problem Info (Scrollable)
        # ============================================
        left_col = ctk.CTkScrollableFrame(content, fg_color='transparent', width=280)
        left_col.grid(row=0, column=0, sticky='nsew', padx=(0, Spacing.SM))
        
        # Problem title with solved badge
        title_frame = ctk.CTkFrame(left_col, fg_color='transparent')
        title_frame.pack(fill='x', pady=(0, Spacing.XS))
        
        ctk.CTkLabel(
            title_frame,
            text=details['name'],
            font=(Typography.FALLBACK, Typography.H5, 'bold'),
            text_color=Colors.TEXT_PRIMARY
        ).pack(side='left')
        
        if is_solved:
            ctk.CTkLabel(
                title_frame,
                text="✓",
                font=(Typography.FALLBACK, Typography.BODY, 'bold'),
                text_color=Colors.SUCCESS
            ).pack(side='left', padx=(Spacing.XS, 0))
        
        # Instructions (compact card)
        inst_card = ctk.CTkFrame(left_col, fg_color=Colors.SURFACE, corner_radius=Effects.RADIUS_MD)
        inst_card.pack(fill='x', pady=(0, Spacing.XS))
        
        inst_content = ctk.CTkFrame(inst_card, fg_color='transparent')
        inst_content.pack(fill='x', padx=Spacing.SM, pady=Spacing.SM)
        
        ctk.CTkLabel(
            inst_content,
            text="Instructions",
            font=(Typography.FALLBACK, Typography.CAPTION, 'bold'),
            text_color=Colors.TEXT_MUTED
        ).pack(anchor='w')
        
        ctk.CTkLabel(
            inst_content,
            text=details['description'],
            font=(Typography.FALLBACK, Typography.BODY_SMALL),
            text_color=Colors.TEXT_SECONDARY,
            wraplength=250,
            justify='left'
        ).pack(anchor='w', pady=(Spacing.XXS, 0))
        
        # Expected Output (compact)
        if details.get('expected_output'):
            out_card = ctk.CTkFrame(left_col, fg_color=Colors.SURFACE, corner_radius=Effects.RADIUS_MD)
            out_card.pack(fill='x', pady=(0, Spacing.XS))
            
            out_content = ctk.CTkFrame(out_card, fg_color='transparent')
            out_content.pack(fill='x', padx=Spacing.SM, pady=Spacing.SM)
            
            ctk.CTkLabel(
                out_content,
                text="Expected Output",
                font=(Typography.FALLBACK, Typography.CAPTION, 'bold'),
                text_color=Colors.TEXT_MUTED
            ).pack(anchor='w')
            
            out_box = ctk.CTkTextbox(
                out_content,
                height=50,
                fg_color=Colors.GRAY_100,
                text_color=Colors.TEXT_PRIMARY,
                font=(Typography.MONO_FALLBACK, 11),
                border_width=0,
                corner_radius=4
            )
            out_box.pack(fill='x', pady=(Spacing.XXS, 0))
            out_box.insert('1.0', details['expected_output'])
            out_box.configure(state='disabled')
        
        # ============================================
        # COMMON MISTAKES SECTION (Left Column)
        # ============================================
        ontology_mistakes = manager.get_common_mistakes(problem)
        
        if ontology_mistakes:
            mistakes_card = ctk.CTkFrame(left_col, fg_color=Colors.WARNING_SUBTLE, corner_radius=Effects.RADIUS_MD)
            mistakes_card.pack(fill='x', pady=(0, Spacing.XS))
            
            mistakes_content = ctk.CTkFrame(mistakes_card, fg_color='transparent')
            mistakes_content.pack(fill='x', padx=Spacing.SM, pady=Spacing.SM)
            
            # Header
            mistakes_header = ctk.CTkFrame(mistakes_content, fg_color='transparent')
            mistakes_header.pack(fill='x', pady=(0, Spacing.XXS))
            
            ctk.CTkLabel(
                mistakes_header,
                text="💡",
                font=(Typography.FALLBACK, Typography.BODY_SMALL),
                text_color=Colors.WARNING
            ).pack(side='left')
            
            ctk.CTkLabel(
                mistakes_header,
                text="Common Mistakes",
                font=(Typography.FALLBACK, Typography.CAPTION, 'bold'),
                text_color=Colors.WARNING
            ).pack(side='left', padx=(Spacing.XXS, 0))
            
            # Mistakes list (show up to 3)
            for i, mistake in enumerate(ontology_mistakes[:3]):
                msg = mistake.get('message', '')
                if len(msg) > 100:
                    msg = msg[:100] + "..."
                
                ctk.CTkLabel(
                    mistakes_content,
                    text=f"• {msg}",
                    font=(Typography.FALLBACK, Typography.CAPTION),
                    text_color=Colors.TEXT_SECONDARY,
                    wraplength=240,
                    justify='left'
                ).pack(anchor='w', pady=(Spacing.XXS, 0))
        
        # ============================================
        # RIGHT COLUMN - Code Editor & Results
        # ============================================
        right_col = ctk.CTkFrame(content, fg_color='transparent')
        right_col.grid(row=0, column=1, sticky='nsew', padx=(Spacing.SM, 0))
        right_col.grid_rowconfigure(1, weight=0)  # Editor - fixed
        right_col.grid_rowconfigure(2, weight=1)  # Results - expandable
        right_col.grid_columnconfigure(0, weight=1)
        
        # Code editor header
        editor_header = ctk.CTkFrame(right_col, fg_color='transparent')
        editor_header.grid(row=0, column=0, sticky='ew', pady=(0, Spacing.XS))
        
        ctk.CTkLabel(
            editor_header,
            text="Your Code",
            font=(Typography.FALLBACK, Typography.BODY_SMALL, 'bold'),
            text_color=Colors.TEXT_PRIMARY
        ).pack(side='left')
        
        # Action buttons (in header)
        btn_frame = ctk.CTkFrame(editor_header, fg_color='transparent')
        btn_frame.pack(side='right')
        
        # Code editor
        editor = ctk.CTkTextbox(
            right_col,
            fg_color=Colors.CODE_BG,
            text_color=Colors.CODE_TEXT,
            font=(Typography.MONO_FALLBACK, 13),
            border_width=1,
            border_color=Colors.BORDER,
            corner_radius=Effects.RADIUS_MD,
            height=180
        )
        editor.grid(row=1, column=0, sticky='ew', pady=(0, Spacing.XS))
        editor.insert('1.0', details.get('starter_code', '# Write your code here\n'))
        
        # Results area - SCROLLABLE FRAME
        results_container = ctk.CTkFrame(right_col, fg_color=Colors.SURFACE, corner_radius=Effects.RADIUS_MD)
        results_container.grid(row=2, column=0, sticky='nsew')
        
        results_area = ctk.CTkScrollableFrame(results_container, fg_color='transparent')
        results_area.pack(fill='both', expand=True, padx=Spacing.XS, pady=Spacing.XS)
        
        # Initial message
        ctk.CTkLabel(
            results_area,
            text="Write code and click Run →",
            font=(Typography.FALLBACK, Typography.BODY_SMALL),
            text_color=Colors.TEXT_MUTED
        ).pack(pady=Spacing.LG)
        
        # Button handlers
        def run_code():
            from src.core.validator import CodeValidator
            code = editor.get('1.0', 'end-1c')
            
            if not code.strip() or code.strip() == '# Write your code here':
                PracticeScreen._show_message(results_area, "Write some code first!", "warning")
                return
            
            PracticeScreen._show_message(results_area, "Running...", "info")
            results_area.update()
            
            solution = manager.get_solution(problem)
            if not solution or not solution.get('code'):
                PracticeScreen._show_message(results_area, "No solution available", "danger")
                return
            
            validator = CodeValidator()
            result = validator.validate_with_test_cases(code, details, solution['code'])
            
            PracticeScreen._show_result(
                results_area, result, gamification, details['name'],
                parent, manager, current_index, on_back, on_progress_update
            )
        
        def show_hint():
            if gamification:
                gamification.record_hint_used()
                if on_progress_update:
                    on_progress_update()
            PracticeScreen._show_message(results_area, f"💡 {details.get('hint', 'Break it into smaller steps!')}", "info")
        
        def show_solution():
            if gamification:
                gamification.record_solution_viewed()
                if on_progress_update:
                    on_progress_update()
            
            solution = manager.get_solution(problem)
            if solution and solution.get('code'):
                PracticeScreen._show_solution(results_area, solution['code'])
            else:
                PracticeScreen._show_message(results_area, "No solution available", "danger")
        
        # Buttons
        run_btn = ctk.CTkButton(
            btn_frame, text="▶ Run", command=run_code,
            width=70, height=28, corner_radius=6,
            fg_color=Colors.SUCCESS, hover_color=Colors.SUCCESS_DARK,
            font=(Typography.FALLBACK, Typography.CAPTION, 'bold')
        )
        run_btn.pack(side='left', padx=(0, Spacing.XS))
        
        hint_btn = ctk.CTkButton(
            btn_frame, text="Hint", command=show_hint,
            width=50, height=28, corner_radius=6,
            fg_color=Colors.GRAY_200, hover_color=Colors.GRAY_300,
            text_color=Colors.TEXT_PRIMARY,
            font=(Typography.FALLBACK, Typography.CAPTION)
        )
        hint_btn.pack(side='left', padx=(0, Spacing.XS))
        
        sol_btn = ctk.CTkButton(
            btn_frame, text="Solution", command=show_solution,
            width=65, height=28, corner_radius=6,
            fg_color='transparent', hover_color=Colors.GRAY_100,
            text_color=Colors.TEXT_SECONDARY,
            font=(Typography.FALLBACK, Typography.CAPTION)
        )
        sol_btn.pack(side='left')
        
        # ============================================
        # FOOTER - Navigation
        # ============================================
        footer = ctk.CTkFrame(parent, fg_color=Colors.SURFACE, height=50)
        footer.pack(fill='x', side='bottom')
        footer.pack_propagate(False)
        
        footer_content = ctk.CTkFrame(footer, fg_color='transparent')
        footer_content.pack(fill='both', expand=True, padx=Spacing.LG, pady=Spacing.SM)
        
        if current_index > 0:
            ctk.CTkButton(
                footer_content, text="← Previous",
                command=lambda: PracticeScreen.create(parent, manager, current_index - 1, on_back, gamification, on_progress_update),
                width=90, height=32, corner_radius=6,
                fg_color=Colors.GRAY_200, hover_color=Colors.GRAY_300,
                text_color=Colors.TEXT_PRIMARY,
                font=(Typography.FALLBACK, Typography.BODY_SMALL)
            ).pack(side='left')
        
        if current_index < len(problems) - 1:
            ctk.CTkButton(
                footer_content, text="Next →",
                command=lambda: PracticeScreen.create(parent, manager, current_index + 1, on_back, gamification, on_progress_update),
                width=80, height=32, corner_radius=6,
                fg_color=Colors.PRIMARY, hover_color=Colors.PRIMARY_DARK,
                font=(Typography.FALLBACK, Typography.BODY_SMALL)
            ).pack(side='right')
    
    @staticmethod
    def _show_message(area, message, variant='info'):
        """Show a simple message"""
        for w in area.winfo_children():
            w.destroy()
        
        colors = {
            'info': (Colors.INFO_SUBTLE, Colors.INFO),
            'warning': (Colors.WARNING_SUBTLE, Colors.WARNING),
            'danger': (Colors.DANGER_SUBTLE, Colors.DANGER),
            'success': (Colors.SUCCESS_SUBTLE, Colors.SUCCESS)
        }
        bg, fg = colors.get(variant, colors['info'])
        
        msg_frame = ctk.CTkFrame(area, fg_color=bg, corner_radius=8)
        msg_frame.pack(fill='x', pady=Spacing.SM)
        
        ctk.CTkLabel(
            msg_frame, text=message,
            font=(Typography.FALLBACK, Typography.BODY_SMALL),
            text_color=fg, wraplength=400
        ).pack(padx=Spacing.BASE, pady=Spacing.SM)
    
    @staticmethod
    def _show_solution(area, code):
        """Show solution code"""
        for w in area.winfo_children():
            w.destroy()
        
        sol_frame = ctk.CTkFrame(area, fg_color=Colors.GRAY_50, corner_radius=8)
        sol_frame.pack(fill='x', pady=Spacing.SM)
        
        ctk.CTkLabel(
            sol_frame, text="Solution",
            font=(Typography.FALLBACK, Typography.CAPTION, 'bold'),
            text_color=Colors.TEXT_MUTED
        ).pack(anchor='w', padx=Spacing.SM, pady=(Spacing.SM, Spacing.XXS))
        
        code_box = ctk.CTkTextbox(
            sol_frame, height=100,
            fg_color=Colors.CODE_BG, text_color=Colors.CODE_TEXT,
            font=(Typography.MONO_FALLBACK, 12),
            corner_radius=4
        )
        code_box.pack(fill='x', padx=Spacing.SM, pady=(0, Spacing.SM))
        code_box.insert('1.0', code)
        code_box.configure(state='disabled')
    
    @staticmethod
    def _show_result(area, result, gam, problem_name, parent, manager, current_index, on_back, on_progress_update=None):
        """Show results with detailed test case information"""
        for w in area.winfo_children():
            w.destroy()
        
        score = result['score']
        is_success = result['valid'] and score >= 70
        
        # ============================================
        # SCORE BANNER
        # ============================================
        banner_color = Colors.SUCCESS if score == 100 else (Colors.INFO if is_success else Colors.DANGER)
        banner_bg = Colors.SUCCESS_SUBTLE if score == 100 else (Colors.INFO_SUBTLE if is_success else Colors.DANGER_SUBTLE)
        
        banner = ctk.CTkFrame(area, fg_color=banner_bg, corner_radius=8)
        banner.pack(fill='x', pady=(0, Spacing.SM))
        
        banner_content = ctk.CTkFrame(banner, fg_color='transparent')
        banner_content.pack(fill='x', padx=Spacing.SM, pady=Spacing.SM)
        
        # Left: Icon + Score
        left_banner = ctk.CTkFrame(banner_content, fg_color='transparent')
        left_banner.pack(side='left')
        
        icon = "✓" if is_success else "✕"
        ctk.CTkLabel(
            left_banner, text=icon,
            font=(Typography.FALLBACK, Typography.H4, 'bold'),
            text_color=banner_color
        ).pack(side='left', padx=(0, Spacing.XS))
        
        ctk.CTkLabel(
            left_banner, text=f"{score}%",
            font=(Typography.FALLBACK, Typography.H4, 'bold'),
            text_color=banner_color
        ).pack(side='left')
        
        msg = "Perfect!" if score == 100 else ("Passed!" if is_success else "Try Again")
        ctk.CTkLabel(
            left_banner, text=msg,
            font=(Typography.FALLBACK, Typography.BODY_SMALL),
            text_color=Colors.TEXT_SECONDARY
        ).pack(side='left', padx=(Spacing.SM, 0))
        
        # Right: XP badge
        if is_success and gam:
            xp_result = gam.record_problem_attempt(problem_name, score, perfect=(score == 100))
            if xp_result['xp_gained'] > 0:
                xp_badge = ctk.CTkFrame(banner_content, fg_color=Colors.SUCCESS, corner_radius=12)
                xp_badge.pack(side='right')
                
                ctk.CTkLabel(
                    xp_badge, text=f"+{xp_result['xp_gained']} XP",
                    font=(Typography.FALLBACK, Typography.CAPTION, 'bold'),
                    text_color=Colors.TEXT_INVERSE
                ).pack(padx=Spacing.SM, pady=Spacing.XXS)
                
                if on_progress_update:
                    on_progress_update()
                
                if xp_result.get('leveled_up', False):
                    parent.after(800, lambda: PracticeScreen._show_level_up_popup(
                        parent, xp_result.get('leveled_up_from', 1),
                        xp_result['new_level'], gam.current_xp
                    ))
        elif not is_success and gam:
            gam.record_problem_attempt(problem_name, score, perfect=False)
            if on_progress_update:
                on_progress_update()
        
        # ============================================
        # TEST RESULTS - DETAILED VIEW
        # ============================================
        if result.get('results'):
            # Header
            passed = result.get('tests_passed', 0)
            total = result.get('tests_total', 0)
            header_color = Colors.SUCCESS if passed == total else (Colors.WARNING if passed > 0 else Colors.DANGER)
            
            ctk.CTkLabel(
                area,
                text=f"Test Results: {passed}/{total} passed",
                font=(Typography.FALLBACK, Typography.BODY_SMALL, 'bold'),
                text_color=header_color
            ).pack(anchor='w', pady=(0, Spacing.XS))
            
            # Individual test results
            for test_res in result['results']:
                is_passed = test_res['passed']
                
                test_row = ctk.CTkFrame(
                    area,
                    fg_color=Colors.SUCCESS_SUBTLE if is_passed else Colors.DANGER_SUBTLE,
                    corner_radius=6
                )
                test_row.pack(fill='x', pady=(0, Spacing.XS))
                
                test_row_content = ctk.CTkFrame(test_row, fg_color='transparent')
                test_row_content.pack(fill='x', padx=Spacing.SM, pady=Spacing.SM)
                
                # Status + Description
                status_icon = "✓" if is_passed else "✕"
                status_color = Colors.SUCCESS if is_passed else Colors.DANGER
                
                test_header = ctk.CTkFrame(test_row_content, fg_color='transparent')
                test_header.pack(fill='x')
                
                ctk.CTkLabel(
                    test_header, text=status_icon,
                    font=(Typography.FALLBACK, Typography.BODY_SMALL, 'bold'),
                    text_color=status_color, width=16
                ).pack(side='left')
                
                ctk.CTkLabel(
                    test_header,
                    text=test_res.get('description', f"Test {test_res.get('test_number', '?')}"),
                    font=(Typography.FALLBACK, Typography.BODY_SMALL, 'bold'),
                    text_color=Colors.TEXT_PRIMARY
                ).pack(side='left', padx=(Spacing.XXS, 0))
                
                # Details frame
                details_frame = ctk.CTkFrame(test_row_content, fg_color='transparent')
                details_frame.pack(fill='x', padx=(Spacing.LG, 0), pady=(Spacing.XS, 0))
                
                # Get expected and actual from the test result OR from solution output
                expected_raw = test_res.get('expected', '') or test_res.get('solution_output', '')
                actual_raw = test_res.get('actual', '')
                
                # Format for display (replace newlines with visible separator)
                expected_display = expected_raw.replace('\n', ' , ') if expected_raw else "(no output)"
                actual_display = actual_raw.replace('\n', ' , ') if actual_raw else "(no output)"
                
                # Truncate if too long
                if len(expected_display) > 50:
                    expected_display = expected_display[:50] + "..."
                if len(actual_display) > 50:
                    actual_display = actual_display[:50] + "..."
                
                # Expected row
                expected_row = ctk.CTkFrame(details_frame, fg_color='transparent')
                expected_row.pack(fill='x')
                
                ctk.CTkLabel(
                    expected_row, text="Expected:",
                    font=(Typography.FALLBACK, Typography.CAPTION, 'bold'),
                    text_color=Colors.TEXT_MUTED, width=60, anchor='w'
                ).pack(side='left')
                
                ctk.CTkLabel(
                    expected_row, text=expected_display,
                    font=(Typography.MONO_FALLBACK, 11),
                    text_color=Colors.TEXT_SECONDARY
                ).pack(side='left', padx=(Spacing.XS, 0))
                
                # Got row
                actual_row = ctk.CTkFrame(details_frame, fg_color='transparent')
                actual_row.pack(fill='x', pady=(Spacing.XXS, 0))
                
                ctk.CTkLabel(
                    actual_row, text="Got:",
                    font=(Typography.FALLBACK, Typography.CAPTION, 'bold'),
                    text_color=Colors.TEXT_MUTED, width=60, anchor='w'
                ).pack(side='left')
                
                ctk.CTkLabel(
                    actual_row, text=actual_display,
                    font=(Typography.MONO_FALLBACK, 11),
                    text_color=Colors.SUCCESS_DARK if is_passed else Colors.DANGER
                ).pack(side='left', padx=(Spacing.XS, 0))
                
                # Error row (if any)
                if test_res.get('error'):
                    error_row = ctk.CTkFrame(details_frame, fg_color='transparent')
                    error_row.pack(fill='x', pady=(Spacing.XXS, 0))
                    
                    error_msg = test_res['error']
                    if len(error_msg) > 50:
                        error_msg = error_msg[:50] + "..."
                    
                    ctk.CTkLabel(
                        error_row, text="Error:",
                        font=(Typography.FALLBACK, Typography.CAPTION, 'bold'),
                        text_color=Colors.DANGER, width=60, anchor='w'
                    ).pack(side='left')
                    
                    ctk.CTkLabel(
                        error_row, text=error_msg,
                        font=(Typography.MONO_FALLBACK, 11),
                        text_color=Colors.DANGER
                    ).pack(side='left', padx=(Spacing.XS, 0))
        
        # ============================================
        # DETECTED MISTAKES (from validator)
        # ============================================
        detected = result.get('detected_mistakes', [])
        if detected and not is_success:
            detect_frame = ctk.CTkFrame(area, fg_color=Colors.INFO_SUBTLE, corner_radius=8)
            detect_frame.pack(fill='x', pady=(Spacing.XS, 0))
            
            detect_content = ctk.CTkFrame(detect_frame, fg_color='transparent')
            detect_content.pack(fill='x', padx=Spacing.SM, pady=Spacing.SM)
            
            detect_header = ctk.CTkFrame(detect_content, fg_color='transparent')
            detect_header.pack(fill='x', pady=(0, Spacing.XXS))
            
            ctk.CTkLabel(
                detect_header, text="⚠",
                font=(Typography.FALLBACK, Typography.BODY_SMALL),
                text_color=Colors.INFO
            ).pack(side='left')
            
            ctk.CTkLabel(
                detect_header, text="Issues Detected",
                font=(Typography.FALLBACK, Typography.CAPTION, 'bold'),
                text_color=Colors.INFO
            ).pack(side='left', padx=(Spacing.XXS, 0))
            
            for mistake in detected[:2]:
                msg = mistake.get('message', '')
                if len(msg) > 100:
                    msg = msg[:100] + "..."
                
                ctk.CTkLabel(
                    detect_content, text=f"• {msg}",
                    font=(Typography.FALLBACK, Typography.CAPTION),
                    text_color=Colors.TEXT_SECONDARY,
                    wraplength=350, justify='left'
                ).pack(anchor='w', pady=(Spacing.XXS, 0))
    
    @staticmethod
    def _show_level_up_popup(parent, old_level, new_level, current_xp):
        """Show compact level up popup"""
        overlay = ctk.CTkFrame(parent, fg_color=("gray90", "gray10"))
        overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        overlay.bind('<Button-1>', lambda e: overlay.destroy())
        
        popup = ctk.CTkFrame(
            overlay, fg_color=Colors.SURFACE,
            corner_radius=16, width=320, height=220,
            border_width=2, border_color=Colors.PRIMARY
        )
        popup.place(relx=0.5, rely=0.5, anchor='center')
        popup.pack_propagate(False)
        
        content = ctk.CTkFrame(popup, fg_color='transparent')
        content.pack(fill='both', expand=True, padx=Spacing.LG, pady=Spacing.LG)
        
        ctk.CTkLabel(
            content, text="⭐",
            font=(Typography.FALLBACK, 48),
            text_color=Colors.PRIMARY
        ).pack(pady=(0, Spacing.XS))
        
        ctk.CTkLabel(
            content, text="Level Up!",
            font=(Typography.FALLBACK, Typography.H3, 'bold'),
            text_color=Colors.PRIMARY
        ).pack()
        
        ctk.CTkLabel(
            content, text=f"Level {old_level} → Level {new_level}",
            font=(Typography.FALLBACK, Typography.BODY),
            text_color=Colors.TEXT_PRIMARY
        ).pack(pady=(Spacing.XS, Spacing.BASE))
        
        ctk.CTkButton(
            content, text="Continue",
            command=overlay.destroy,
            width=100, height=32,
            fg_color=Colors.PRIMARY,
            corner_radius=8
        ).pack()