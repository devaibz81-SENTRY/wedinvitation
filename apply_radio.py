import os
import re

print("Running RSVP checkmark update...")

rsvp_css = """
    /* --- PRIYANSHUGUPTA28 ANIMATED CHECKS --- */
    .attend-option input[type="radio"] {
      visibility: hidden;
      display: none;
    }
    .attend-option .attend-label svg {
      vertical-align: middle;
      width: 44px;
      height: 44px;
      margin-bottom: 0.8rem;
    }
    .attend-option .path1 {
      stroke-dasharray: 400;
      stroke-dashoffset: 400;
      transition: .5s stroke-dashoffset;
      opacity: 0;
    }
    .attend-option input[type="radio"]:checked + .attend-label svg g .path1 {
      stroke-dashoffset: 0;
      opacity: 1;
    }
    .attend-option input[type="radio"]:checked + .attend-label svg path.bg {
      fill: #000;
    }
    .attend-option input[type="radio"]:checked + .attend-label svg g .path1 {
      stroke: #fff;
    }
"""

svg_yes = """<span class="attend-icon">
                <svg viewBox="0 0 50 50">
                  <path class="bg" d="M25,0C11.19,0,0,11.19,0,25s11.19,25,25,25s25-11.19,25-25S38.81,0,25,0z" fill="transparent" stroke="#000" stroke-width="1.5"></path>
                  <g><path class="path1" d="M15,25.5l7,7l14-14" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round"></path></g>
                </svg>
              </span>"""

if os.path.exists('rsvp.html'):
    with open('rsvp.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Inject CSS
    if 'PRIYANSHUGUPTA28' not in content:
        content = content.replace('</style>', rsvp_css + '\n  </style>', 1)

    # 2. Replaces the attend-icon spans
    content = re.sub(r'<span class="attend-icon">Yes</span>', svg_yes, content)
    content = re.sub(r'<span class="attend-icon">Later</span>', svg_yes, content)
    content = re.sub(r'<span class="attend-icon">No</span>', svg_yes, content)

    with open('rsvp.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated rsvp.html")
else:
    print("No rsvp.html found!")
