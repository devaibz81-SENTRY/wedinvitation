import os
import re

# 1. Update font-family for ampersand in index.html & invitation.html
for file in ['index.html', 'invitation.html']:
    if os.path.exists(file):
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # We know we put '/* Restore Ampersand */' and '.hero-ampersand {' in earlier
        font_override = "    .hero-ampersand {\\n        font-family: 'Great Vibes', cursive !important;\\n"
        if "font-family: 'Great Vibes'" not in content:
            content = content.replace('.hero-ampersand {\\n', font_override)
            
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)

# 2. Update Admin Dashboard Message Bay behavior
if os.path.exists('admin.html'):
    with open('admin.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Change wa-preview from div to textarea
    if '<div class="wa-preview" id="wa-preview">' in content:
        content = content.replace('<div class="wa-preview" id="wa-preview">Loading preview...</div>', 
                                  '<textarea class="wa-preview wa-template" id="wa-preview" style="min-height:180px;">Loading preview...</textarea>')

    # Update script logic for showSelectedPersonMeta and copyWA / sendOneWA
    js_update_meta = \"\"\"
      const due = person.deadline ? new Date(person.deadline).toLocaleDateString() : 'Not set';
      box.textContent = ${person.first_name}  |  |  | RSVP deadline: ;
      
      const previewBox = document.getElementById('wa-preview');
      if(previewBox && previewBox.tagName === 'TEXTAREA') {
          previewBox.value = buildPersonalizedText(person);
      }
    }
\"\"\"
    if "previewBox.tagName === 'TEXTAREA'" not in content:
        content = re.sub(r'const due.*?\}\n', js_update_meta, content, count=1, flags=re.DOTALL)

    # Make copyWA use .value for textarea
    content = content.replace("document.getElementById('wa-preview').textContent", "document.getElementById('wa-preview').value")

    # Make sendOneWA use the custom text from editor
    send_wa_update = \"\"\"
    function openGuestWhatsApp(g, customText = null) {
      if (!g) return false;
      const phone = normalizeWaPhone(g.phone);
      if (!phone) return false;
      const text = customText !== null ? customText : buildPersonalizedText(g);
      window.open(https://wa.me/?text=, '_blank');
      return true;
    }
    
    function sendOneWA() {
      const sel = document.getElementById('wa-person');
      if (!sel || !sel.value) { alert('Select a guest first.'); return; }
      const person = findGuestByKey(sel.value);
      if (!person) { alert('Could not find selected guest.'); return; }
      
      const customText = document.getElementById('wa-preview').value;
      if (!openGuestWhatsApp(person, customText)) {
        alert('No valid WhatsApp number for selected guest.');
      }
    }
\"\"\"
    # Replace openGuestWhatsApp definition
    if 'customText' not in content:
        content = re.sub(r'function openGuestWhatsApp.*?return true;\n    \}', send_wa_update, content, flags=re.DOTALL)
        
    with open('admin.html', 'w', encoding='utf-8') as f:
        f.write(content)

print('Updated Ampersand Font and Admin Message Bay!')
