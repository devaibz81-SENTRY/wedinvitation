import os
import re

print("Starting cleanup...")

new_js = """    function copySpecificInput(text, hintId) {
        const hint = document.getElementById(hintId);
        const original = hint.innerText;

        const attemptCopy = (str) => {
            if(navigator.clipboard && navigator.clipboard.writeText) {
                return navigator.clipboard.writeText(str);
            } else {
                return new Promise((res, rej) => {
                    const temp = document.createElement('textarea');
                    temp.value = str;
                    document.body.appendChild(temp);
                    temp.select();
                    try { document.execCommand('copy'); res(); } 
                    catch(err) { rej(err); }
                    document.body.removeChild(temp);
                });
            }
        };

        attemptCopy(text).then(() => {
            hint.innerText = "COPIED!";
            hint.style.color = "#ffffff";
            setTimeout(() => { hint.innerText = original; hint.style.color = "#ccc"; }, 2000);
        }).catch(() => {
            hint.innerText = "COPIED!";
            hint.style.color = "#ffffff";
            setTimeout(() => { hint.innerText = original; hint.style.color = "#ccc"; }, 2000);
        });
    }"""

for file in ['index.html', 'invitation.html']:
    if os.path.exists(file):
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Update JS function
        if 'attemptCopy' not in content:
            js_pattern = r'function copySpecificInput.*?\}\n\s*\}\n'
            if re.search(js_pattern, content, re.DOTALL):
                content = re.sub(js_pattern, new_js + '\n', content, flags=re.DOTALL)

        # Update labels
        content = content.replace('(Tap to Copy)', '(Click/Tap to Copy)')

        # Tear out duplicate section
        delete_pattern = r'</div>\s*<div style="margin-bottom: 1\.5rem;">\s*<label\s*style="display: block; font-size: 0\.6rem;[^>]+>Bank</label>\s*<div[^>]+>Belize Bank</div>\s*</div>\s*<div>\s*<label\s*style="display: block; font-size: 0\.6rem;[^>]+>Account\s*Number</label>\s*<div[^>]+>\s*150816010140000</div>\s*</div>\s*<button id="copy-gift-btn"[^>]+>Copy Details To Clipboard</button>\s*</div>'
        
        # Replace it with just the closing div `</div>` for the first cream block
        if re.search(delete_pattern, content):
            content = re.sub(delete_pattern, r'</div>', content)
            
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Cleaned up in {file}")
