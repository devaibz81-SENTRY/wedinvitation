import os
import re

files_to_check = ['index.html', 'invitation.html']

css_inj = """
    /* Gift Modal Upgrades */
    .secret-card {
        background: #000000 !important;
        color: #ffffff !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        /* Animation base */
        transform: scale(0.9) translateY(40px) !important;
        transition: transform 0.6s cubic-bezier(0.34, 1.56, 0.64, 1), opacity 0.6s ease !important;
    }
    .secret-card.show {
        transform: scale(1) translateY(0) !important;
        opacity: 1 !important;
    }
    #gift-modal h3, #gift-modal label, #gift-modal div {
        color: #ffffff !important;
    }
    #gift-modal .section-eyebrow {
        color: rgba(255,255,255,0.6) !important;
    }
    #gift-modal > div > div:nth-of-type(1) {
        background: #111111 !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
    }
    #gift-modal button[onclick="closeGiftModal()"] {
        color: #ffffff !important;
    }
    .copy-btn {
        background: #ffffff;
        color: #000000;
        border: none;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        font-family: 'Montserrat', sans-serif;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        cursor: pointer;
        width: 100%;
        margin-top: 1rem;
        transition: transform 0.3s, box-shadow 0.3s;
    }
    .copy-btn:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(255,255,255,0.25);
    }
"""

copy_btn_html = """
        <button id="copy-gift-btn" class="copy-btn" onclick="copyGiftDetails()">Copy Details To Clipboard</button>
      </div>

      <p"""

js_inj = """
    // Copy to Clipboard
    function copyGiftDetails() {
        const details = "Account Name: Rosanna Depaz / Andrew Haylock\\nBank: Belize Bank\\nAccount Number: 150816010140000";
        if(navigator.clipboard && navigator.clipboard.writeText) {
             navigator.clipboard.writeText(details).then(() => {
                 const btn = document.getElementById('copy-gift-btn');
                 btn.innerText = "COPIED!";
                 setTimeout(() => btn.innerText = "COPY DETAILS TO CLIPBOARD", 2000);
             });
        }
    }
    
    // Gift Modal Logic
    function openGiftModal() {
      const modal = document.getElementById('gift-modal');
      const card = modal.querySelector('.secret-card');
      modal.style.display = 'flex';
      setTimeout(() => {
        card.classList.add('show');
      }, 10);
      document.body.style.overflow = 'hidden';
    }

    function closeGiftModal() {
      const modal = document.getElementById('gift-modal');
      const card = modal.querySelector('.secret-card');
      card.classList.remove('show');
      setTimeout(() => {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
      }, 500);
    }
"""

for file in files_to_check:
    if os.path.exists(file):
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Inject CSS
        if '/* Gift Modal Upgrades */' not in content:
            content = content.replace('</style>', css_inj + '\n  </style>', 1)
        
        # Inject HTML Copy Button
        if 'id="copy-gift-btn"' not in content:
            # We target the end of the inner details div, right before the "<p" with gratitude.
            content = content.replace("</div>\n\n      <p", copy_btn_html)
        
        # Replace JS
        # We need to replace the entire old openGiftModal / closeGiftModal block
        old_js_pattern = r'// Gift Modal Logic[\s\S]*?function closeGiftModal\(\) \{[\s\S]*?\}, 500\);\s*\}'
        if re.search(old_js_pattern, content):
            content = re.sub(old_js_pattern, js_inj.strip(), content)
        
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
print(f"Updates processed for {files_to_check}")
