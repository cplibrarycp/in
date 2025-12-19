import os

# നിങ്ങളുടെ HTML ഫയലുകൾ ഉള്ള ഫോൾഡറിന്റെ പാത്ത് താഴെ നൽകുക
directory = r"L:\BOOK\New"

def fix_mobile_view_v2(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # മൊബൈലിൽ ഹെഡർ ഇറക്കി വെക്കാനും 2 പുസ്തകങ്ങൾ വരിയിൽ കാണിക്കാനുമുള്ള CSS
        mobile_fix_css = """
        /* Mobile Header & 2-Column Grid Fix - Thripudi */
        @media (max-width: 768px) {
            header {
                height: auto !important;
                min-height: 120px !important; /* ഹെഡറിന് കൂടുതൽ ഉയരം നൽകി */
                padding: 20px 0 !important;
                position: relative !important;
                display: block !important;
            }
            .navbar {
                display: flex !important;
                flex-direction: column !important;
                align-items: center !important;
                gap: 10px !important;
            }
            .logo-container {
                margin-bottom: 10px !important;
                justify-content: center !important;
                width: 100% !important;
            }
            .logo-text {
                font-size: 1.4em !important; /* പേര് വ്യക്തമായി കാണാൻ */
                display: block !important;
                margin-top: 5px !important;
            }
            .nav-links {
                width: 100% !important;
                justify-content: center !important;
                flex-wrap: wrap !important;
            }
            .nav-item {
                font-size: 0.75em !important;
                padding: 5px 8px !important;
            }
            /* ഒരു വരിയിൽ രണ്ട് പുസ്തകങ്ങൾ */
            .library-container {
                grid-template-columns: repeat(2, 1fr) !important;
                gap: 12px !important;
                padding: 10px !important;
            }
            .image-wrapper {
                height: 220px !important; /* 2 പുസ്തകം വരുമ്പോൾ ഹൈറ്റ് അല്പം കുറച്ചു */
            }
            .book-title {
                font-size: 0.8em !important;
                height: 3em !important;
            }
        }
        """
        
        # </style> ടാഗിന് മുൻപായി പുതിയ CSS ചേർക്കുന്നു
        if '</style>' in content:
            updated_content = content.replace('</style>', mobile_fix_css + '\n    </style>')
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            return True
        return False
        
    except Exception as e:
        print(f"Error in {os.path.basename(filepath)}: {e}")
        return False

# മെയിൻ പ്രോഗ്രാം
if __name__ == "__main__":
    if not os.path.exists(directory):
        print("ഫോൾഡർ പാത്ത് പരിശോധിക്കുക.")
    else:
        count = 0
        for filename in os.listdir(directory):
            if filename.lower().endswith(('.html', '.htm')):
                if fix_mobile_view_v2(os.path.join(directory, filename)):
                    print(f"അപ്ഡേറ്റ് ചെയ്തു: {filename}")
                    count += 1
        print(f"\nവിജയകരമായി {count} പേജുകൾ ശരിയാക്കി.")