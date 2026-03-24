import os
import re

print("Running scribble checkmark update...")

svg_scribble = """<span class="attend-icon">
                <svg width="48" height="48" viewBox="0 0 95 95" style="margin-bottom:0.5rem">
                  <rect x="30" y="20" width="50" height="50" stroke="black" fill="none" stroke-width="2"></rect>
                  <g transform="translate(0,-952.36222)">
                    <path class="path1" d="m 56,963 c -102,122 6,9 7,9 17,-5 -66,69 -38,52 122,-77 -7,14 18,4 29,-11 45,-43 23,-4" stroke="black" stroke-width="3" fill="none"></path>
                  </g>
                </svg>
              </span>"""

if os.path.exists('rsvp.html'):
    with open('rsvp.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # The existing SVG we want to remove is:
    # <span class="attend-icon">
    #   <svg viewBox="0 0 50 50">
    #     <path class="bg" d="M25,0C11.19,0,0,11.19,0,25s11.19,25,25,25s25-11.19,25-25S38.81,0,25,0z" fill="transparent" stroke="#000" stroke-width="1.5"></path>
    #     <g><path class="path1" d="M15,25.5l7,7l14-14" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round"></path></g>
    #   </svg>
    # </span>
    
    old_svg_pattern = r'<span class="attend-icon">\s*<svg viewBox="0 0 50 50">\s*<path class="bg" d="M25.*?></path>\s*<g><path class="path1".*?></path></g>\s*</svg>\s*</span>'
    content = re.sub(old_svg_pattern, svg_scribble, content)

    # I also need to modify the CSS override I added earlier, specifically: 
    # `.attend-option input[type="radio"]:checked + .attend-label svg g .path1 { stroke: #fff; }`
    # Since the new check is black on a white background, we don't want it turning white when checked on a white background!
    # I should erase that CSS rule if it exists.
    content = content.replace('.attend-option input[type="radio"]:checked + .attend-label svg path.bg {\n      fill: #000;\n    }', '')
    content = content.replace('.attend-option input[type="radio"]:checked + .attend-label svg g .path1 {\n      stroke: #fff;\n    }', '')

    with open('rsvp.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated rsvp.html with PriyanshuGupta28 scribble check")
else:
    print("No rsvp.html found!")
