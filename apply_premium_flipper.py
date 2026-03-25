import os

def get_flip_group(id_prefix, digits=2):
    groups = []
    if digits == 3: groups.append('hundred')
    groups.extend(['ten', 'one'])
    html = f'<div class="flip-group" id="{id_prefix}">\\n'
    for g in groups:
        html += f'  <div class="nums nums-{g}">\\n'
        for i in range(10):
            nxt = (i + 1) % 10
            html += f'    <div class="num" data-num="{i}" data-num-next="{nxt}"></div>\\n'
        html += '  </div>\\n'
    html += '</div>'
    return html

carlos_css = """
/* --- FLIP CLOCK STYLES --- */
.countdown-wrapper { display: flex !important; justify-content: center !important; gap: 20px !important; flex-wrap: wrap; }
.count-block { display: flex !important; flex-direction: column !important; align-items: center !important; }
.flip-group { display: flex; gap: 5px; position: relative; height: 120px; }
.nums { box-shadow: 0 3px 10px #111; border-top: 1px solid #393939; display: inline-block; height: 100px; perspective: 1000px; position: relative; width: 70px; }
.nums:before { border-bottom: 2px solid black; content: ""; height: 1px; left: 0; position: absolute; transform: translate3d(0, -1px, 0); top: 50%; width: 100%; z-index: 1000; }
.nums:after { backface-visibility: hidden; background: #2a2a2a; border-bottom: 1px solid #444444; border-top: 1px solid black; border-radius: 0 0 5px 5px; bottom: 0; box-shadow: inset 0 15px 50px #202020; color: #eeeeee; content: "0"; display: block; font-size: 80px; height: calc(50% - 1px); left: 0; line-height: 0; overflow: hidden; position: absolute; text-align: center; text-shadow: 0 1px 2px #333; width: 100%; z-index: 0; }
.num { border-radius: 5px; font-size: 80px; height: 100%; left: 0; position: absolute; transform: rotateX(0deg); transition: transform 0.6s ease-in, z-index 0.6s; transform-style: preserve-3d; top: 0; width: 100%; z-index: 1; }
.num:before, .num:after { backface-visibility: hidden; color: #eeeeee; display: block; height: 50%; left: 0; overflow: hidden; position: absolute; text-align: center; text-shadow: 0 1px 2px #333; width: 100%; }
.num:before { background: #181818; border-radius: 5px 5px 0 0; box-shadow: inset 0 15px 50px #111111; content: attr(data-num); line-height: 1.38; top: 0; z-index: 2; }
.num:after { background: #2a2a2a; border-bottom: 1px solid #444444; border-radius: 0 0 5px 5px; box-shadow: inset 0 15px 50px #202020; content: attr(data-num-next); height: calc(50% - 1px); line-height: 0; top: 0; transform: rotateX(180deg); }
.num.flipping { transform: rotateX(-180deg); z-index: 50 !important; }
.num.active { z-index: 10; }
.count-label { margin-top: 15px; font-size: 0.65rem; letter-spacing: 0.3em; text-transform: uppercase; color: var(--black); }
@media (max-width: 600px) { .nums { width: 50px; height: 80px; } .num, .nums:after { font-size: 60px; } .flip-group { height: 100px; } }
"""

new_js = (
    "    function updateDigit(groupEl, value) {\\n"
    "        if (!groupEl) return;\\n"
    "        const currentNum = groupEl.getAttribute('data-val') || '0';\\n"
    "        if (currentNum === String(value)) return;\\n"
    "        groupEl.setAttribute('data-val', value);\\n"
    "        const nums = groupEl.querySelectorAll('.num');\\n"
    "        nums.forEach(n => { n.classList.remove('flipping'); n.classList.remove('active'); });\\n"
    "        const prev = parseInt(currentNum);\\n"
    "        if (nums[prev]) nums[prev].classList.add('flipping');\\n"
    "        if (nums[value]) nums[value].classList.add('active');\\n"
    "    }\\n"
    "    function updateFlipGroup(id, value, digits=2) {\\n"
    "        const groupWrap = document.getElementById(id);\\n"
    "        if (!groupWrap) return;\\n"
    "        const valStr = String(value).padStart(digits, '0');\\n"
    "        const groups = ['hundred', 'ten', 'one'];\\n"
    "        const startIdx = groups.length - digits;\\n"
    "        for (let i = 0; i < digits; i++) {\\n"
    "            const el = groupWrap.querySelector('.nums-' + groups[startIdx + i]);\\n"
    "            if (el) updateDigit(el, valStr[i]);\\n"
    "        }\\n"
    "    }\\n"
)

def apply_to_file(filename):
    if not os.path.exists(filename): return
    with open(filename, 'r', encoding='utf-8') as f: content = f.read()
    s_start = content.find('/* --- FLIP CLOCK STYLES --- */')
    s_end = content.find('*/', s_start + 30) + 2
    if s_start != -1: content = content[:s_start] + carlos_css + content[s_end:]
    content = content.replace('<span class="count-number" id="cd-days">--</span>', get_flip_group('fg-days', 3))
    content = content.replace('<span class="count-number" id="cd-hours">--</span>', get_flip_group('fg-hours', 2))
    content = content.replace('<span class="count-number" id="cd-mins">--</span>', get_flip_group('fg-mins', 2))
    content = content.replace('<span class="count-number" id="cd-secs">--</span>', get_flip_group('fg-secs', 2))
    if 'updateFlipGroup' not in content:
        content = content.replace('// Gift Modal Logic', new_js + '\\n    // Gift Modal Logic')
    content = content.replace("updateElement('cd-days', d);", "updateFlipGroup('fg-days', d, 3);")
    content = content.replace("updateElement('cd-hours', h);", "updateFlipGroup('fg-hours', h, 2);")
    content = content.replace("updateElement('cd-mins', m);", "updateFlipGroup('fg-mins', m, 2);")
    content = content.replace("updateElement('cd-secs', s);", "updateFlipGroup('fg-secs', s, 2);")
    with open(filename, 'w', encoding='utf-8') as f: f.write(content)
    print(f"Upgraded {filename}")

for f in ['index.html', 'invitation.html']: apply_to_file(f)
