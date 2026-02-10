import streamlit as st
import random
import time
from st_keyup import st_keyup

# --- PAGE CONFIG ---
st.set_page_config(page_title="Ian's Arcade", page_icon="", layout="centered")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .main { background-color: #fff0f3; }
    .stButton>button { width: 100%; border-radius: 20px; border: 2px solid #ff4d6d; background-color: white; color: #ff4d6d; font-weight: bold; }
    .stButton>button:hover { background-color: #ff4d6d; color: white; }
    h1, h2, h3 { color: #c9184a; }
    .stProgress > div > div > div > div { background-color: #ff4d6d; }
    </style>
    """, unsafe_allow_html=True)

# --- INITIALIZE GLOBAL STATE ---
if 'fragments' not in st.session_state:
    st.session_state.fragments = set()
if 'heart_forged' not in st.session_state:
    st.session_state.heart_forged = False

# --- HOME / WELCOME PAGE ---
def welcome_page():
    st.title("💔 The Heart Fragment Quest")
    st.markdown("""
    ### Welcome,
    To unlock the finale, you must recover **4 Heart Fragments**. 
    Each game masters a different side of romance. Collect them all to forge the heart!
    """)
    st.divider()
    
    # Progress Display
    num_frags = len(st.session_state.fragments)
    st.subheader(f"Heart Fragments: {num_frags} / 4")
    
    heart_display = ["🤍", "🤍", "🤍", "🤍"]
    for i in range(num_frags):
        heart_display[i] = "❤️"
    st.markdown(f"## {' '.join(heart_display)}")

    if num_frags == 4 and not st.session_state.heart_forged:
        st.success("✨ All fragments collected! You are ready to forge the heart.")
        if st.button("🔨 FORGE THE HEART"):
            st.session_state.heart_forged = True
            st.balloons()
            st.rerun()
    elif st.session_state.heart_forged:
        st.success("💖 The Heart is whole! The FINALE is now unlocked in the sidebar.")
    else:
        st.info("👈 Select a challenge from the sidebar to find fragments!")

# --- GAME 1: TYPE RACER ---
def type_racer():
    st.header("❤️‍🔥 Heartbeat Racer")
    phrases = [
        "Love looks not with the eyes, but with the mind",
        "You are the moon to my night",
        "Sweetheart.exe is running",
        "Did the sun come out or did you just smile at me",
        "Your hand looks heavy, can I hold it for you?"
    ]
    if 'phrase_idx' not in st.session_state:
        st.session_state.phrase_idx = 0
        st.session_state.start_time = None

    target = phrases[st.session_state.phrase_idx]
    st.subheader(f"Level {st.session_state.phrase_idx + 1} of {len(phrases)}")
    st.markdown(f"### **Type this:** `{target}`")
    
    user_input = st_keyup("Type with your heart...", key=f"keyup_{st.session_state.phrase_idx}")

    # Correct character tracking
    correct_chars = 0
    for i in range(min(len(user_input), len(target))):
        if user_input[i] == target[i]: correct_chars += 1
        else: break 

    progress_val = correct_chars / len(target)
    st.progress(progress_val, text=f"Syncing... {int(progress_val * 100)}%")

    if user_input:
        if st.session_state.start_time is None:
            st.session_state.start_time = time.time()
        elapsed = time.time() - st.session_state.start_time
        if elapsed > 0:
            wpm = int((len(user_input) / 5) / (elapsed / 60))
            st.metric("Live Speed", f"{wpm} WPM")

    if user_input == target:
        if st.session_state.phrase_idx < len(phrases) - 1:
            st.balloons()
            st.session_state.phrase_idx += 1
            st.session_state.start_time = None
            st.rerun()
        else:
            st.session_state.fragments.add("Type Racer")
            st.success("🔥 Fragment Obtained! You've mastered the rhythm.")
            if st.button("Back to Home"): st.rerun()

# --- GAME 2: POTION LAB ---
def potion_game():
    st.header("🧪 Love Potion Alchemist")
    shelf = {
        "Rose Petals": (10, 0, 2), "Chili Peppers": (2, 12, 5),
        "Dark Chocolate": (8, 5, 1), "Sparkling Starlight": (5, 5, 10),
        "Awkward Silence": (0, 0, 15), "Puppy Ears": (15, 0, 0)
    }

    # Initialize result storage if it doesn't exist
    if 'potion_result' not in st.session_state:
        st.session_state.potion_result = None

    choices = st.multiselect("Pick 3 ingredients to define your vibe:", list(shelf.keys()), max_selections=3)
    
    col1, col2 = st.columns(2)
    
    if col1.button("Brew Potion"):
        if len(choices) == 3:
            sweet = sum(shelf[c][0] for c in choices)
            spice = sum(shelf[c][1] for c in choices)
            chaos = sum(shelf[c][2] for c in choices)
            
            # --- EXTENDED PERSONALITY ARCHETYPES ---
            if chaos > 22:
                name = "THE COSMIC WILDCARD 🌪️"
                style = "error"
                details = """
                **Your Vibe:** Unpredictable, hilarious, and genuinely one-of-a-kind.  
                **Personality Traits:**
                * **Adaptability:** You can turn a flat tire into a roadside picnic without missing a beat.
                * **Spontaneity:** You thrive in the 'weird' moments that others might find awkward.
                * **Fearlessness:** You aren't afraid to be your authentic, chaotic self.
                """
            elif sweet > 25:
                name = "THE RADIANT ROMANTIC 🍬"
                style = "success"
                details = """
                **Your Vibe:** Warm, comforting, and deeply thoughtful.  
                **Personality Traits:**
                * **Empathy:** You have a superpower for making people feel seen and heard.
                * **Sincerity:** You actually mean the nice things you say (a rare trait!).
                * **Optimism:** You find the beauty in the small, quiet moments.
                """
            elif spice > 20:
                name = "THE DYNAMIC ADVENTURER 🔥"
                style = "warning"
                details = """
                **Your Vibe:** Bold, high-energy, and charismatic.  
                **Personality Traits:**
                * **Confidence:** You lead with your heart and take big swings in life.
                * **Passion:** When you care about something, you give it 110%.
                * **Wit:** Your conversation is sharp, fast-paced, and never boring.
                """
            else:
                name = "THE ZEN ANCHOR ☕"
                style = "info"
                details = """
                **Your Vibe:** Grounded, peaceful, and effortlessly cool.  
                **Personality Traits:**
                * **Reliability:** You are the person people turn to when the world gets too loud.
                * **Mindfulness:** You appreciate quality over quantity in everything you do.
                * **Subtle Humor:** You don't need to shout to be the funniest person in the room.
                """
            
            # Save to session state so it persists
            st.session_state.potion_result = {
                "name": name, 
                "style": style, 
                "details": details, 
                "stats": f"Sweetness: {sweet} | Spice: {spice} | Chaos: {chaos}"
            }
            st.session_state.fragments.add("Potion Lab")
            st.balloons()
        else:
            st.warning("Please pick exactly 3 ingredients to brew!")

    if col2.button("Reset Lab"):
        st.session_state.potion_result = None
        st.rerun()

    # --- PERSISTENT DISPLAY LOGIC ---
    if st.session_state.potion_result:
        res = st.session_state.potion_result
        st.divider()
        
        # Display the box based on style
        if res["style"] == "error": st.error(res["name"])
        elif res["style"] == "success": st.success(res["name"])
        elif res["style"] == "warning": st.warning(res["name"])
        else: st.info(res["name"])
        
        st.markdown(res["details"])
        st.caption(res["stats"])
        st.write("✨ **Fragment Obtained!** You can find it on the Home page.")

# --- GAME 3: Vamp BATTLE ---
def rpg_battle():
    st.header("⚔️ Battle for Romance")
    import base64 

    # --- 1. MEDIA CONFIGURATION ---
    # Add your "Dead Vampire" filename here
    gifs = {
        "start": "vampire_start.gif",   
        "idle": "vampire_idle.gif",     
        "damage": "vampire_ouch.gif",
        "win": "vampire_dead.png"  # <--- NEW: Image to show on victory
    }

    # --- HELPER: RENDER MEDIA CENTERED & SIZED ---
    def show_animated_gif(filename, width=300):
        try:
            with open(filename, "rb") as f:
                contents = f.read()
                data_url = base64.b64encode(contents).decode("utf-8")
                st.markdown(
                    f'<div style="display: flex; justify-content: center;">'
                    f'<img src="data:image/gif;base64,{data_url}" width="{width}">'
                    f'</div>',
                    unsafe_allow_html=True,
                )
        except FileNotFoundError:
            st.error(f"⚠️ Missing file: {filename}")

    # --- 2. STATE INITIALIZATION ---
    if 'php' not in st.session_state:
        st.session_state.php = 50
        st.session_state.bhp = 50
        st.session_state.battle_state = "start" 
        st.session_state.last_action = "The Vampire is waiting..."
        st.session_state.show_damage_gif = False

    # --- 3. THE START SCREEN ---
    if st.session_state.battle_state == "start":
        show_animated_gif(gifs["start"], width=300)
        st.markdown("""
        ### A Wild Vampire appeared!
        They don't believe in true love or joy. They think Valentine's Day is a corporate scam.
        **Your Mission:** Melt their icy heart before they drain your optimism.
        """)
        if st.button("⚔️ FIGHT!"):
            st.session_state.battle_state = "fighting"
            st.rerun()
        return

    # --- 4. END GAME CHECKS ---
    
    # Heroic Sacrifice
    if st.session_state.bhp <= 0 and st.session_state.php <= 0:
        st.session_state.fragments.add("Vamp Battle")
        
        # Show the "Dead" image here too if you want, or keep it text only
        show_animated_gif(gifs["win"], width=300) 
        
        st.info("🌹 THE SUPREME SACRIFICE 🌹")
        st.balloons()
        st.success("You defeated the Vampire, but the battle took everything you had.")
        st.markdown("""
        **Rest in Peace, Legend.** By dealing the final blow at the cost of your own heart, you **died a Valentine Hero**. 
        """)
        if st.button("Ascend to Romance Heaven (Reset)"):
            del st.session_state.php 
            del st.session_state.battle_state
            st.rerun()
        return

    # Standard Victory
    elif st.session_state.bhp <= 0:
        st.session_state.fragments.add("Vamp Battle")
        
        # --- SHOW THE DEAD VAMPIRE IMAGE ---
        show_animated_gif(gifs["win"], width=300)
        
        st.balloons()
        st.success("💖 VICTORY! The Vampire's heart has melted!")
        if st.button("Play Again"):
            del st.session_state.php
            del st.session_state.battle_state
            st.rerun()
        return

    # Standard Defeat
    elif st.session_state.php <= 0:
        st.error("💔 DEFEAT! The Vampire's bloodthirst was too powerful.")
        if st.button("Try Again"):
            del st.session_state.php
            del st.session_state.battle_state
            st.rerun()
        return

    # --- 5. THE BATTLE INTERFACE (Active Fight) ---
    
    # Logic: Show 'Damage' GIF if they just got hit, otherwise 'Idle'
    current_gif = gifs["damage"] if st.session_state.show_damage_gif else gifs["idle"]
    show_animated_gif(current_gif, width=300)

    # Health Bars
    display_bhp = max(0, st.session_state.bhp)
    display_php = max(0, st.session_state.php)
    st.progress(display_bhp / 50, text=f"Vampire Health: {display_bhp}")
    st.progress(display_php / 50, text=f"Your Health: {display_php}")

    # --- 6. COMBAT CONTROLS ---
    st.subheader("Select Your Move:")
    st.caption(f"Last Turn: {st.session_state.last_action}")
    
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)
    
    player_move = False
    
    # Reset flag
    if st.session_state.show_damage_gif:
        st.session_state.show_damage_gif = False

    if col1.button("📩 Sweet Text (Low Risk)"):
        dmg = random.randint(5, 8)
        st.session_state.bhp -= dmg
        st.session_state.last_action = f"Sent a sweet text! Dealt {dmg} damage."
        st.session_state.show_damage_gif = True
        player_move = True
    
    elif col2.button("💐 Surprise Bouquet (Mid Risk)"):
        if random.random() > 0.2: 
            dmg = random.randint(12, 18)
            st.session_state.bhp -= dmg
            st.session_state.last_action = f"Bouquet hit! Dealt {dmg} damage."
            st.session_state.show_damage_gif = True
        else:
            st.session_state.last_action = "Missed! They have pollen allergies."
        player_move = True

    elif col3.button("🎸 Public Serenade (High Risk)"):
        if random.random() > 0.6: 
            dmg = random.randint(35, 48)
            st.session_state.bhp -= dmg
            st.session_state.last_action = f"SERENADE HIT! Massive {dmg} damage!"
            st.session_state.show_damage_gif = True
        else:
            st.session_state.last_action = "Cringe! You forgot the lyrics."
        player_move = True

    elif col4.button("🎲 Blind Date (Chaotic Risk)"):
        st.session_state.php -= 15
        st.session_state.bhp -= 15
        st.session_state.last_action = "Chaos! Both took 15 damage."
        st.session_state.show_damage_gif = True
        player_move = True

    # --- 7. ENEMY TURN & REFRESH ---
    if player_move:
        if st.session_state.bhp > 0:
            boss_dmg = random.randint(8, 14)
            st.session_state.php -= boss_dmg
            st.session_state.last_action += f" | Vampire hit you for {boss_dmg}."
        
        st.rerun()

# --- GAME 4: DATE SIMULATOR ---
def date_sim():
    st.header("🥀 Chaotic Date Simulator")
    if 'date_step' not in st.session_state: st.session_state.date_step = 0

    # STEP 0: THE ORDER
    if st.session_state.date_step == 0:
        st.write("The waiter arrives. He is wearing a monocle. What do you order?")
        if st.button("A single lukewarm spaghetti noodle and two spoons"): st.session_state.date_step = -1
        if st.button("The 'Mystery Bucket' (Don't ask, don't tell)"): st.session_state.date_step = 1
        if st.button("I'll have what the restaurant's cat is having"): st.session_state.date_step = 1

    # STEP 1: THE CAREER
    elif st.session_state.date_step == 1:
        st.write("Your date is intrigued. 'So,' they ask, 'how do you pay for all this mystery food?'")
        if st.button("I'm an undercover agent for an Alien Rebellion"): st.session_state.date_step = 2
        if st.button("I'm a professional Cloud-Watcher and part-time ghost hunter"): st.session_state.date_step = 2
        if st.button("I'm an Aquatic Structural Systems Engineer (plumber)"): st.session_state.date_step = -1

    # STEP 2: THE MUSIC
    elif st.session_state.date_step == 2:
        st.write("Your date gets nervous, so they throw an icebreaker at you: 'What would you rather have to listen to 24/7?'")
        if st.button("A rock band playing classical music"): st.session_state.date_step = 3
        if st.button("Dramatic thunder every time you turn your head"): st.session_state.date_step = 3
        if st.button("Aggressive beatboxing during moments of complete silence"): st.session_state.date_step = -1

    # STEP 3: WOULD YOU RATHER
    elif st.session_state.date_step == 3:
        st.write("The vibe is getting weird. Your date asks: 'Would you rather...'")
        if st.button("Have a cat that knows all your secrets and occasionally hint at them"): 
            st.session_state.date_step = 4; st.rerun()
        if st.button("Hear inner thoughts very loudly all the time"): 
            st.session_state.date_step = 4; st.rerun()
        if st.button("Have a dog that publicly overreacts to everything you do"): 
            st.session_state.date_step = -1; st.rerun()

    # STEP 4: THE BILL
    elif st.session_state.date_step == 4:
        st.write("The check arrives. It's written in ancient runes. How do you pay?")
        if st.button("Challenge the chef to a high-stakes game of Dominó"): 
            st.session_state.date_step = 5; st.rerun()
        if st.button("Pay with the restaurant's own cat in a disguise"): 
            st.session_state.date_step = 5; st.rerun()
        if st.button("Pretend to fall asleep the moment the check touches the table"): 
            st.session_state.date_step = -1; st.rerun()

    # SUCCESS
    elif st.session_state.date_step == 5:
        st.session_state.fragments.add("Date Simulator")
        st.balloons()
        st.success("🏆 VICTORY! Fragment Obtained. You're getting a second date!")
        if st.button("Return Home"): 
            st.session_state.date_step = 0; st.rerun()

    # GAME OVER
    elif st.session_state.date_step == -1:
        st.error("💀 GAME OVER: Ghosted!")
        if st.button("Try Again"): 
            st.session_state.date_step = 0; st.rerun()

# --- FINALE ---
def finale():
    if not st.session_state.heart_forged:
        st.error("🔒 LOCK: Go Home and Forge the Heart first!")
        return
    st.header("💌 The Grand Reveal")
    try:
        st.image("valentine_photo.jpg", use_container_width=True, caption="Happy Valentine's Day! 🫶")
        st.balloons()
    except:
        st.error("Missing 'valentine_photo.jpg' file.")
    st.markdown("<h2 style='text-align: center; color: #c9184a;'>You are a certified romantic</h2>", unsafe_allow_html=True)

# --- SIDEBAR & ROUTING ---
st.sidebar.title("Ian's Super Cool Arcade")
menu = ["Home", "Type Racer", "Potion Lab", "Vamp Battle", "Date Simulator"]
if st.session_state.heart_forged: menu.append("FINALE")
page = st.sidebar.radio("Navigate:", menu)

if page == "Home": welcome_page()
elif page == "Type Racer": type_racer()
elif page == "Potion Lab": potion_game()
elif page == "Vamp Battle": rpg_battle()
elif page == "Date Simulator": date_sim()

elif page == "FINALE": finale()
