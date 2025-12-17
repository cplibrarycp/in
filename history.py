import os
import re

# ================= സെറ്റിംഗ്സ് =================
target_folder = "."  # നിങ്ങളുടെ HTML ഫയലുകൾ ഉള്ള ഫോൾഡർ
# ============================================

# ഏറ്റവും സുരക്ഷിതമായ പുതിയ ഹിസ്റ്ററി സേവിംഗ് ലോജിക്
# ഇത് ബട്ടണുകളെ ബാധിക്കില്ല.
CORRECT_HISTORY_LOGIC = """
    function saveToHistory(element, bookId) {
        try {
            // Firebase ലോഗിൻ ഉണ്ടോ എന്ന് നോക്കുന്നു
            const userId = (window.currentUser) ? window.currentUser.uid : 'default_user';
            
            const card = element.closest('.book-card');
            if (!card) return;

            const title = card.querySelector('.book-title').innerText;
            const imgTag = card.querySelector('.book-cover');
            const image = imgTag ? imgTag.src : '';
            const date = new Date().toLocaleDateString('ml-IN');
            
            const key = 'history_' + userId;
            let history = JSON.parse(localStorage.getItem(key)) || [];
            
            history = history.filter(item => item.title !== title);
            history.unshift({ title: title, image: image, link: 'read.html?bookId=' + bookId, date: date });
            
            if (history.length > 50) history.pop();
            localStorage.setItem(key, JSON.stringify(history));
            console.log("History Updated for:", userId);
        } catch (e) {
            console.log("History Error:", e);
        }
    }
"""

def fix_all_files():
    print(f"നിങ്ങളുടെ ഫയലുകൾ പരിശോധിക്കുന്നു...")
    
    files = [f for f in os.listdir(target_folder) if f.endswith('.html')]
    
    for filename in files:
        if filename in ["history.html", "index.html", "profile.html", "dashboard.html", "login.html"]:
            continue
            
        file_path = os.path.join(target_folder, filename)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 1. ആദ്യം തെറ്റായ കോഡ് നീക്കം ചെയ്യുന്നു (Clean up)
            # function saveToHistory എന്ന് തുടങ്ങുന്ന ഏത് കോഡും ഇത് മാറ്റും
            clean_pattern = re.compile(r'function\s+saveToHistory\s*\(.*?\)\s*\{.*?\}', re.DOTALL)
            content = clean_pattern.sub("", content)

            # 2. ഇപ്പോൾ ശരിയായ കോഡ് </script> ടാഗിന് തൊട്ടുമുകളിൽ ചേർക്കുന്നു
            if "</script>" in content:
                # ആദ്യത്തെ </script> കണ്ടുപിടിച്ച് അതിന് മുൻപിലായി ചേർക്കുന്നു
                new_content = content.replace("</script>", CORRECT_HISTORY_LOGIC + "\n</script>", 1)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"✅ ഫിക്സ് ചെയ്തു: {filename}")
            else:
                print(f"⚠️ സ്ക്രിപ്റ്റ് ടാഗ് കാണുന്നില്ല: {filename}")

        except Exception as e:
            print(f"❌ പിശക് {filename}: {e}")

if __name__ == "__main__":
    fix_all_files()
    print("\nഎല്ലാ ഫയലുകളും ശരിയാക്കിയിട്ടുണ്ട്. ഇനി ബട്ടൺ പ്രവർത്തിക്കും.")