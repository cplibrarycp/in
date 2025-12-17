import os
import re

# 1. പുതിയ CSS കോഡ് (നിങ്ങൾ ആവശ്യപ്പെട്ട വെള്ള ഹോവർ ഇഫക്റ്റ് ഉൾപ്പെടെ)
new_header_css = """
    /* --- റെസ്പോൺസീവ് ഹെഡർ (പൈത്തൺ വഴി അപ്ഡേറ്റ് ചെയ്തത്) --- */
    header {
        background-color: var(--secondary-dark);
        padding: 10px 0;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        position: sticky;
        top: 0;
        z-index: 1000;
        width: 100%;
    }
    .navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
    }
    .logo {
        font-size: 1.5em;
        font-weight: 700;
        color: #FFFFFF !important;
        display: flex;
        align-items: center;
        gap: 10px;
        white-space: nowrap;
    }
    .nav-links {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .nav-links a.nav-item {
        color: #FFFFFF !important;
        background-color: var(--secondary-dark) !important;
        font-weight: 600;
        font-size: 0.85em;
        text-transform: uppercase;
        padding: 8px 18px;
        border: 1.5px solid rgba(255, 255, 255, 0.4);
        border-radius: 4px;
        transition: all 0.3s ease;
        text-decoration: none;
        display: inline-block;
    }
    .nav-links a.nav-item:hover {
        background-color: #FFFFFF !important;
        color: var(--secondary-dark) !important;
        border-color: #FFFFFF;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        transform: translateY(-2px);
    }
    .user-profile {
        display: flex;
        align-items: center;
        margin-left: 15px;
        padding-left: 15px;
        border-left: 1px solid rgba(255, 255, 255, 0.2);
        position: relative;
        cursor: pointer;
        color: #FFFFFF;
    }
    @media (max-width: 850px) {
        .navbar { flex-direction: column; gap: 15px; }
        .nav-links { justify-content: center; width: 100%; flex-wrap: wrap; gap: 8px; }
        .user-profile { border-left: none; margin-left: 0; padding-left: 0; margin-top: 5px; }
        .logo { font-size: 1.3em; }
    }
"""

def update_html_files():
    # സ്ക്രിപ്റ്റ് ഇരിക്കുന്ന ഫോൾഡറിലെ എല്ലാ ഫയലുകളും പരിശോധിക്കുന്നു
    files = [f for f in os.listdir('.') if f.endswith('.html')]
    
    for filename in files:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()

        # പഴയ ഹെഡർ സ്റ്റൈലുകൾ കണ്ടെത്താനും മാറ്റാനും ശ്രമിക്കുന്നു
        # ഇത് 'header {' മുതൽ '.logo {' വരെയുള്ള ഭാഗം മാറ്റി പകരം പുതിയത് വെക്കും
        # അല്ലെങ്കിൽ സ്റ്റൈൽ ടാഗിനുള്ളിലേക്ക് ഇത് ചേർക്കും
        
        if '/* ---' in content or 'header {' in content:
            # നിലവിലുള്ള ഹെഡർ സ്റ്റൈൽ സെക്ഷൻ ഉണ്ടെങ്കിൽ അത് മാറ്റി പകരം വെക്കുന്നു
            # (ഇത് നിങ്ങളുടെ ഫയലിലെ CSS ഘടന അനുസരിച്ച് അല്പം മാറ്റം വന്നേക്കാം)
            pattern = re.compile(r'header\s*{[^}]*}.*?\.logo\s*{[^}]*}.*?\.nav-links\s*{[^}]*}.*?\.nav-item:hover\s*{[^}]*}', re.DOTALL)
            
            if pattern.search(content):
                new_content = pattern.sub(new_header_css, content)
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"✅ Updated: {filename}")
            else:
                print(f"⚠️ Could not auto-replace in {filename}. Adding to end of style tag.")
                # പാറ്റേൺ മാച്ച് ചെയ്തില്ലെങ്കിൽ </style> ടാഗിന് തൊട്ടു മുൻപായി ഇത് ചേർക്കുന്നു
                new_content = content.replace('</style>', new_header_css + '\n</style>')
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(new_content)

if __name__ == "__main__":
    update_html_files()