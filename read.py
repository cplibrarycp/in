import os
import re

# ================= സെറ്റിംഗ്സ് =================
target_folder = r"L:\html"  # നിങ്ങളുടെ ഫോൾഡർ പാത്ത്
# ============================================

# പുതിയ ക്ലീൻ സ്ക്രിപ്റ്റ് (History മാത്രം സേവ് ചെയ്യും, Modal ഇല്ല)
CLEAN_SCRIPT = """
    <script type="module">
        import { initializeApp } from "https://www.gstatic.com/firebasejs/9.15.0/firebase-app.js";
        import { getAuth, onAuthStateChanged, signOut } from "https://www.gstatic.com/firebasejs/9.15.0/firebase-auth.js";

        const firebaseConfig = { apiKey: "AIzaSyBzwhpHmeZdLf_nZrcPQirlnpj3Vhg9EqA", authDomain: "thripudilibrary.firebaseapp.com", projectId: "thripudilibrary", storageBucket: "thripudilibrary.firebasestorage.app", messagingSenderId: "887018912750", appId: "1:887018912750:web:cc05190a72b13db816acff", measurementId: "G-B59RDW4KG4" };
        const app = initializeApp(firebaseConfig); 
        const auth = getAuth(app);

        onAuthStateChanged(auth, async (user) => {
            const nameDisplay = document.getElementById('display-name');
            const avatarDiv = document.getElementById('userAvatar');

            if (user) {
                try { await user.reload(); } catch(e) {}
                const currentUser = auth.currentUser;
                const displayName = currentUser.displayName ? currentUser.displayName.split(' ')[0] : currentUser.email.split('@')[0];
                if(nameDisplay) nameDisplay.textContent = displayName;
                if (currentUser.photoURL && avatarDiv) avatarDiv.innerHTML = `<img src="${currentUser.photoURL}" alt="Profile">`;

                setupHistoryOnly(user.uid);
            }
        });

        const logoutLink = document.getElementById('logout-link');
        if(logoutLink) {
            logoutLink.addEventListener('click', (e) => { 
                e.preventDefault(); 
                signOut(auth).then(() => { window.location.href = "index.html"; }); 
            });
        }

        window.setupHistoryOnly = function(uid) {
            const buttons = document.querySelectorAll(".overlay-btn");
            buttons.forEach(btn => {
                const newBtn = btn.cloneNode(true);
                btn.parentNode.replaceChild(newBtn, btn);
                
                newBtn.addEventListener("click", function(e) {
                    // ഇവിടെ preventDefault ഇല്ല, കാരണം read.html ലേക്ക് പോകണം
                    const card = this.closest('.book-card');
                    const linkUrl = this.getAttribute('href'); // read.html link
                    
                    if (card) {
                        const title = card.querySelector('.book-title').innerText;
                        const image = card.querySelector('.book-cover').src;
                        const date = new Date().toLocaleDateString('ml-IN');
                        const key = 'history_' + uid;
                        let history = JSON.parse(localStorage.getItem(key)) || [];
                        history = history.filter(item => item.title !== title);
                        history.unshift({ title, image, url: linkUrl, date });
                        if (history.length > 50) history.pop();
                        localStorage.setItem(key, JSON.stringify(history));
                    }
                });
            });
        };
    </script>
    <script>
        function toggleProfileMenu() { 
            var dropdown = document.querySelector(".profile-dropdown"); 
            if(dropdown) dropdown.style.display = dropdown.style.display === "block" ? "none" : "block"; 
        }
        window.onclick = function(event) {
            if (!event.target.closest('.user-profile')) {
                var dropdowns = document.getElementsByClassName("profile-dropdown");
                for (var i = 0; i < dropdowns.length; i++) { dropdowns[i].style.display = "none"; }
            }
        }
        function searchBooks() { var input = document.getElementById('searchBar'); if(!input) return; var filter = input.value.toUpperCase(); var cards = document.getElementsByClassName('book-card'); for (var i = 0; i < cards.length; i++) { var title = cards[i].getElementsByClassName("book-title")[0]; if (title) { var txtValue = title.textContent || title.innerText; cards[i].style.display = txtValue.toUpperCase().indexOf(filter) > -1 ? "" : "none"; } } }
    </script>
</body>
</html>
"""

def revert_to_read_html():
    print(f"Scanning folder: {target_folder}...")
    
    # 1. Regex to find Google Drive Links and convert to read.html
    # Finds: href="https://drive.google.com/file/d/ID/preview"
    # Replaces with: href="read.html?id=ID"
    link_pattern = re.compile(r'href=["\']https://drive\.google\.com/file/d/([a-zA-Z0-9_-]+)/(?:preview|view).*?["\']')
    
    # 2. Regex to remove the Modal Div
    modal_pattern = re.compile(r'<div id="pdfModal".*?</div>', re.DOTALL)

    # 3. Regex to replace the Script block
    script_pattern = re.compile(r'<script type="module">[\s\S]*?</html>', re.DOTALL)

    for root, dirs, files in os.walk(target_folder):
        for file in files:
            if file.lower().endswith(".html"):
                if file.lower() in ["index.html", "read.html"]:
                    continue # Skip these files

                file_path = os.path.join(root, file)
                print(f"Processing: {file}")

                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # A. ലിങ്കുകൾ മാറ്റുന്നു
                    new_content = link_pattern.sub(r'href="read.html?id=\1" target="_blank"', content)
                    
                    # B. Modal Div കളയുന്നു
                    new_content = modal_pattern.sub('', new_content)

                    # C. സ്ക്രിപ്റ്റ് അപ്ഡേറ്റ് ചെയ്യുന്നു
                    if re.search(script_pattern, new_content):
                        new_content = re.sub(script_pattern, CLEAN_SCRIPT, new_content)
                    else:
                        # സ്ക്രിപ്റ്റ് കണ്ടില്ലെങ്കിൽ അവസാനം ചേർക്കുന്നു
                        new_content = new_content.replace("</body>", CLEAN_SCRIPT.replace("</body>\n</html>", "") + "</body>")
                        new_content = new_content + "\n</html>"

                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    
                    print(f"  [Updated] {file}")

                except Exception as e:
                    print(f"  [Error] {file}: {e}")

    print("-" * 30)
    print("All files reverted to read.html style!")

if __name__ == "__main__":
    if os.path.exists(target_folder):
        revert_to_read_html()
    else:
        print("Error: നൽകിയ ഫോൾഡർ പാത്ത് നിലവിലില്ല.")