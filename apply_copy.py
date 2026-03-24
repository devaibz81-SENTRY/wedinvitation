import os
import re

print("Running copy update...")

new_bank_details = """      <div style="background: var(--cream); padding: 2rem; border-radius: 8px; text-align: left; margin-bottom: 1rem;">
        <div style="margin-bottom: 1.5rem; cursor: pointer; transition: opacity 0.2s;" onclick="copySpecificInput('Rosanna Depaz / Andrew Haylock', 'copy-name-hint')" onmouseover="this.style.opacity=0.7" onmouseout="this.style.opacity=1">
          <label
            style="display: flex; justify-content: space-between; font-size: 0.6rem; letter-spacing: 0.15em; text-transform: uppercase; color: #888; margin-bottom: 0.5rem;">Account
            Name <span id="copy-name-hint" style="color: #ccc; font-weight: 600;">(Tap to Copy)</span></label>
          <div style="font-family: 'Cormorant Garamond', serif; font-size: 1.3rem; color: var(--black);">Rosanna Depaz / Andrew Haylock</div>
        </div>
        <div style="margin-bottom: 1.5rem;">
          <label
            style="display: block; font-size: 0.6rem; letter-spacing: 0.15em; text-transform: uppercase; color: #888; margin-bottom: 0.5rem;">Bank</label>
          <div style="font-family: 'Cormorant Garamond', serif; font-size: 1.3rem; color: var(--black);">Belize Bank</div>
        </div>
        <div style="cursor: pointer; transition: opacity 0.2s;" onclick="copySpecificInput('150816010140000', 'copy-num-hint')" onmouseover="this.style.opacity=0.7" onmouseout="this.style.opacity=1">
          <label
            style="display: flex; justify-content: space-between; font-size: 0.6rem; letter-spacing: 0.15em; text-transform: uppercase; color: #888; margin-bottom: 0.5rem;">Account
            Number <span id="copy-num-hint" style="color: #ccc; font-weight: 600;">(Tap to Copy)</span></label>
          <div
            style="font-family: 'Cormorant Garamond', serif; font-size: 1.3rem; color: var(--black); letter-spacing: 0.05em;">
            150816010140000</div>
        </div>
      </div>"""

new_js = """    // Copy to Clipboard Specific
    function copySpecificInput(text, hintId) {
        if(navigator.clipboard && navigator.clipboard.writeText) {
             navigator.clipboard.writeText(text).then(() => {
                 const hint = document.getElementById(hintId);
                 const original = hint.innerText;
                 hint.innerText = "COPIED!";
                 hint.style.color = "#ffffff";
                 setTimeout(() => { hint.innerText = original; hint.style.color = "#ccc"; }, 2000);
             });
        }
    }
    
    // Gift Modal Logic"""

for file in ['index.html', 'invitation.html']:
    if os.path.exists(file):
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()

        # 1. Replace the inner div of banking details
        # Pattern captures the div with background var(--cream) down to its closing </div>
        pattern_banking = r'<div style="background: var\(--cream\); padding: 2rem; border-radius: 8px; text-align: left; margin-bottom: 1rem;">.*?</div>\s*</div>'
        if re.search(pattern_banking, content, re.DOTALL):
            content = re.sub(pattern_banking, new_bank_details, content, flags=re.DOTALL)
        
        # 2. Replace the copyGiftDetails JS logic with copySpecificInput
        pattern_js = r'// Copy to Clipboard\s*function copyGiftDetails\(\) \{[\s\S]*?\}\s*// Gift Modal Logic'
        if re.search(pattern_js, content):
            content = re.sub(pattern_js, new_js, content)
            
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {file}")
