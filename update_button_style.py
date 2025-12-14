import os
import re

# ================= സെറ്റിംഗ്സ് =================
# നിങ്ങളുടെ HTML ഫയലുകൾ ഉള്ള ഫോൾഡർ പാത്ത് ഇവിടെ നൽകുക
target_folder = r"L:\html"
# ============================================

# പുതിയ "Solid Box" സ്റ്റൈൽ CSS
NEW_BUTTON_STYLE = """
        /* --- Updated Header Button: Solid Box Style --- */
        .nav-links a.nav-item {
            color: var(--light-text);
            margin-left: 15px;
            font-weight: 600;
            font-size: 0.85em;
            text-transform: uppercase;
            padding: 8px 16px; /* ബോക്സിനുള്ളിലെ സ്ഥലം */
            border: 1px solid rgba(255,255,255,0.3); /* നേരിയ ബോർഡർ */
            border-radius: 4px; /* അറ്റം ചെറുതായി വളയാൻ */
            transition: all 0.3s ease;
            text-decoration: none;
        }

        .nav-links a.nav-item:hover {
            background-color: #ffffff; /* മൗസ് വെക്കുമ്പോൾ വെളുത്ത നിറം */
            color: var(--secondary-dark); /* അക്ഷരം ഡാർക്ക് ആകുന്നു */
            border-color: #ffffff;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            transform: translateY(-2px);
        }
"""

def update_header_buttons():
    print(f"Scanning folder: {target_folder}...")
    count = 0

    # പഴയ CSS പാറ്റേൺ കണ്ടുപിടിക്കാനുള്ള Regex
    # .nav-links a.nav-item { ... } .nav-links a.nav-item:hover { ... }
    # ഇത് പഴയ ഏത് സ്റ്റൈൽ ആണെങ്കിലും കണ്ടുപിടിക്കും
    css_pattern = r"\.nav-links\s+a\.nav-item\s*\{[\s\S]*?\}\s*\.nav-links\s+a\.nav-item:hover\s*\{[\s\S]*?\}"

    for root, dirs, files in os.walk(target_folder):
        for file in files:
            if file.lower().endswith(".html"):
                file_path = os.path.join(root, file)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # പഴയ CSS ഉണ്ടോ എന്ന് നോക്കുന്നു
                    if re.search(css_pattern, content):
                        # ഉണ്ടെങ്കിൽ അത് മാറ്റി പുതിയത് വെക്കുന്നു
                        new_content = re.sub(css_pattern, NEW_BUTTON_STYLE, content)
                        
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        
                        print(f"  [Updated]: {file}")
                        count += 1
                    else:
                        print(f"  [Skipped]: {file} (CSS pattern not found)")

                except Exception as e:
                    print(f"  [Error] {file}: {e}")

    print("-" * 30)
    print(f"Success! Total {count} files updated with new button style.")

if __name__ == "__main__":
    if os.path.exists(target_folder):
        update_header_buttons()
    else:
        print("Error: നൽകിയ ഫോൾഡർ പാത്ത് നിലവിലില്ല.")