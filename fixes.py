import os
import re

print("Running updates...")
for file in ['index.html', 'invitation.html']:
    if os.path.exists(file):
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # We know we put '/* Restore Ampersand */' and '.hero-ampersand {' in earlier
        font_override = "    .hero-ampersand {\n        font-family: 'Great Vibes', cursive !important;\n"
        if "font-family: 'Great Vibes'" not in content:
            content = content.replace('.hero-ampersand {\n', font_override)
            
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated font for {file}")

if os.path.exists('admin.html'):
    with open('admin.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Change wa-preview from div to textarea
    if '<div class="wa-preview" id="wa-preview">' in content:
        content = content.replace('<div class="wa-preview" id="wa-preview">Loading preview...</div>', 
                                  '<textarea class="wa-preview wa-template" id="wa-preview" style="min-height:220px;">Loading preview...</textarea>')

    # 1. Update openGuestWhatsApp
    old_openGuest = re.search(r'function openGuestWhatsApp.*?return true;\s*\}', content, re.DOTALL)
    if old_openGuest:
        new_openGuest = """function openGuestWhatsApp(g, customText = null) {
      if (!g) return false;
      const phone = normalizeWaPhone(g.phone);
      if (!phone) return false;
      const text = customText !== null ? customText : buildPersonalizedText(g);
      window.open(`https://wa.me/${phone}?text=${encodeURIComponent(text)}`, '_blank');
      return true;
    }"""
        content = content.replace(old_openGuest.group(0), new_openGuest)

    # 2. Update sendOneWA
    old_sendOne = re.search(r'function sendOneWA.*?\}', content, re.DOTALL)
    if old_sendOne:
        new_sendOne = """function sendOneWA() {
      const sel = document.getElementById('wa-person');
      if (!sel || !sel.value) { alert('Select a guest first.'); return; }
      const person = findGuestByKey(sel.value);
      if (!person) { alert('Could not find selected guest.'); return; }
      
      const customText = document.getElementById('wa-preview').value;
      if (!openGuestWhatsApp(person, customText)) {
        alert('No valid WhatsApp number for selected guest.');
      }
    }"""
        content = content.replace(old_sendOne.group(0), new_sendOne)

    # 3. Update copyWA
    if "document.getElementById('wa-preview').textContent" in content:
        content = content.replace("document.getElementById('wa-preview').textContent", "document.getElementById('wa-preview').value")

    # 4. Update showSelectedPersonMeta to populate the text area
    old_meta = re.search(r'function showSelectedPersonMeta.*? box.textContent = `\$\{person\.first_name.*?\}', content, re.DOTALL)
    if old_meta and "previewBox.tagName === 'TEXTAREA'" not in content:
        new_meta = old_meta.group(0)[:-1] + """  const previewBox = document.getElementById('wa-preview');
      if(previewBox && previewBox.tagName === 'TEXTAREA') {
          previewBox.value = buildPersonalizedText(person);
      }
    }"""
        content = content.replace(old_meta.group(0), new_meta)

    with open('admin.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated admin.html message bay")
