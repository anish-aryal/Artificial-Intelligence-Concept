import sys
sys.path.append('src')

import tkinter as tk
from ui.components import Button, Card, Label, CodeBlock, InputBox, Badge, Divider
from ui.styles import Colors

# Create main window
window = tk.Tk()
window.title("🎨 Component Showcase - All UI Elements")
window.geometry("700x900")
window.configure(bg=Colors.BACKGROUND)

# Create scrollable canvas
canvas = tk.Canvas(window, bg=Colors.BACKGROUND, highlightthickness=0)
scrollbar = tk.Scrollbar(window, orient='vertical', command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg=Colors.BACKGROUND)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

# Main container
container = tk.Frame(scrollable_frame, bg=Colors.BACKGROUND)
container.pack(fill='both', expand=True, padx=30, pady=30)

# ============================================================
# TITLE
# ============================================================
title = tk.Label(
    container,
    text="🎨 Modern UI Component Showcase",
    font=('Arial', 28, 'bold'),
    bg=Colors.BACKGROUND,
    fg=Colors.TEXT_PRIMARY
)
title.pack(pady=(0, 10))

subtitle = tk.Label(
    container,
    text="All reusable components in action",
    font=('Arial', 14),
    bg=Colors.BACKGROUND,
    fg=Colors.TEXT_SECONDARY
)
subtitle.pack(pady=(0, 30))

# ============================================================
# 1. BUTTONS
# ============================================================
button_card = Card.create(container)
button_card.pack(fill='x', pady=(0, 20))

Label.heading(button_card, "1️⃣ Buttons").pack(pady=(20, 15), anchor='w', padx=20)

btn_frame = tk.Frame(button_card, bg=Colors.SURFACE)
btn_frame.pack(pady=(0, 20))

def on_click(name):
    print(f"✅ {name} button clicked!")

# All button styles
Button.create(btn_frame, "Primary Button", lambda: on_click("Primary"), style='primary').pack(pady=5)
Button.create(btn_frame, "Success Button", lambda: on_click("Success"), style='success').pack(pady=5)
Button.create(btn_frame, "Danger Button", lambda: on_click("Danger"), style='danger').pack(pady=5)
Button.create(btn_frame, "Secondary Button", lambda: on_click("Secondary"), style='secondary').pack(pady=5)
Button.create(btn_frame, "Outline Button", lambda: on_click("Outline"), style='outline').pack(pady=5)

Label.muted(button_card, "Hover over buttons to see color changes").pack(pady=(0, 15))

# ============================================================
# 2. LABELS / TYPOGRAPHY
# ============================================================
typography_card = Card.create(container)
typography_card.pack(fill='x', pady=(0, 20))

Label.heading(typography_card, "2️⃣ Typography / Labels").pack(pady=(20, 15), anchor='w', padx=20)

Label.title(typography_card, "Title Text Style").pack(pady=5, anchor='w', padx=20)
Label.heading(typography_card, "Heading Text Style").pack(pady=5, anchor='w', padx=20)
Label.subheading(typography_card, "Subheading Text Style").pack(pady=5, anchor='w', padx=20)
Label.body(typography_card, "Body text style - used for paragraphs and descriptions").pack(pady=5, anchor='w', padx=20)
Label.muted(typography_card, "Muted text style - used for secondary information").pack(pady=(5, 20), anchor='w', padx=20)

# ============================================================
# 3. BADGES
# ============================================================
badge_card = Card.create(container)
badge_card.pack(fill='x', pady=(0, 20))

Label.heading(badge_card, "3️⃣ Badges").pack(pady=(20, 15), anchor='w', padx=20)

badge_container = tk.Frame(badge_card, bg=Colors.SURFACE)
badge_container.pack(pady=(0, 20))

# Different badge colors
Badge.create(badge_container, "Level 1").pack(side='left', padx=5)
Badge.create(badge_container, "Easy", bg_color=Colors.SUCCESS_SUBTLE, fg_color=Colors.SUCCESS).pack(side='left', padx=5)
Badge.create(badge_container, "Medium", bg_color=Colors.WARNING_SUBTLE, fg_color=Colors.WARNING).pack(side='left', padx=5)
Badge.create(badge_container, "Hard", bg_color=Colors.DANGER_SUBTLE, fg_color=Colors.DANGER).pack(side='left', padx=5)
Badge.create(badge_container, "Info", bg_color=Colors.INFO_SUBTLE, fg_color=Colors.INFO).pack(side='left', padx=5)

# ============================================================
# 4. CODE BLOCK
# ============================================================
code_card = Card.create(container)
code_card.pack(fill='x', pady=(0, 20))

Label.heading(code_card, "4️⃣ Code Display Block").pack(pady=(20, 15), anchor='w', padx=20)

sample_code = """# Python iteration example
numbers = [1, 2, 3, 4, 5]
for num in numbers:
    print(num)

# Output: 1, 2, 3, 4, 5"""

code_block = CodeBlock.create(code_card, sample_code, height=7)
code_block.pack(fill='x', padx=20, pady=(0, 20))

Label.muted(code_card, "Dark theme with syntax highlighting (monospace font)").pack(pady=(0, 15))

# ============================================================
# 5. INPUT BOX
# ============================================================
input_card = Card.create(container)
input_card.pack(fill='x', pady=(0, 20))

