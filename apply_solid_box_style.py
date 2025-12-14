import os
import re

# ================= സെറ്റിംഗ്സ് =================
# നിങ്ങളുടെ HTML ഫയലുകൾ ഉള്ള ഫോൾഡർ പാത്ത് ഇവിടെ നൽകുക
target_folder = r"L:\html"
# ============================================

# പുതിയ "Solid Box" ബട്ടൺ സ്റ്റൈൽ (Teal Theme-ന് അനുയോജ്യമായത്)
NEW_BUTTON_STYLE = """
        /* --- Updated Header Button: Solid Box Style --- */
        .nav-links a.nav-item {
            color: var(--light-text);
            margin-left: 15px;
            font-weight: 600;
            font-size: 0.85em;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            
            /* Box Shape */
            padding: 8px 18px;
            border: 1px solid rgba(255,255,255,0.3); /* തെളിഞ്ഞ ബോർഡർ */
            border-radius: 4px; /* അറ്റം ചെറുതായി വളയാൻ */
            transition: all 0.3s ease;
            text-decoration: none;
        }

        .nav-links a.nav-item:hover {
            background-color: #ffffff; /* ഹോവർ ചെയ്യുമ്പോൾ വെളുത്ത നിറം */
            color: var(--secondary-dark); /* അക്ഷരം ഡാർക്ക് ഗ്രീൻ ആകുന്നു */
            border-color: #ffffff;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            transform: translateY(-2px); /* ബട്ടൺ പൊങ്ങുന്നു */
        }
"""

def update_button_styles():
    print(f"Scanning folder: {target_folder}...")
    updated_count = 0

    # പഴയ CSS കണ്ടുപിടിക്കാനുള്ള പാറ്റേൺ
    # .nav-links a.nav-item { ... } മുതൽ :hover { ... } വരെയുള്ള ഭാഗം
    css_pattern = r"\.nav-links\s+a\.nav-item\s*\{[\s\S]*?\}\s*\.nav-links\s+a\.nav-item:hover\s*\{[\s\S]*?\}"

    for root, dirs, files in os.walk(target_folder):
        for file in files:
            if file.lower().endswith(".html"):
                file_path = os.path.join(root, file)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # പഴയ സ്റ്റൈൽ ഉണ്ടോ എന്ന് നോക്കുന്നു
                    if re.search(css_pattern, content):
                        # പഴയത് മാറ്റി പുതിയത് വെക്കുന്നു
                        new_content = re.sub(css_pattern, NEW_BUTTON_STYLE, content)
                        
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        
                        print(f"  [Updated]: {file}")
                        updated_count += 1
                    else:
                        print(f"  [Skipped]: {file} (Button CSS not found)")

                except Exception as e:
                    print(f"  [Error] {file}: {e}")

    print("-" * 30)
    print(f"വിജയകരം! {updated_count} ഫയലുകളിൽ Solid Box സ്റ്റൈൽ അപ്ഡേറ്റ് ചെയ്തു.")

if __name__ == "__main__":
    if os.path.exists(target_folder):
        update_button_styles()
    else:
        print("Error: നൽകിയ ഫോൾഡർ പാത്ത് നിലവിലില്ല.")