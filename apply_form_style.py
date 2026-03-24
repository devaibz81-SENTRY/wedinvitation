import os

print("Applying Praashoo7 input styling to rsvp.html...")

# CSS to inject
praashoo_css = """
    /* --- PRAASHOO7-INSPIRED INPUT STYLING --- */
    .form-group {
      display: flex;
      flex-direction: column;
      gap: 0.5rem;
    }

    .form-group label {
      font-size: 0.65rem;
      letter-spacing: 0.15em;
      text-transform: uppercase;
      color: #555;
      font-weight: 600;
    }

    /* Pill-style input wrapper */
    .input-wrap {
      display: flex;
      align-items: center;
      gap: 0.6rem;
      background: #1a1a1a;
      border-radius: 25px;
      padding: 0.7rem 1.1rem;
      box-shadow: inset 2px 5px 10px rgba(0,0,0,0.6);
      transition: box-shadow 0.3s;
    }

    .input-wrap:focus-within {
      box-shadow: inset 2px 5px 10px rgba(0,0,0,0.9), 0 0 0 2px rgba(255,255,255,0.1);
    }

    .input-wrap .input-icon {
      width: 1.2em;
      height: 1.2em;
      fill: rgba(255,255,255,0.5);
      flex-shrink: 0;
    }

    .form-group input,
    .form-group select {
      background: none;
      border: none;
      outline: none;
      width: 100%;
      color: #d3d3d3;
      font-family: 'Cormorant Garamond', serif;
      font-size: 1.1rem;
      font-weight: 500;
    }

    .form-group input::placeholder,
    .form-group select::placeholder {
      color: rgba(255,255,255,0.25);
      font-style: italic;
    }

    .form-group select {
      cursor: pointer;
      color: #d3d3d3;
    }

    .form-group select option {
      background: #1a1a1a;
      color: #d3d3d3;
    }

    /* Keep textarea separate - full width, no pill */
    .form-group textarea {
      width: 100%;
      min-height: 120px;
      padding: 1rem 1.1rem;
      border-radius: 16px;
      border: none;
      background: #1a1a1a;
      box-shadow: inset 2px 5px 10px rgba(0,0,0,0.6);
      font-family: 'Cormorant Garamond', serif;
      font-size: 1rem;
      color: #d3d3d3;
      resize: vertical;
      outline: none;
      transition: box-shadow 0.3s;
    }

    .form-group textarea:focus {
      box-shadow: inset 2px 5px 10px rgba(0,0,0,0.9), 0 0 0 2px rgba(255,255,255,0.1);
    }

    .form-group textarea::placeholder {
      color: rgba(255,255,255,0.25);
      font-style: italic;
    }
"""

# Icon definitions
icon_person = '<svg class="input-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"><path d="M8 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm2-3a2 2 0 1 1-4 0 2 2 0 0 1 4 0zm4 8c0 1-1 1-1 1H3s-1 0-1-1 1-4 6-4 6 3 6 4zm-1-.004c-.001-.246-.154-.986-.832-1.664C11.516 10.68 10.029 10 8 10c-2.029 0-3.516.68-4.168 1.332-.678.678-.83 1.418-.832 1.664h10z"/></svg>'
icon_email = '<svg class="input-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"><path d="M0 4a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V4zm2-1a1 1 0 0 0-1 1v.217l7 4.2 7-4.2V4a1 1 0 0 0-1-1H2zm13 2.383-4.708 2.825L15 11.105V5.383zm-.034 6.876-5.64-3.471L8 9.583l-1.326-.795-5.64 3.47A1 1 0 0 0 2 13h12a1 1 0 0 0 .966-.741zM1 11.105l4.708-2.897L1 5.383v5.722z"/></svg>'
icon_phone = '<svg class="input-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"><path d="M3.654 1.328a.678.678 0 0 0-1.015-.063L1.605 2.3c-.483.484-.661 1.169-.45 1.77a17.568 17.568 0 0 0 4.168 6.608 17.569 17.569 0 0 0 6.608 4.168c.601.211 1.286.033 1.77-.45l1.034-1.034a.678.678 0 0 0-.063-1.015l-2.307-1.794a.678.678 0 0 0-.58-.122l-2.19.547a1.745 1.745 0 0 1-1.657-.459L5.482 8.062a1.745 1.745 0 0 1-.46-1.657l.548-2.19a.678.678 0 0 0-.122-.58L3.654 1.328z"/></svg>'
icon_music = '<svg class="input-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"><path d="M6 13c0 1.105-1.12 2-2.5 2S1 14.105 1 13c0-1.104 1.12-2 2.5-2s2.5.896 2.5 2zm9-2c0 1.105-1.12 2-2.5 2s-2.5-.895-2.5-2 1.12-2 2.5-2 2.5.895 2.5 2zM14 11V2h1v9h-1zM6 3v10H5V3h1z"/><path d="M5 2.905a1 1 0 0 1 .9-.995l8-.8a1 1 0 0 1 1.1.995V3L5 4V2.905z"/></svg>'
icon_msg = '<svg class="input-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"><path d="M2.678 11.894a1 1 0 0 1 .287.801 10.97 10.97 0 0 1-.398 2c1.395-.323 2.247-.697 2.634-.893a1 1 0 0 1 .71-.074A8.06 8.06 0 0 0 8 14c3.996 0 7-2.807 7-6 0-3.192-3.004-6-7-6S1 4.808 1 8c0 1.468.617 2.83 1.678 3.894z"/></svg>'

def wrap_input(html, placeholder_frag, icon_html, input_pattern):
    """Wrap a bare input in the pill .input-wrap container"""
    return html.replace(input_pattern, 
        f'<div class="input-wrap">\n              {icon_html}\n              {input_pattern.strip()}\n            </div>')

if os.path.exists('rsvp.html'):
    with open('rsvp.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Inject CSS
    if 'PRAASHOO7-INSPIRED' not in content:
        content = content.replace('</style>', praashoo_css + '\n  </style>', 1)

    # 2. Wrap each bare input with the pill wrapper + icon
    # They look like: <input type="text" id="first-name" placeholder="..." />
    # We replace them individually
    replacements = [
        ('<input type="text" id="first-name" placeholder="Your first name" required />',
         f'<div class="input-wrap">{icon_person}\n              <input type="text" id="first-name" placeholder="Your first name" required /></div>'),
        ('<input type="text" id="last-name" placeholder="Your last name" />',
         f'<div class="input-wrap">{icon_person}\n              <input type="text" id="last-name" placeholder="Your last name" /></div>'),
        ('<input type="email" id="email" placeholder="your@email.com" />',
         f'<div class="input-wrap">{icon_email}\n              <input type="email" id="email" placeholder="your@email.com" /></div>'),
        ('<input type="tel" id="phone" placeholder="+501 000 0000" onclick="toggleNumberPad()" onfocus="toggleNumberPad()" readonly />',
         f'<div class="input-wrap">{icon_phone}\n              <input type="tel" id="phone" placeholder="+501 000 0000" onclick="toggleNumberPad()" onfocus="toggleNumberPad()" readonly /></div>'),
        ('<input type="text" id="song" placeholder="Song title - Artist" />',
         f'<div class="input-wrap">{icon_music}\n              <input type="text" id="song" placeholder="Song title - Artist" /></div>'),
    ]
    
    for old, new in replacements:
        if old in content and 'input-wrap' not in content.split(old)[0].split('<div class="form-group">')[-1]:
            content = content.replace(old, new, 1)

    with open('rsvp.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated rsvp.html with Praashoo7 pill input styling!")
