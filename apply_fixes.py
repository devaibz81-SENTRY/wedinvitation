import os
import re

html_files = [f for f in os.listdir('.') if f.endswith('.html')]

# We'll update our previous appended CSS block to include the new requests:
css_injections = """
    /* --- COLOR & TRIM OVERRIDES V2 --- */
    .hero-flourish, .hero-divider, 
    .story-signature, .story-img-accent {
        display: none !important;
    }
    
    /* Restore Ampersand */
    .hero-ampersand {
        display: inline-block !important;
        color: #000000 !important;
    }
    
    /* Soft shadows on headings */
    h1, h2, h3, .section-title, .hero-names, .gift-title {
        text-shadow: 0 4px 15px rgba(0,0,0,0.08) !important;
    }
    
    /* Black Nav Header & Buttons */
    nav {
        background: #000000 !important;
        border-bottom: none !important;
    }
    nav a {
        background: #000000 !important;
        color: #ffffff !important;
        border: 1px solid rgba(255,255,255,0.3) !important;
    }
    nav a:hover {
        background: rgba(255,255,255,0.15) !important;
        border-color: #ffffff !important;
    }
    
    /* White Footer Text with Dark Background */
    footer {
        background: #000000 !important;
        color: #ffffff !important;
    }
    footer .footer-names, footer p {
        color: #ffffff !important;
    }
    /* Larger Date in Footer */
    footer p:nth-of-type(1) {
        font-size: clamp(2rem, 5vw, 3.2rem) !important;
        margin-top: 1rem;
    }
"""

js_countdown_old = """      if (diff <= 0) {
        document.querySelector('.countdown-wrapper').innerHTML =
          '<p style="font-family:\\'Great Vibes\\',cursive;font-size:3rem;color:var(--gold)">Today is the Day!</p>';
        return;
      }
      const d = Math.floor(diff / 86400000);
      const h = Math.floor((diff % 86400000) / 3600000);
      const m = Math.floor((diff % 3600000) / 60000);
      const s = Math.floor((diff % 60000) / 1000);"""

js_countdown_new = """      let absDiff = diff;
      if (diff <= 0) {
        absDiff = Math.abs(diff);
        // Find header holding 'Days Until We Say I Do'
        let headers = document.querySelectorAll('.section-eyebrow');
        headers.forEach(h => {
             if(h.innerText.includes('Days Until We Say I Do')) {
                  h.innerText = "Days we've been married";
             }
        });
        let pTags = document.querySelectorAll('p');
        pTags.forEach(p => {
             if(p.innerText.includes('Days Until We Say I Do')) {
                  p.innerText = "Days we've been married";
             }
        });
      }
      const d = Math.floor(absDiff / 86400000);
      const h = Math.floor((absDiff % 86400000) / 3600000);
      const m = Math.floor((absDiff % 3600000) / 60000);
      const s = Math.floor((absDiff % 60000) / 1000);"""

for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Update CSS injections. Remove old CSS block and insert new one
    content = re.sub(r'/\* --- COLOR & TRIM OVERRIDES --- \*/.*?</style>', css_injections + '\n  </style>', content, flags=re.DOTALL)
    
    # Also if it doesn't already have the old block but needs the new one (e.g. if we missed it somehow)
    if "/* --- COLOR & TRIM OVERRIDES V2 --- */" not in content:
        content = content.replace("</style>", f"{css_injections}\n  </style>")

    # 2. Update JS Logic in index.html specifically
    if file == 'index.html':
        content = content.replace(js_countdown_old, js_countdown_new)
        # Also let's make sure the text "Days Until We Say I Do" is found by adding an ID if possible:
        content = content.replace('Days Until We Say I Do', '<span id="countdown-title">Days Until We Say I Do</span>')
        
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print(f"Updated {len(html_files)} HTML files with new typography, UI, and JS changes.")
