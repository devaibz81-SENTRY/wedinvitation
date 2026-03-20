import os
import re
import shutil

repo_dir = r"C:\Users\tcabb\OneDrive\Documents\wedding\wedinvitation"
index_file = os.path.join(repo_dir, "index.html")
invite_card_file = os.path.join(repo_dir, "invite-card.html")
invitation_file = os.path.join(repo_dir, "invitation.html")

# 1. Rename files appropriately
if os.path.exists(index_file):
    shutil.move(index_file, invitation_file)
if os.path.exists(invite_card_file):
    shutil.move(invite_card_file, index_file)

# 2. Add redirect to the Card (now index.html)
with open(index_file, 'r', encoding='utf-8') as f:
    card_html = f.read()

# The card currently fades out the overlay. Change it to redirect.
if "setTimeout(function () { overlay.style.display = 'none'; }, 1000);" in card_html:
    card_html = card_html.replace(
        "setTimeout(function () { overlay.style.display = 'none'; }, 1000);",
        "setTimeout(function () { window.location.href = 'invitation.html'; }, 1000);"
    )
elif "document.body.style.overflow = ''; window.scrollTo(0,0);" in card_html:
    # If the previous merge logic was somehow in there
    card_html = re.sub(r'setTimeout\(function \(\) \{ overlay\.style\.display = \'none\';.*?\}, 1000\);', 
                       "setTimeout(function () { window.location.href = 'invitation.html'; }, 1000);", card_html)
else:
    # Fallback if text differs slightly
    card_html = re.sub(r'setTimeout\(function \(\) \{.*overlay\.style\.display = \'none\'.*?\}, 1000\);', 
                       "setTimeout(function () { window.location.href = 'invitation.html'; }, 1000);", card_html)

with open(index_file, 'w', encoding='utf-8') as f:
    f.write(card_html)


# 3. Apply the 8 Polish fixes to the Main Site (now invitation.html)
with open(invitation_file, 'r', encoding='utf-8') as f:
    legacy_html = f.read()

legacy_html = legacy_html.replace('background: var(--green);', 'background: var(--black);')
legacy_html = legacy_html.replace('background-color: var(--green);', 'background-color: var(--black);')
legacy_html = legacy_html.replace('class="btn-gold">RSVP Now', 'class="btn-gold" style="background-color: var(--black); color: var(--ivory); border-color: var(--black);">RSVP Now')
legacy_html = legacy_html.replace('padding: 6rem 2rem 4rem;', 'padding: 10rem 2rem 4rem;')

if '.time-unit .number {' in legacy_html:
    legacy_html = legacy_html.replace('.time-unit .number {', '.time-unit .number { font-variant-numeric: tabular-nums; display: inline-block; min-width: 1.5em; ')

old_event = """<div class="detail-label">When &amp; Where</div>
          <div class="detail-value">Saturday, July 4th, 2026<br />4:00 PM</div>
          <div class="detail-divider"></div>
          <div class="detail-value">Gully Grill<br />San Ignacio</div>"""
new_event = """<div class="detail-label">When &amp; Where</div>
          <div class="detail-value"><strong>Ceremony:</strong><br />Sacred Heart Church, 2:00 PM</div>
          <div class="detail-divider" style="margin: 1rem auto; width: 40px; height: 1px; background: var(--gold);"></div>
          <div class="detail-value"><strong>Reception:</strong><br />The Gully Grill, San Ignacio</div>"""
if old_event in legacy_html:
    legacy_html = legacy_html.replace(old_event, new_event)
else:
    legacy_html = legacy_html.replace('Gully Grill<br />San Ignacio', '<strong>Ceremony:</strong> Sacred Heart Church at 2:00 PM<br /><br /><strong>Reception:</strong> The Gully Grill, San Ignacio')

legacy_html = legacy_html.replace("Your presence is the greatest gift of all.", "Your presence at our wedding is appreciated.")
legacy_html = legacy_html.replace("However, should you wish to honor us with a gift, a contribution toward our future together would be deeply appreciated.", "Should you wish to honor us with a gift, we would gratefully appreciate a monetary contribution toward our future together.")

legacy_html = re.sub(r'Rosanna\s+(?:Vanessa\s+)?Depaz', 'Rosanna', legacy_html)
legacy_html = re.sub(r'Andrew\s+(?:Denton\s+)?Haylock', 'Andrew', legacy_html)

legacy_html = legacy_html.replace('Gully Grill', 'The Gully Grill')
legacy_html = legacy_html.replace('The The Gully', 'The Gully')

# Swap Gift / Registry and RSVP
registry_match = re.search(r'(<section id="registry".*?</section>)', legacy_html, re.DOTALL)
rsvp_match = re.search(r'(<section id="rsvp".*?</section>)', legacy_html, re.DOTALL)
if registry_match and rsvp_match:
    legacy_html = legacy_html.replace(registry_match.group(1), '')
    legacy_html = legacy_html.replace(rsvp_match.group(1), registry_match.group(1) + '\n\n' + rsvp_match.group(1))

with open(invitation_file, 'w', encoding='utf-8') as f:
    f.write(legacy_html)

print("Site successfully split and rewritten with redirect!")
