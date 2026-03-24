import os
import re

files = [f for f in os.listdir('.') if f.endswith('.html')]

colors_to_change = {
    r'--gold:\s*#[0-9a-fA-F]+': '--gold: #000000',
    r'--cream:\s*#[0-9a-fA-F]+': '--cream: #ffffff',
    r'--champagne:\s*#[0-9a-fA-F]+': '--champagne: #ffffff',
    r'--ivory:\s*#[0-9a-fA-F]+': '--ivory: #ffffff',
    r'--green:\s*#[0-9a-fA-F]+': '--green: #ffffff',  # some files used green as champagne
}

# The user wants to hide gold trimming and gold letters on the end.
# We will inject a global CSS block right before </style> or right after <style> 
# to hide elements identified as trimming.
# Known typical trimming classes: .hero-flourish, .hero-divider, .hero-ampersand

css_overrides = """
    /* --- COLOR & TRIM OVERRIDES --- */
    .hero-flourish, .hero-divider, .hero-ampersand, 
    .story-signature, .story-img-accent {
        display: none !important;
    }
    .photo-frame::after {
        border-color: transparent !important;
    }
"""

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Apply color var swaps
    for pattern, replacement in colors_to_change.items():
        content = re.sub(pattern, replacement, content)
    
    # Inject display:none for trimmings
    if "/* --- COLOR & TRIM OVERRIDES --- */" not in content:
        content = content.replace("</style>", f"{css_overrides}\n  </style>")

    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print(f"Updated {len(files)} HTML files.")
