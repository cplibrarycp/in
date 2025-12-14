import os
import re

# ================= സെറ്റിംഗ്സ് =================
# നിങ്ങളുടെ HTML ഫയലുകൾ ഉള്ള ഫോൾഡർ പാത്ത് ഇവിടെ നൽകുക
target_folder = r"L:\test" 
# ============================================

# പുതിയ ജാവാസ്ക്രിപ്റ്റ് & HTML (Full Page PDF + Name Fix)
NEW_CONTENT = """
    <div id="pdfModal" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:#fff; z-index:9999; flex-direction:column;">
        <div style="background:#004D40; color:white; padding:15px; display:flex; justify-content:space-between; align-items:center; box-shadow:0 2px 5px rgba(0,0,0,0.2);">
            <span style="font-family:'Poppins',sans-serif; font-weight:600; font-size:1.1em;"> <i class="fas fa-book-reader"></i> Reading Mode</span>
            <button onclick="closePdfModal()" style="background:transparent; border:none; color:white; font-size:1.2em; cursor:pointer; padding:0 10px;">
                <i class="fas fa-times"></i> Close
            </button>
        </div>
        <iframe id="pdfFrame" style="width:100%; flex:1; border:none; display:block;"></iframe>
    </div>

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
                // --- 1. USER NAME SYNC FIX ---
                // പേജ് ലോഡ് ആകുമ്പോൾ തന്നെ വിവരങ്ങൾ നിർബന്ധമായും പുതുക്കുന്നു
                try { 
                    await user.reload(); 
                } catch(e) { 
                    console.log("Auto-reload error, using cached data"); 
                }
                
                // ഫയർബേസിൽ നിന്ന് ഏറ്റവും പുതിയ വിവരം എടുക്കുന്നു
                const currentUser = auth.currentUser; 
                
                // പേര് ഡിസ്പ്ലേ ചെയ്യുന്നു
                const displayName = currentUser.displayName ? currentUser.displayName.split(' ')[0] : currentUser.email.split('@')[0];
                if(nameDisplay) nameDisplay.textContent = displayName;
                
                // ഫോട്ടോ ഡിസ്പ്ലേ ചെയ്യുന്നു
                if (currentUser.photoURL && avatarDiv) {
                    avatarDiv.innerHTML = `<img src="${currentUser.photoURL}" alt="Profile">`;
                }

                // --- 2. SETUP CLICKS ---
                setupInteractions(user.uid);

            } else {
                // ലോഗിൻ ചെയ്തിട്ടില്ലെങ്കിൽ ഇൻഡക്സ് പേജിലേക്ക്
                if (!window.location.pathname.includes("index.html")) {
                     window.location.href = "index.html";
                }
            }
        });

        const logoutLink = document.getElementById('logout-link');
        if(logoutLink) {
            logoutLink.addEventListener('click', (e) => { 
                e.preventDefault(); 
                signOut(auth).then(() => { window.location.href = "index.html"; }); 
            });
        }

        // --- GLOBAL FUNCTIONS ---
        window.setupInteractions = function(uid) {
            const buttons = document.querySelectorAll(".overlay-btn");
            buttons.forEach(btn => {
                // പഴയ ഇവന്റുകൾ നീക്കം ചെയ്ത് പുതിയത് ചേർക്കുന്നു
                const newBtn = btn.cloneNode(true);
                btn.parentNode.replaceChild(newBtn, btn);
                
                newBtn.addEventListener("click", function(e) {
                    e.preventDefault(); // പുതിയ ടാബിൽ തുറക്കുന്നത് തടയുന്നു
                    
                    const card = this.closest('.book-card');
                    const linkUrl = this.getAttribute('href');
                    
                    // History Saving
                    if (card) {
                        const title = card.querySelector('.book-title').innerText;
                        const image = card.querySelector('.book-cover').src;
                        const date = new Date().toLocaleDateString('ml-IN');
                        
                        const key = 'history_' + uid;
                        let history = JSON.parse(localStorage.getItem(key)) || [];
                        history = history.filter(item => item.title !== title); // Remove duplicate
                        history.unshift({ title, image, url: linkUrl, date });
                        if (history.length > 50) history.pop();
                        localStorage.setItem(key, JSON.stringify(history));
                    }

                    // Open Full Page PDF
                    openPdfModal(linkUrl);
                });
            });
        };
    </script>

    <script>
        // --- FULL PAGE PDF LOGIC ---
        function openPdfModal(url) {
            const modal = document.getElementById('pdfModal');
            const frame = document.getElementById('pdfFrame');
            
            // Drive Link Conversion (Preview Mode)
            let embedUrl = url;
            if(url.includes("view") || url.includes("preview")) {
                embedUrl = url.replace(/\/view.*/, "/preview").replace(/\/preview.*/, "/preview");
            }
            
            frame.src = embedUrl;
            modal.style.display = "flex"; // Flex ഉപയോഗിച്ചാണ് ഫുൾ പേജ് സെറ്റ് ചെയ്യുന്നത്
            document.body.style.overflow = "hidden"; // പിന്നിലെ പേജ് സ്ക്രോൾ ആവാതിരിക്കാൻ
        }

        function closePdfModal() {
            const modal = document.getElementById('pdfModal');
            const frame = document.getElementById('pdfFrame');
            
            modal.style.display = "none";
            frame.src = ""; 
            document.body.style.overflow = "auto"; // സ്ക്രോൾ തിരികെ കൊണ്ടുവരുന്നു
        }

        function toggleProfileMenu() { 
            var dropdown = document.querySelector(".profile-dropdown"); 
            if(dropdown) dropdown.style.display = dropdown.style.display === "block" ? "none" : "block"; 
        }
        
        // ക്ലിക്ക് ഔട്ട്സൈഡ് (Dropdown Close)
        window.onclick = function(event) {
            if (!event.target.closest('.user-profile')) {
                var dropdowns = document.getElementsByClassName("profile-dropdown");
                for (var i = 0; i < dropdowns.length; i++) {
                    dropdowns[i].style.display = "none";
                }
            }
        }
        
        function searchBooks() { var input = document.getElementById('searchBar'); if(!input) return; var filter = input.value.toUpperCase(); var cards = document.getElementsByClassName('book-card'); for (var i = 0; i < cards.length; i++) { var title = cards[i].getElementsByClassName("book-title")[0]; if (title) { var txtValue = title.textContent || title.innerText; cards[i].style.display = txtValue.toUpperCase().indexOf(filter) > -1 ? "" : "none"; } } }
    </script>
</body>
</html>
"""

