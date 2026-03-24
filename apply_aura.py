import os

new_css = """
    /* --- LATEST USER REQUESTS --- */
    .story-img-wrap {
        background: #000000 !important;
    }

    body {
        position: relative;
    }
    
    body::before {
        content: '';
        position: fixed;
        inset: -10%;
        z-index: -10;
        pointer-events: none;
        background:
            radial-gradient(ellipse 80% 60% at 20% 30%, rgba(0, 0, 0, 0.04) 0%, transparent 60%),
            radial-gradient(ellipse 60% 50% at 80% 70%, rgba(0, 0, 0, 0.03) 0%, transparent 60%),
            radial-gradient(ellipse 40% 40% at 50% 10%, rgba(0, 0, 0, 0.02) 0%, transparent 50%);
        animation: auraShiftGlobal 18s ease-in-out infinite alternate;
    }
    
    @keyframes auraShiftGlobal {
        0% { transform: scale(1) translate(0,0) rotate(0deg); }
        50% { transform: scale(1.05) translate(1%, 2%) rotate(1deg); }
        100% { transform: scale(1.1) translate(-1%, -1%) rotate(-1deg); }
    }
    
    #hero::before { display: none !important; }
"""

print("Injecting aura & photo background fixes...")

for file in ['index.html', 'invitation.html']:
    if os.path.exists(file):
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()

        if 'auraShiftGlobal' not in content:
            content = content.replace('</style>', new_css + '\n  </style>', 1)
            
            with open(file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated {file}")
        else:
            print(f"{file} already has aura effect.")
