"""
Dashboard Screen - Main landing page
"""

import customtkinter as ctk
from src.ui.components import Button, Card, Badge, LevelIndicator
from src.ui.styles import Colors, Typography, Spacing
from src.ui.icons import UIText


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