def update_html_files():
    print(f"Scanning folder: {target_folder}...")
    
    count = 0
    for root, dirs, files in os.walk(target_folder):
        for file in files:
            if file.lower().endswith(".html"):
                # ഈ ഫയലുകളെ ഒഴിവാക്കുന്നു (കാരണം ഇവയ്ക്ക് വേറെ ലോജിക് ആണ്)
                if file.lower() in ["index.html", "history.html", "profile.html", "register.html", "dashboard.html"]:
                    print(f"Skipping core file: {file}")
                    continue

                file_path = os.path.join(root, file)
                print(f"Updating: {file}")

                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # പഴയ സ്ക്രിപ്റ്റുകൾ കണ്ടെത്തി നീക്കം ചെയ്ത് പുതിയത് ചേർക്കുന്നു
                    # ഇത് <footer> കഴിഞ്ഞ് വരുന്ന എല്ലാ സ്ക്രിപ്റ്റുകളെയും മാറ്റും
                    
                    pattern = r'(?s)<div id="pdfModal".*?</html>|(?s)<script type="module">.*?</html>'
                    
                    # സ്ക്രിപ്റ്റ് ഉണ്ടെങ്കിൽ അത് റീപ്ലേസ് ചെയ്യുന്നു
                    if re.search(pattern, content):
                        new_content = re.sub(pattern, NEW_CONTENT, content)
                    else:
                        # സ്ക്രിപ്റ്റ് കണ്ടില്ലെങ്കിൽ ബോഡി ക്ലോസ് ചെയ്യുന്നതിന് തൊട്ടുമുൻപ് ചേർക്കുന്നു
                        new_content = content.replace("</body>", NEW_CONTENT.replace("</body>\n</html>", "") + "</body>")
                        new_content = new_content + "\n</html>"
                        
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    
                    count += 1
                    print(f"  [Success] Updated {file}")

                except Exception as e:
                    print(f"  [Error] Failed to update {file}: {e}")

    print("-" * 30)
    print(f"Completed! Total {count} book pages updated.")

if __name__ == "__main__":
    if os.path.exists(target_folder):
        update_html_files()
    else:
        print("Error: നൽകിയ ഫോൾഡർ പാത്ത് നിലവിലില്ല.")