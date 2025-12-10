"""
Modern Screen Designs - Professional & Clean
"""

import customtkinter as ctk
from src.ui.components import (
    Button, Card, Badge, ProgressBar, CodeDisplay, 
    Alert, LevelIndicator
)
from src.ui.styles import Colors, Typography, Spacing, Layout, Effects
from src.ui.icons import Icons, IconHelper, UIText


class DashboardScreen:
    """Modern Dashboard"""
    
    @staticmethod
    def create(parent, manager, user_data, callbacks):
        """Create dashboard screen"""
        for widget in parent.winfo_children():
            widget.destroy()
        
        scroll = ctk.CTkScrollableFrame(parent, fg_color=Colors.BACKGROUND)
        scroll.pack(fill='both', expand=True, padx=Spacing.GIANT, pady=Spacing.XXL)
        
        header = ctk.CTkFrame(scroll, fg_color='transparent')
        header.pack(fill='x', pady=(0, Spacing.XXXL))
        
        welcome = ctk.CTkLabel(
            header,
            text="Welcome back!",
            font=(Typography.FALLBACK, Typography.H1, 'bold'),
            text_color=Colors.TEXT_PRIMARY
        )
        welcome.pack(anchor='w')
        
        subtitle = ctk.CTkLabel(
            header,
            text="Continue your Python iteration journey",
            font=(Typography.FALLBACK, Typography.BODY_LARGE),
            text_color=Colors.TEXT_SECONDARY
        )
        subtitle.pack(anchor='w', pady=(Spacing.XS, 0))
        
        level_card = Card.create(scroll)
        level_card.pack(fill='x', pady=(0, Spacing.XXL))
        
        LevelIndicator.create(
            level_card,
            level=user_data.get('level', 1),
            current_xp=user_data.get('xp', 0),
            xp_for_next=user_data.get('xp_for_next', 500)
        ).pack(padx=Spacing.LG, pady=Spacing.LG)
        
        stats_row = ctk.CTkFrame(scroll, fg_color='transparent')
        stats_row.pack(fill='x', pady=(0, Spacing.XXL))
        
        stats = manager.get_statistics()
        
        stat_configs = [
            {
                'value': stats['concepts'],
                'label': 'Learning Topics',
                'sublabel': 'Core concepts to master',
                'color': Colors.PRIMARY,
                'action': ('Start Learning', callbacks['on_learn'])
            },
            {
                'value': stats['problems'],
                'label': 'Practice Problems',
                'sublabel': 'Coding exercises',
                'color': Colors.SUCCESS,
                'action': ('Practice Now', callbacks['on_practice'])
            },
            {
                'value': user_data.get('problems_solved', 0),
                'label': 'Problems Solved',
                'sublabel': f"of {stats['problems']} completed",
                'color': Colors.INFO,
                'action': None
            }
        ]
        
        for config in stat_configs:
            stat_card = Card.create(stats_row, hover=True)
            stat_card.pack(side='left', padx=Spacing.SM, expand=True, fill='both')
            
            value_label = ctk.CTkLabel(
                stat_card,
                text=str(config['value']),
                font=(Typography.FALLBACK, Typography.DISPLAY, 'bold'),
                text_color=config['color']
            )
            value_label.pack(pady=(Spacing.XXL, Spacing.XS))
            
            label = ctk.CTkLabel(
                stat_card,
                text=config['label'],
                font=(Typography.FALLBACK, Typography.H5, 'bold'),
                text_color=Colors.TEXT_PRIMARY
            )
            label.pack()
            
            sublabel = ctk.CTkLabel(
                stat_card,
                text=config['sublabel'],
                font=(Typography.FALLBACK, Typography.BODY_SMALL),
                text_color=Colors.TEXT_MUTED
            )
            sublabel.pack(pady=(Spacing.XXS, Spacing.BASE))
            
            if config['action']:
                btn_text, btn_cmd = config['action']
                Button.create(
                    stat_card,
                    btn_text,
                    btn_cmd,
                    variant='ghost',
                    size='sm'
                ).pack(pady=(0, Spacing.LG))
        
        continue_section = ctk.CTkFrame(scroll, fg_color='transparent')
        continue_section.pack(fill='x', pady=(0, Spacing.XXL))
        
        section_header = ctk.CTkLabel(
            continue_section,
            text=UIText.CONTINUE_LEARNING,
            font=(Typography.FALLBACK, Typography.H3, 'bold'),
            text_color=Colors.TEXT_PRIMARY
        )
        section_header.pack(anchor='w', pady=(0, Spacing.BASE))
        
        concepts = manager.get_concepts()
        if concepts:
            concept = concepts[0]
            details = manager.get_concept_details(concept)
            
            concept_card = Card.create(continue_section, hover=True)
            concept_card.pack(fill='x')
            
            content = ctk.CTkFrame(concept_card, fg_color='transparent')
            content.pack(fill='both', expand=True, padx=Spacing.LG, pady=Spacing.LG)
            
            name_label = ctk.CTkLabel(
                content,
                text=details['name'],
                font=(Typography.FALLBACK, Typography.H4, 'bold'),
                text_color=Colors.TEXT_PRIMARY
            )
            name_label.pack(anchor='w', pady=(0, Spacing.SM))
            
            badge_row = ctk.CTkFrame(content, fg_color='transparent')
            badge_row.pack(anchor='w', pady=(0, Spacing.MD))
            
            if details.get('iterable'):
                Badge.create(
                    badge_row,
                    details['iterable']['name'],
                    variant='primary'
                ).pack(side='left', padx=(0, Spacing.XS))
            
            if details.get('method'):
                Badge.create(
                    badge_row,
                    details['method']['name'],
                    variant='success'
                ).pack(side='left')
            
            explanation = details['explanation'][:120] + "..." if len(details['explanation']) > 120 else details['explanation']
            
            desc_label = ctk.CTkLabel(
                content,
                text=explanation,
                font=(Typography.FALLBACK, Typography.BODY),
                text_color=Colors.TEXT_SECONDARY,
                wraplength=800,
                justify='left'
            )
            desc_label.pack(anchor='w', pady=(0, Spacing.BASE))
            
            Button.create(
                content,
                UIText.START_LEARNING,
                callbacks['on_learn'],
                variant='primary',
                size='md'
            ).pack(anchor='w')
        
        actions_section = ctk.CTkFrame(scroll, fg_color='transparent')
        actions_section.pack(fill='x')
        
        actions_header = ctk.CTkLabel(
            actions_section,
            text=UIText.QUICK_ACTIONS,
            font=(Typography.FALLBACK, Typography.H3, 'bold'),
            text_color=Colors.TEXT_PRIMARY
        )
        actions_header.pack(anchor='w', pady=(0, Spacing.BASE))
        
        actions_row = ctk.CTkFrame(actions_section, fg_color='transparent')
        actions_row.pack(fill='x')
        
        actions_config = [
            ("Browse Topics", "Explore all concepts", callbacks['on_learn'], Colors.PRIMARY),
            ("Practice", "Solve challenges", callbacks['on_practice'], Colors.SUCCESS),
            ("Progress", "View achievements", callbacks['on_progress'], Colors.INFO)
        ]
        
        for title, desc, cmd, color in actions_config:
            action_card = Card.create(actions_row, hover=True)
            action_card.pack(side='left', padx=Spacing.SM, expand=True, fill='both')
            
            action_card.configure(cursor='hand2')
            
            def create_handler(command=cmd):
                return lambda e: command()
            
            handler = create_handler()
            action_card.bind('<Button-1>', handler)
            
            color_bar = ctk.CTkFrame(
                action_card,
                fg_color=color,
                height=4,
                corner_radius=0
            )
            color_bar.pack(fill='x')
            color_bar.bind('<Button-1>', handler)
            
            content_frame = ctk.CTkFrame(action_card, fg_color='transparent')
            content_frame.pack(fill='both', expand=True, padx=Spacing.BASE, pady=Spacing.BASE)
            content_frame.bind('<Button-1>', handler)
            
            title_label = ctk.CTkLabel(
                content_frame,
                text=title,
                font=(Typography.FALLBACK, Typography.H5, 'bold'),
                text_color=Colors.TEXT_PRIMARY
            )
            title_label.pack(pady=(Spacing.SM, Spacing.XXS))
            title_label.bind('<Button-1>', handler)
            
            desc_label = ctk.CTkLabel(
                content_frame,
                text=desc,
                font=(Typography.FALLBACK, Typography.BODY_SMALL),
                text_color=Colors.TEXT_SECONDARY
            )
            desc_label.pack(pady=(0, Spacing.SM))
            desc_label.bind('<Button-1>', handler)


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


