from nicegui import ui, app
import random
import time
import base64
import os
import asyncio

# --- 1. GLOBAL DATA ---
songs = [
    {"lyric": "Cause all of me loves all of you / Love your curves and all your edges", "artist": "John Legend", "title": "All of Me"},
    {"lyric": "And, darling, I will be loving you 'til we're 70", "artist": "Ed Sheeran", "title": "Thinking Out Loud"},
    {"lyric": "I have died every day waiting for you / Darling, don't be afraid", "artist": "Christina Perri", "title": "A Thousand Years"},
    {"lyric": "I won't give up on us / Even if the skies get rough", "artist": "Jason Mraz", "title": "I Won't Give Up"},
    {"lyric": "It's like you're my mirror / My mirror staring back at me", "artist": "Justin Timberlake", "title": "Mirrors"},
    {"lyric": "I'm off the deep end, watch as I dive in / I'll never meet the ground", "artist": "Lady Gaga & Bradley Cooper", "title": "Shallow"},
    {"lyric": "I knew I loved you then / But you'd never know", "artist": "James Arthur", "title": "Say You Won't Let Go"},
    {"lyric": "You make me feel like I'm livin' a teenage dream / The way you turn me on", "artist": "Katy Perry", "title": "Teenage Dream"},
    {"lyric": "Baby, you light up my world like nobody else", "artist": "One Direction", "title": "What Makes You Beautiful"},
    {"lyric": "When I see your face / There's not a thing that I would change", "artist": "Bruno Mars", "title": "Just the Way You Are"},
    {"lyric": "Baby, it's you / You're the one I love / You're the one I need", "artist": "Beyoncé", "title": "Love On Top"},
    {"lyric": "Hey, I just met you, and this is crazy / But here's my number", "artist": "Carly Rae Jepsen", "title": "Call Me Maybe"},
    {"lyric": "Your sugar / Yes, please / Won't you come and put it down on me?", "artist": "Maroon 5", "title": "Sugar"},
    {"lyric": "We found love in a hopeless place", "artist": "Rihanna", "title": "We Found Love"},
    {"lyric": "You're the light, you're the night / You're the color of my blood", "artist": "Ellie Goulding", "title": "Love Me Like You Do"},
    {"lyric": "Baby, why don't you just meet me in the middle?", "artist": "Zedd, Maren Morris", "title": "The Middle"},
    {"lyric": "Can I go where you go? / Can we always be this close?", "artist": "Taylor Swift", "title": "Lover"},
    {"lyric": "I'd walk through fire for you / Just let me adore you", "artist": "Harry Styles", "title": "Adore You"},
    {"lyric": "Baby, I'm dancing in the dark with you between my arms", "artist": "Ed Sheeran", "title": "Perfect"},
    {"lyric": "It's a beautiful night, we're looking for something dumb to do", "artist": "Bruno Mars", "title": "Marry You"}
]

phrases_db = [
    "Did the sun just come out or did you smile at me?",
    "Do you have a map? I keep getting lost in your eyes.",
    "Is your name Google? Because you have everything I've been searching for.",
    "Are you a magician? Because whenever I look at you, everyone else disappears.",
    "Do you believe in love at first sight, or should I walk by again?",
    "If you were a vegetable, you'd be a cute-cumber.",
    "Are you a time traveler? Because I see you in my future.",
    "I'm not a photographer, but I can picture us together."
]

# --- 2. HELPER: LOAD AUDIO AS DATA ---
def get_audio_source(filename):
    if not os.path.exists(filename):
        if filename not in ['beep.mp3', 'car.gif', 'finale.mp3']: 
            print(f"ERROR: Could not find {filename}")
        return None
    try:
        with open(filename, 'rb') as f:
            data = f.read()
        b64 = base64.b64encode(data).decode()
        return f'data:audio/mp3;base64,{b64}'
    except Exception as e:
        print(f"Error reading audio: {e}")
        return None