Label.heading(input_card, "5️⃣ Text Input Box").pack(pady=(20, 15), anchor='w', padx=20)
Label.body(input_card, "Type your Python code here:").pack(pady=(0, 10), anchor='w', padx=20)

input_container, text_box = InputBox.create(input_card, height=5, width=60)
input_container.pack(fill='x', padx=20, pady=(0, 10))

# Add sample text
text_box.insert('1.0', "# Write your code here...\n")

# Submit button
submit_frame = tk.Frame(input_card, bg=Colors.SURFACE)
submit_frame.pack(pady=(0, 20))

def check_code():
    code = text_box.get('1.0', 'end-1c')
    print(f"✅ Submitted code:\n{code}")

Button.create(submit_frame, "Submit Code", check_code, style='success', width=150).pack()

# ============================================================
# 6. DIVIDER
# ============================================================
divider_card = Card.create(container)
divider_card.pack(fill='x', pady=(0, 20))

Label.heading(divider_card, "6️⃣ Horizontal Divider").pack(pady=(20, 15), anchor='w', padx=20)
Label.body(divider_card, "Content above divider").pack(pady=5, anchor='w', padx=20)

Divider.create(divider_card).pack(fill='x', padx=20, pady=15)

Label.body(divider_card, "Content below divider").pack(pady=(5, 20), anchor='w', padx=20)

# ============================================================
# 7. CARDS
# ============================================================
cards_demo_card = Card.create(container)
cards_demo_card.pack(fill='x', pady=(0, 20))

Label.heading(cards_demo_card, "7️⃣ Cards (Containers)").pack(pady=(20, 15), anchor='w', padx=20)
Label.body(cards_demo_card, "All components above are inside Card containers!").pack(pady=(0, 10), anchor='w', padx=20)

# Nested cards example
nested_container = tk.Frame(cards_demo_card, bg=Colors.SURFACE)
nested_container.pack(fill='x', padx=20, pady=(0, 20))

mini_card1 = Card.create(nested_container)
mini_card1.pack(side='left', padx=10, ipadx=20, ipady=15)
Label.body(mini_card1, "Card 1").pack(padx=10, pady=10)

mini_card2 = Card.create(nested_container)
mini_card2.pack(side='left', padx=10, ipadx=20, ipady=15)
Label.body(mini_card2, "Card 2").pack(padx=10, pady=10)

mini_card3 = Card.create(nested_container)
mini_card3.pack(side='left', padx=10, ipadx=20, ipady=15)
Label.body(mini_card3, "Card 3").pack(padx=10, pady=10)

# ============================================================
# 8. COMBINED EXAMPLE
# ============================================================
combined_card = Card.create(container)
combined_card.pack(fill='x', pady=(0, 20))

Label.heading(combined_card, "8️⃣ Real-World Example").pack(pady=(20, 15), anchor='w', padx=20)
Label.subheading(combined_card, "Problem: Print List Items").pack(pady=(0, 10), anchor='w', padx=20)

# Problem description
Label.body(
    combined_card, 
    "Write code to print each item in the list: numbers = [1, 2, 3]"
).pack(pady=(0, 10), anchor='w', padx=20)

# Badges
difficulty_frame = tk.Frame(combined_card, bg=Colors.SURFACE)
difficulty_frame.pack(pady=(0, 15), anchor='w', padx=20)

Badge.create(difficulty_frame, "Level 1").pack(side='left', padx=5)
Badge.create(difficulty_frame, "Easy", bg_color=Colors.SUCCESS_SUBTLE, fg_color=Colors.SUCCESS).pack(side='left', padx=5)

# Code input
Label.body(combined_card, "Your solution:").pack(pady=(0, 5), anchor='w', padx=20)
example_container, example_box = InputBox.create(combined_card, height=4, width=60)
example_container.pack(fill='x', padx=20, pady=(0, 15))

# Buttons
action_frame = tk.Frame(combined_card, bg=Colors.SURFACE)
action_frame.pack(pady=(0, 20))

Button.create(action_frame, "Submit", lambda: print("Submit!"), style='success', width=120).pack(side='left', padx=5)
Button.create(action_frame, "Get Hint", lambda: print("Hint!"), style='outline', width=120).pack(side='left', padx=5)
Button.create(action_frame, "Reset", lambda: print("Reset!"), style='secondary', width=120).pack(side='left', padx=5)

# ============================================================
# FOOTER
# ============================================================
footer = tk.Label(
    container,
    text="✅ All components rendered successfully on macOS!",
    font=('Arial', 13, 'bold'),
    bg=Colors.BACKGROUND,
    fg=Colors.SUCCESS
)
footer.pack(pady=(20, 0))

# Pack canvas and scrollbar
canvas.pack(side='left', fill='both', expand=True)
scrollbar.pack(side='right', fill='y')

# Mouse wheel scrolling
def on_mousewheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

canvas.bind_all("<MouseWheel>", on_mousewheel)

# Instructions
print("=" * 60)
print("🎨 COMPONENT SHOWCASE RUNNING")
print("=" * 60)
print("Test each component:")
print("  • Click all 5 button types")
print("  • Hover over buttons (they change color)")
print("  • Type in the input boxes")
print("  • Scroll with mouse wheel")
print("  • Click Submit/Hint/Reset buttons")
print("=" * 60)

window.mainloop()