class PracticeScreen:
    """Practice screen - results inline"""
    
    @staticmethod
    def create(parent, manager, current_index=0, on_back=None, gamification=None):
        print("🔥 NEW PRACTICE SCREEN LOADING")
        
        for widget in parent.winfo_children():
            widget.destroy()
        
        problems = manager.get_problems()
        
        if not problems or current_index >= len(problems):
            Alert.create(parent, "No problems available", variant='warning').pack(pady=50)
            return
        
        problem = problems[current_index]
        details = manager.get_problem_details(problem)
        
        # Header
        header = ctk.CTkFrame(parent, fg_color=Colors.BACKGROUND)
        header.pack(fill='x', side='top')
        
        hcontent = ctk.CTkFrame(header, fg_color='transparent')
        hcontent.pack(fill='x', padx=Spacing.XXL, pady=Spacing.BASE)
        
        if on_back:
            Button.create(hcontent, f"{Icons.ARROW_LEFT} Back", on_back, variant='ghost', size='sm').pack(anchor='w', pady=(0, Spacing.SM))
        
        ctk.CTkLabel(hcontent, text=f"Problem {current_index + 1} of {len(problems)}", font=(Typography.FALLBACK, Typography.BODY_SMALL), text_color=Colors.TEXT_MUTED).pack(anchor='w', pady=(0, Spacing.XXS))
        _, p = ProgressBar.create(hcontent, current_index + 1, len(problems), show_label=False)
        p.master.pack(fill='x')
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
        
        ctk.CTkLabel(left, text=details['name'], font=(Typography.FALLBACK, Typography.H3, 'bold'), text_color=Colors.TEXT_PRIMARY).pack(anchor='w', pady=(0, Spacing.SM))
        
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
            PracticeScreen._show_result(res, r, gamification)
        
        def hint():
            for w in res.winfo_children():
                w.destroy()
            Alert.create(res, f"💡 {details.get('hint', 'Try step by step!')}", variant='info').pack()
        
        def sol():
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
            Button.create(fc, f"{Icons.ARROW_LEFT} Previous", lambda: PracticeScreen.create(parent, manager, current_index - 1, on_back, gamification), variant='secondary', size='md').pack(side='left')
        if current_index < len(problems) - 1:
            Button.create(fc, f"Next {Icons.ARROW_RIGHT}", lambda: PracticeScreen.create(parent, manager, current_index + 1, on_back, gamification), variant='primary', size='md').pack(side='right')
    
    @staticmethod
    def _show_result(area, result, gam):
        for w in area.winfo_children():
            w.destroy()
        c = Card.create(area)
        c.pack(fill='x')
        cnt = ctk.CTkFrame(c, fg_color='transparent')
        cnt.pack(padx=Spacing.BASE, pady=Spacing.BASE)
        sc = result['score']
        col = Colors.SUCCESS if sc >= 70 else Colors.DANGER
        ctk.CTkLabel(cnt, text=f"Score: {sc}%", font=(Typography.FALLBACK, Typography.H3, 'bold'), text_color=col).pack(anchor='w')
        msg = "Perfect!" if result['valid'] and sc == 100 else "Good!" if result['valid'] else "Failed. Try again."
        ctk.CTkLabel(cnt, text=msg, font=(Typography.FALLBACK, Typography.BODY), text_color=col).pack(anchor='w', pady=(Spacing.XXS, 0))
        if result['errors']:
            ctk.CTkLabel(cnt, text=f"Error: {result['errors'][0]}", font=(Typography.FALLBACK, Typography.BODY_SMALL), text_color=Colors.DANGER, wraplength=520, justify='left').pack(anchor='w', pady=(Spacing.XS, 0))
        if result['valid'] and gam:
            xp = gam.record_problem_attempt("p", sc, perfect=(sc == 100))
            if xp['xp_gained'] > 0:
                ctk.CTkLabel(cnt, text=f"🎉 +{xp['xp_gained']} XP!", font=(Typography.FALLBACK, Typography.BODY, 'bold'), text_color=Colors.SUCCESS).pack(anchor='w', pady=(Spacing.SM, 0))


class ProgressScreen:
    """Progress screen"""
    
    @staticmethod
    def create(parent, manager):
        """Create progress screen"""
        for widget in parent.winfo_children():
            widget.destroy()
        
        container = ctk.CTkFrame(parent, fg_color=Colors.BACKGROUND)
        container.pack(fill='both', expand=True)
        
        ctk.CTkLabel(
            container,
            text="Your Progress",
            font=(Typography.FALLBACK, Typography.H1, 'bold'),
            text_color=Colors.TEXT_PRIMARY
        ).pack(pady=50)
        
        ctk.CTkLabel(
            container,
            text="Coming soon!",
            font=(Typography.FALLBACK, Typography.BODY_LARGE),
            text_color=Colors.TEXT_SECONDARY
        ).pack()