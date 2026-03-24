import os
import re

print("Running updates...")

# 1. Flip Clock Style for index.html (and invitation.html)
flip_css = """
    /* --- FLIP CLOCK STYLES --- */
    .countdown-wrapper {
      display: flex;
      justify-content: center;
      gap: 15px !important;
      flex-wrap: wrap;
    }
    .count-block {
      display: flex;
      flex-direction: column;
      align-items: center;
    }
    .count-number {
      background: #2a2a2a;
      border-radius: 5px;
      box-shadow: inset 0 15px 50px #202020, 0 3px 10px #111;
      position: relative;
      display: inline-block;
      min-width: clamp(70px, 15vw, 100px);
      height: clamp(80px, 18vw, 120px);
      line-height: clamp(80px, 18vw, 120px);
      color: #eeeeee;
      font-size: clamp(2rem, 6vw, 4rem) !important;
      font-family: Arial, sans-serif !important;
      text-shadow: 0 1px 2px #333;
      border-top: 1px solid #393939;
      border-bottom: 1px solid #111;
      margin-bottom: 10px;
    }
    .count-number::before {
      border-bottom: 2px solid #000;
      content: "";
      height: 1px;
      left: 0;
      position: absolute;
      top: 50%;
      width: 100%;
      z-index: 10;
    }
    .count-label {
      font-size: 0.65rem !important;
      letter-spacing: 0.3em !important;
      color: var(--black) !important;
      text-transform: uppercase;
      font-weight: 600;
    }
"""

# 2. Heart Preloader for Admin HTML
preloader_css = """
    /* --- HEART PRELOADER --- */
    .loader-container {
      position: relative;
      width: 100%;
      height: 200px;
      display: flex;
      justify-content: center;
      align-items: center;
      flex-direction: column;
    }
    .loader-container .preloader {
      position: relative;
      width: 64px;
      height: 64px;
      animation: rotate 2.3s cubic-bezier(0.75, 0, 0.5, 1) infinite;
    }
    @keyframes rotate {
      50% { transform: rotate(360deg); }
      100% { transform: rotate(720deg); }
    }
    .preloader span {
      --c: #f23f3f;
      position: absolute;
      display: block;
      height: 64px;
      width: 64px;
      background: var(--c);
      border: 1px solid var(--c);
      border-radius: 100%;
    }
    .preloader span:nth-child(1) {
      transform: translate(-28px, -28px);
      animation: shape_1 2.3s cubic-bezier(0.75, 0, 0.5, 1) infinite;
    }
    @keyframes shape_1 {
      60% { transform: scale(0.4); }
    }
    .preloader span:nth-child(2) {
      transform: translate(28px, -28px);
      animation: shape_2 2.3s cubic-bezier(0.75, 0, 0.5, 1) infinite;
    }
    @keyframes shape_2 {
      40% { transform: scale(0.4); }
    }
    .preloader span:nth-child(3) {
      position: relative;
      border-radius: 0px;
      transform: scale(0.98) rotate(-45deg);
      animation: shape_3 2.3s cubic-bezier(0.75, 0, 0.5, 1) infinite;
    }
    @keyframes shape_3 {
      50% { border-radius: 100%; transform: scale(0.5) rotate(-45deg); }
      100% { transform: scale(0.98) rotate(-45deg); }
    }
    .shadow {
      position: relative;
      top: 30px;
      height: 16px;
      width: 64px;
      border-radius: 50%;
      background-color: #d9d9d9;
      border: 1px solid #d9d9d9;
      animation: shadow 2.3s cubic-bezier(0.75, 0, 0.5, 1) infinite;
    }
    @keyframes shadow {
      50% { transform: scale(0.5); border-color: #f2f2f2; }
    }
"""

preloader_html = """<tr><td colspan="7">
  <div class="loader-container">
    <div class="preloader">
      <span></span><span></span><span></span>
    </div>
    <div class="shadow"></div>
    <div style="margin-top:40px; font-size: 0.7rem; letter-spacing: 0.2em; color: #888;">LOADING...</div>
  </div>
</td></tr>"""

# Apply to main HTMLs
for file in ['index.html', 'invitation.html']:
    if os.path.exists(file):
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()

        if 'FLIP CLOCK STYLES' not in content:
            content = content.replace('</style>', flip_css + '\n  </style>', 1)
            
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated flip clock in {file}")

# Apply to admin.html
if os.path.exists('admin.html'):
    with open('admin.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'HEART PRELOADER' not in content:
        content = content.replace('</style>', preloader_css + '\n  </style>', 1)
    
    # Replace "Loading data from Convex..." tr with preloader
    content = re.sub(
        r'<tr><td colspan="7" style="text-align:center;padding:2rem;">Syncing with Convex\.\.\.</td></tr>', 
        preloader_html, 
        content
    )
    # Also replace in the HTML body fallback
    content = re.sub(
        r'<td colspan="7" style="text-align:center;padding:3rem;">Loading data from Convex\.\.\.</td>',
        preloader_html.replace('<tr><td colspan="7">', '<td colspan="7">').replace('</td></tr>', '</td>'),
        content
    )
    
    with open('admin.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated admin.html preloader")