# --- 3. MAIN PAGE LOGIC ---
@ui.page('/')
def main_page():
    # Style configuration and head HTML
    ui.add_head_html('''
        <link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
        <style>
            body { background-color: #fff0f3; color: #881337; font-family: 'Press Start 2P', cursive; font-size: 12px; margin: 0; }
            .arcade-btn { background-color: white; border: 4px solid #be123c; color: #be123c; border-radius: 0px; font-family: 'Press Start 2P', cursive; transition: all 0.1s; box-shadow: 4px 4px 0px #be123c; }
            .arcade-btn:active { transform: translate(2px, 2px); box-shadow: 2px 2px 0px #be123c; }
            .nav-btn { width: 100%; text-align: left; justify-content: flex-start; margin-bottom: 12px; padding: 10px; font-size: 10px; }
            .typed-correct { color: #16a34a; } .typed-remain { color: #94a3b8; }   
        </style>
    ''')

    # Reset game state every time the page is loaded/refreshed
    app.storage.user['fragments'] = []
    app.storage.user['heart_forged'] = False
    app.storage.user['game_started'] = False
    
    # Audio Player Setup
    bg_source = get_audio_source('background_music.mp3')
    quiz_source = get_audio_source('quiz_music.mp3')
    finale_source = get_audio_source('finale.mp3')
    beep_source = get_audio_source('beep.mp3') 
    
    audio_player = ui.audio(bg_source or '', autoplay=False, loop=True).classes('hidden')
    beep_player = ui.audio(beep_source or '', autoplay=False).classes('hidden')
    if beep_player: beep_player.props('volume=0.5')

    def switch_music(track_type):
        if track_type == "Quiz" and quiz_source:
            audio_player.set_source(quiz_source); audio_player.play()
        elif track_type == "Finale" and finale_source:
            audio_player.set_source(finale_source); audio_player.play()
        elif bg_source:
            audio_player.set_source(bg_source); audio_player.play()

    def sound_button(text, on_click=None):
        async def click_handler():
            if beep_player: beep_player.seek(0); beep_player.play()
            if on_click:
                if asyncio.iscoroutinefunction(on_click): await on_click()
                else: on_click()       
        return ui.button(text, on_click=click_handler)

    # UI Containers
    splash_container = ui.column().classes('w-full h-screen items-center justify-center bg-rose-100 absolute top-0 left-0 z-50')
    arcade_container = ui.column().classes('w-full min-h-screen hidden')

    # --- SECRET DEV UNLOCK FUNCTION ---
    def dev_unlock():
        app.storage.user['fragments'] = ["Type Racer", "Date Sim", "Quiz"]
        app.storage.user['heart_forged'] = True
        render_drawer_finale.refresh()
        ui.notify("DEV SHORTCUT ACTIVATED 🏎️💨", type='info')
        nav("Finale")

    # Sidebar Drawer (Starts hidden)
    @ui.refreshable
    def render_drawer_finale():
        if app.storage.user.get('heart_forged', False):
            ui.separator().classes('my-4')
            sound_button('THE FINALE', on_click=lambda: nav("Finale")).classes('bg-rose-600 text-white nav-btn animate-pulse')

    with ui.left_drawer(value=False).classes('bg-rose-100 p-4') as drawer:
        ui.label("THE VALENTINE QUEST").classes('text-lg text-rose-600 mb-6')
        ui.label("MUSIC VOL").classes('text-xs text-rose-500 mb-2')
        vol_slider = ui.slider(min=0, max=1, step=0.01, value=0.5).props('color=pink label-always')
        vol_slider.on_value_change(lambda e: audio_player.props(f'volume={e.value}'))
        
        ui.label("SFX VOL").classes('text-xs text-rose-500 mt-4 mb-2')
        sfx_slider = ui.slider(min=0, max=1, step=0.01, value=0.5).props('color=pink label-always')
        sfx_slider.on_value_change(lambda e: beep_player.props(f'volume={e.value}'))
        
        ui.separator().classes('my-4')
        sound_button('HOME', on_click=lambda: nav("Home")).classes('arcade-btn nav-btn')
        sound_button('TYPE RACER', on_click=lambda: nav("Type")).classes('arcade-btn nav-btn')
        sound_button('DATE SIM', on_click=lambda: nav("Date")).classes('arcade-btn nav-btn')
        sound_button('MUSIC QUIZ', on_click=lambda: nav("Quiz")).classes('arcade-btn nav-btn')
        render_drawer_finale()

    # Arcade Main View
    with arcade_container:
        # THE GHOST BUTTON: car.gif is now a secret dev portal
        car_gif = ui.image('car.gif').classes('fixed top-4 right-4 w-32 z-50 cursor-default').on('click', dev_unlock)
        content_area = ui.column().classes('w-full p-8 items-center max-w-4xl mx-auto')

    # --- NAVIGATION LOGIC ---
    def nav(page_name):
        content_area.clear() 
        if page_name == "Finale": switch_music("Finale")
        else: switch_music("Home")
        
        # Car is hidden only in the Finale
        car_gif.set_visibility(page_name != "Finale")

        with content_area:
            if page_name == "Home": render_home()
            elif page_name == "Type": render_type_racer()
            elif page_name == "Quiz": render_quiz()
            elif page_name == "Date": render_date_sim()
            elif page_name == "Finale": render_finale()

    # (Place your Game Renderer functions here: render_home, render_type_racer, etc.)

    def render_home():
        ui.label("MISSION HEARTBREAK").classes('text-2xl text-rose-700 text-center')
        ui.label("RECOVER 3 HEART FRAGMENTS").classes('text-xs mt-4 mb-8')
        frags = len(app.storage.user['fragments'])
        if app.storage.user.get('heart_forged', False):
            ui.label("💛").classes('text-6xl my-6 animate-bounce')
            ui.label("HEART RESTORED!").classes('text-green-600 mt-4')
        else:
            hearts = "❤️ " * frags + "🤍 " * (3 - frags)
            ui.label(hearts).classes('text-3xl my-6')
            ui.label(f"COLLECTED: {frags} / 3").classes('text-sm')
        if frags >= 3 and not app.storage.user['heart_forged']:
            def forge():
                app.storage.user['heart_forged'] = True
                render_drawer_finale.refresh()
                ui.notify("HEART FORGED!", type='positive')
                nav("Home") 
            sound_button("FORGE HEART", on_click=forge).classes('bg-rose-500 text-white text-sm p-4 mt-8')
        elif not app.storage.user['heart_forged']:
            ui.label("<--SELECT GAME--").classes('text-gray-500 mt-8 text-xs')
        ui.separator().classes('my-12 w-1/2')
        async def reset_progress():
            app.storage.user['fragments'] = []
            app.storage.user['heart_forged'] = False
            if beep_player: beep_player.seek(0); beep_player.play()
            render_drawer_finale.refresh()
            drawer.set_value(False)
            arcade_container.classes(add='hidden', remove='block')
            splash_container.classes(remove='hidden')
            ui.notify("SYSTEM RESET", type='info')
        sound_button("RESET SYSTEM", on_click=reset_progress).classes('bg-gray-400 text-white text-xs px-4 py-2')

    def render_type_racer():
        ui.label("HEARTBEAT RACER").classes('text-xl mb-4')
        session_phrases = random.sample(phrases_db, 5)
        game_state = {'round': 1, 'wpm_list': [], 'start_time': 0, 'current_phrase': ""}
        
        # UI Elements
        status_row = ui.row().classes('w-full justify-between mb-4 text-xs text-rose-500')
        text_display = ui.html().classes('text-lg text-center mb-4 leading-loose p-4 bg-white border-2 border-rose-100 rounded shadow-inner')
        input_container = ui.row().classes('w-full')

        def start_round():
            input_container.clear()
            game_state['current_phrase'] = session_phrases[game_state['round'] - 1]
            game_state['start_time'] = time.time()
            
            # --- UPDATED: Visible Round Counter ---
            status_row.clear()
            with status_row:
                ui.label(f"ROUND {game_state['round']} OF 5")
            
            with input_container:
                new_input = ui.input(placeholder="TYPE HERE...").classes('w-full text-lg')
                new_input.props('autofocus')
                def on_type(e):
                    val = e.value
                    target = game_state['current_phrase']
                    matched = ""
                    for i, char in enumerate(val):
                        if i < len(target) and char == target[i]: matched += char
                        else: break 
                    text_display.set_content(f"<span class='typed-correct'>{matched}</span><span class='typed-remain'>{target[len(matched):]}</span>")
                    if val == target:
                        new_input.disable()
                        end_round()
                new_input.on_value_change(on_type)
                new_input.run_method('focus')
            text_display.set_content(f"<span class='typed-remain'>{game_state['current_phrase']}</span>")

        def end_round():
            elapsed = time.time() - game_state['start_time']
            wpm = int((len(game_state['current_phrase'])/5)/(elapsed/60))
            game_state['wpm_list'].append(wpm)
            ui.notify(f"Round {game_state['round']} Clear! Speed: {wpm} WPM", type='positive')
            if game_state['round'] < 5:
                game_state['round'] += 1
                ui.timer(1.0, start_round, once=True)
            else: show_results()

        def show_results():
            avg = sum(game_state['wpm_list']) // 5
            content_area.clear()
            with content_area:
                ui.label("RACE COMPLETE!").classes('text-2xl text-rose-600 mb-4')
                ui.label(f"AVG SPEED: {avg} WPM").classes('text-xl mb-4')
                rank = "NOVICE POET"
                if avg > 60: rank = "SPEED DEMON"
                elif avg > 40: rank = "FAST FINGERS"
                elif avg > 20: rank = "SENTIMENTAL TYPIST"
                ui.label(f"RANK: {rank}").classes('text-lg text-gray-500 mb-8 animate-pulse')
                
                # --- UPDATED: Heart Fragment Notification ---
                if "Type Racer" not in app.storage.user['fragments']:
                    app.storage.user['fragments'].append("Type Racer")
                    ui.label("FRAGMENT OBTAINED!").classes('text-xl font-bold text-green-600 mb-4 animate-bounce')
                else:
                    ui.label("ALREADY COMPLETED").classes('text-sm text-gray-400 mb-4')

                sound_button("RETURN HOME", on_click=lambda: nav("Home")).classes('arcade-btn')
        start_round()

    def render_quiz():
        state = {'score': 0, 'lives': 3, 'time': 30, 'active': False}
        session_songs = random.sample(songs, 10)
        ui.label("MUSICAL VAMPIRE").classes('text-xl text-rose-900 mb-4')
        vamp_container = ui.card().classes('w-full items-center p-4 bg-transparent no-shadow border-none')
        with vamp_container: 
            vamp_img = ui.image('vampire_idle.gif').classes('w-48 h-48 object-contain pixelated')
        start_area = ui.column().classes('items-center w-full')
        battle_area = ui.column().classes('items-center w-full hidden')
        with battle_area:
            stats = ui.row().classes('w-full justify-between mb-4 text-xs')
            with stats:
                score_lbl = ui.label(f"SCORE: 0/10")
                lives_lbl = ui.label("LIVES: ❤️❤️❤️")
                timer_lbl = ui.label("TIME: 30").classes('text-rose-600')
            lyric_card = ui.card().classes('w-full p-4 bg-white mb-4 items-center border-2 border-black')
            options_area = ui.grid(columns=1).classes('w-full gap-2')
        def tick():
            if not state['active']: return
            state['time'] -= 1
            timer_lbl.set_text(f"TIME: {state['time']}")
            if state['time'] <= 0: handle_wrong()
        timer = ui.timer(1.0, tick, active=False)
        def begin_actual_combat():
            car_gif.set_visibility(False)
            vamp_img.set_source('vampire_start.gif')
            ui.timer(2.0, finish_battle_start, once=True)
        def finish_battle_start():
            switch_music('Quiz')
            state['active'] = True
            vamp_img.set_source('vampire_start.gif') 
            start_area.classes(add='hidden')
            battle_area.classes(remove='hidden')
            timer.activate()
            next_round()
        def next_round():
            state['time'] = 30
            vamp_img.set_source('vampire_start.gif') 
            current_song = session_songs[state['score']]
            lyric_card.clear()
            with lyric_card: ui.label(f'"{current_song["lyric"]}"').classes('text-xs text-center leading-relaxed')
            correct = current_song['title']
            opts = [correct]
            while len(opts) < 4:
                s = random.choice(songs)['title']
                if s not in opts: opts.append(s)
            random.shuffle(opts)
            options_area.clear()
            with options_area:
                for opt in opts:
                    def click_handler(o=opt): check_answer(o, correct)
                    sound_button(opt, on_click=click_handler).classes('arcade-btn h-12 text-xs')
        def check_answer(selected, correct):
            if selected == correct:
                vamp_img.set_source('vampire_ouch.gif')
                state['score'] += 1
                score_lbl.set_text(f"SCORE: {state['score']}/10")
                ui.notify("HIT!", type='positive')
                if state['score'] >= 10: win_quiz()
                else: ui.timer(1.2, next_round, once=True)
            else: handle_wrong()
        def handle_wrong():
            state['lives'] -= 1
            lives_lbl.set_text("HP: " + "❤️" * state['lives'])
            ui.notify("MISS!", type='negative')
            if state['lives'] <= 0: lose_quiz()
            else: next_round()
        def win_quiz():
            state['active'] = False
            timer.cancel()
            content_area.clear()
            with content_area:
                ui.image('vampire_dead.png').classes('w-48 h-48 object-contain mb-4 animate-bounce')
                ui.label("FRAGMENT OBTAINED!").classes('text-xl text-green-600 mb-4')
                if "Quiz" not in app.storage.user['fragments']: app.storage.user['fragments'].append("Quiz")
                sound_button("RETURN", on_click=lambda: nav("Home")).classes('arcade-btn mt-8')
        def lose_quiz():
            state['active'] = False
            timer.cancel()
            content_area.clear()
            with content_area:
                ui.label("GAME OVER").classes('text-2xl text-gray-700 mb-4')
                sound_button("RETRY", on_click=lambda: nav("Quiz")).classes('arcade-btn')
        with start_area:
            sound_button("START BATTLE", on_click=begin_actual_combat).classes('bg-rose-700 text-white text-lg p-6 animate-pulse')

    def render_date_sim():
        ui.label("CHAOTIC DATE SIMULATOR").classes('text-xl mb-8')
        sim_card = ui.card().classes('w-full max-w-md items-center text-center p-6 bg-white border-2 border-rose-300 shadow-xl')
        with sim_card:
            story_box = ui.column().classes('w-full items-center')
            def show_step(text, options):
                story_box.clear()
                with story_box:
                    ui.label(text).classes('text-sm mb-8 leading-loose text-rose-800')
                    for label, next_step in options.items():
                        if next_step == "WIN": sound_button(label, on_click=win_date).classes('arcade-btn mb-4 w-full')
                        elif next_step == "LOSE": sound_button(label, on_click=lose_date).classes('arcade-btn mb-4 w-full')
                        else: sound_button(label, on_click=lambda ns=next_step: next_step_logic(ns)).classes('arcade-btn mb-4 w-full')
            def win_date():
                story_box.clear()
                with story_box:
                    ui.label("FRAGMENT OBTAINED!").classes('text-xl text-green-600 mb-4')
                    if "Date Sim" not in app.storage.user['fragments']:
                        app.storage.user['fragments'].append("Date Sim")
                        ui.notify("FRAGMENT OBTAINED!")
                    sound_button("RETURN HOME", on_click=lambda: nav("Home")).classes('arcade-btn')
            def lose_date():
                story_box.clear()
                with story_box:
                    ui.label("BAD ENDING").classes('text-xl text-red-600 mb-4')
                    sound_button("RETRY", on_click=lambda: nav("Date")).classes('arcade-btn mt-4')
            def next_step_logic(step_id):
                if step_id == 1: show_step("THE WAITER ARRIVES. ORDER?", {"MYSTERY DISH": 2, "WHATEVER THE RESTAURANT CAT IS HAVING": 2, "AUTHENTIC SPAGHETTI WITH TWO FORKS": "LOSE"})
                elif step_id == 2: show_step("YOUR DATE ASKS ABOUT YOUR JOB.", {"SPY FOR AN ALIEN REBELLION": 3, "PROFESSIONAL CLOUD WATCHER": 3, "AQUATIC TUBING SYSTEMS ENGINEER (PLUMBER)": "LOSE"})
                elif step_id == 3: show_step("THE CHECK ARRIVES, HOW DO YOU PAY?.", {"BATTLE THE CHEF": 4, "PAY WITH THE RESTAURANT'S OWN CAT IN A DISGUISE": 4, "PRETEND TO FALL ASLEEP": "LOSE"})
                elif step_id == 4: show_step("A DRAGON BLOCKS THE EXIT.", {"OFFER RESTAURANT CAT": 5, "DANCE OFF": 5, "SLAY IT": "LOSE"})
                elif step_id == 5: show_step("YOUR DATE WILL WALK YOU HOME", {"FLY HOME": "WIN", "TELEPORT HOME": "WIN", "RUN AWAY": "LOSE"})
            next_step_logic(1)

    def render_finale():
        ui.label("THE REVEAL").classes('text-2xl text-rose-800 mb-6')
        ui.image('valentine_photo.jpg').classes('rounded-none shadow-xl w-full max-w-md mb-6 border-4 border-white')
        ui.label("HAPPY VALENTINE'S DAY!").classes('text-lg text-rose-600')
        ui.label("From Ian").classes('text-sm text-rose-500 mt-2 animate-pulse')
        ui.label("Keep being you!").classes('text-sm text-rose-500 mt-2 animate-pulse')

    async def enter_arcade():
        if beep_player: beep_player.seek(0); beep_player.play()
        splash_container.classes(add='hidden')
        arcade_container.classes(remove='hidden', add='block')
        drawer.set_value(True)
        audio_player.play()
        nav("Home")

    with splash_container:
        ui.label("The Valentine Quest").classes('text-4xl text-rose-600 mb-6 text-center leading-loose')
        ui.label("For Aryam... Are you READY?").classes('text-sm text-rose-800 mb-12 animate-bounce')
        sound_button("INSERT COIN", on_click=enter_arcade).classes('arcade-btn bg-rose-600 text-white text-xl p-8 border-none')

if __name__ in {"__main__", "__mp_main__"}:
    ui.run(title="Valentine Arcade", favicon="❤️", storage_secret='valentine_secret_key_2026')