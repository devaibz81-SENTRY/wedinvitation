import os
import re

print("Running updates...")

# 1. Update the nav bar by injecting RSVP link
def update_nav(content):
    if '<a href="rsvp.html">RSVP</a>' not in content:
        # The structure is <nav>\n  <a href="#story">Story</a>\n  <a href="#details">Details</a>\n</nav>
        content = re.sub(
            r'<a href="#details">Details</a>', 
            '<a href="#details">Details</a>\n    <a href="rsvp.html">RSVP</a>', 
            content
        )
    return content

# 2. Update the Quote Card
def update_quote_card(content):
    # Old max-width 600px with clamp 1.4-1.8
    card_pattern = re.compile(r'<blockquote class="reveal" style="background:\s*#000000;[^>]*>.*?</blockquote>', re.DOTALL)
    
    new_card = """<blockquote class="reveal" style="background: #000000; color: #ffffff; padding: 3rem 2rem; border-radius: 12px; text-align: center; margin: 4rem auto; font-family: 'Cormorant Garamond', serif; font-size: clamp(1.1rem, 3vw, 1.35rem); font-style: italic; box-shadow: 0 10px 30px rgba(0,0,0,0.15); max-width: 550px; line-height: 1.8; position: relative;">
          <div style="font-size: 1.5rem; margin-bottom: 0.8rem; color: #ffffff; opacity: 0.8;">❦</div>
          <p style="margin: 0;">"Love isn’t just about the good moments.<br />
          It’s about choosing each other through everything."</p>
          <div style="font-size: 1.5rem; margin-top: 0.8rem; color: #ffffff; opacity: 0.8; transform: rotate(180deg);">❦</div>
        </blockquote>"""
    
    if re.search(card_pattern, content):
        content = re.sub(card_pattern, new_card, content)
    return content

for file in ['index.html', 'invitation.html']:
    if os.path.exists(file):
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        content = update_nav(content)
        content = update_quote_card(content)
            
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {file}")
