import streamlit as st
import pandas as pd
import os
import random
import io
from datetime import date, datetime
import plotly.graph_objects as go

# ================= DATABASE CONFIG =================
DB_FILE = "synclife_v49_data.csv"
USER_DB = "synclife_v49_users.csv"

def load_data(file, columns):
    if not os.path.exists(file): return pd.DataFrame(columns=columns)
    try:
        return pd.read_csv(file)
    except:
        return pd.DataFrame(columns=columns)

def save_data(df, file):
    df.to_csv(file, index=False)

# ================= AI DYNAMIC MOTIVATION ENGINE =================
def get_ai_motivation():
    today_seed = date.today().strftime("%Y%m%d")
    random.seed(int(today_seed))
    themes = ["Metabolic Intelligence", "Biological Resilience", "Peak Performance", "Neural Clarity", "Longevity Mindset", "Cellular Discipline"]
    quotes = [
        "Your biology is a reflection of your consistency. Optimize today for a better tomorrow.",
        "The metabolic fire you stoke today burns through the limitations of yesterday.",
        "Health isn't a destination; it's a high-resolution data set of your daily habits.",
        "Every step is a signal to your DNA that you choose strength over stagnation.",
        "Precision in your nutrition leads to precision in your focus. Stay sharp.",
        "Recovery is not rest; it is the active rebuilding of your future self."
    ]
    selected_theme = random.choice(themes)
    selected_quote = random.choice(quotes)
    return f'<span style="font-weight:800; text-transform:uppercase; letter-spacing:1px; color:#f0f9ff;">{selected_theme}:</span> "{selected_quote}"'

# ================= AUTHENTICATION LOGIC =================
def auth_system():
    user_cols = ["Email", "Name", "Password"]
    user_df = load_data(USER_DB, user_cols)
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        st.markdown('<div class="welcome-banner"><h1>🌿 SyncLife Pro</h1><p>Join the Family Health Journey</p></div>', unsafe_allow_html=True)
        t1, t2 = st.tabs(["Login", "Register"])
        with t1:
            with st.form("Login"):
                e = st.text_input("Email ID").lower().strip()
                p = st.text_input("Password", type="password")
                if st.form_submit_button("Sign In"):
                    match = user_df[(user_df["Email"] == e) & (user_df["Password"] == str(p))]
                    if not match.empty:
                        st.session_state.authenticated = True
                        st.session_state.user_id = e
                        st.session_state.user_display_name = match.iloc[0]["Name"]
                        st.rerun()
                    else: st.error("Invalid credentials")
        with t2:
            with st.form("Register"):
                n_n = st.text_input("Full Name")
                n_e = st.text_input("Email ID").lower().strip()
                n_p = st.text_input("Create Password", type="password")
                if st.form_submit_button("Create Account"):
                    if n_e and n_p and n_n:
                        save_data(pd.concat([user_df, pd.DataFrame([[n_e, n_n, n_p]], columns=user_cols)], ignore_index=True), USER_DB)
                        st.success("Account created! Please log in.")
        return False
    return True

# ================= UI & STYLING =================
st.set_page_config(page_title="SyncLife Pro", page_icon="🌿", layout="wide")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }
    
    .welcome-banner { 
        background: linear-gradient(135deg, #0d9488 0%, #2563eb 100%); 
        color: white; padding: 45px; border-radius: 35px; text-align: center; margin-bottom: 30px; 
    }
    
    .main-heading { 
        font-size: 1.85rem; 
        font-weight: 800; 
        color: inherit; 
        margin-top: 25px; 
        margin-bottom: 15px;
    }
    
    .tile { 
        padding: 20px; border-radius: 18px; 
        background: rgba(128, 128, 128, 0.05); 
        border-top: 5px solid #10b981; 
        text-align: center; height: 100%; 
    }
    .tile-header { font-size: 0.8rem; font-weight: 800; color: #10b981; text-transform: uppercase; }
    .tile-value { font-size: 1.3rem; font-weight: 700; margin-top: 5px; }
    </style>
""", unsafe_allow_html=True)

if auth_system():
    uid = st.session_state.user_id
    COLUMNS = ["Date", "User_ID", "User_Name", "User_Age", "User_Gender", "User_Height", "User_Target_W",
               "Target_Steps", "Target_Sleep", "Target_Calories", "Weight", "Steps", "Sleep_H", "Sleep_M",
               "Calories", "Protein", "Carbs", "Fats", "Fiber", "Tea_Cups", "Toilet_Visits", "Workout",
               "Supplements", "Fasting_Ratio", "Daily_Notes", "Mood"]
    
    df = load_data(DB_FILE, COLUMNS)
    user_df = df[df["User_ID"] == uid]

    d_a, d_g, d_h, d_tw, d_ts, d_tc, d_tsl = 25, "Male", 170.0, 70.0, 10000, 2000, 8.0
    if not user_df.empty:
        last = user_df.iloc[-1]
        d_a, d_g, d_h = int(last.get("User_Age", 25)), last.get("User_Gender", "Male"), float(last.get("User_Height", 170.0))
        d_tw, d_ts, d_tc, d_tsl = float(last.get("User_Target_W", 70.0)), int(last.get("Target_Steps", 10000)), int(last.get("Target_Calories", 2000)), float(last.get("Target_Sleep", 8.0))

    with st.sidebar:
        st.markdown(f"## 👤 {st.session_state.user_display_name}")
        log_date = st.date_input("Log Date", date.today(), max_value=date.today())
        date_str = log_date.strftime("%Y-%m-%d")
        if st.button("Logout"): st.session_state.authenticated = False; st.rerun()

        with st.expander("⚙️ Profile & Goals"):
            u_name = st.text_input("Name", value=st.session_state.user_display_name)
            u_gender = st.selectbox("Gender", ["Male", "Female", "Other"], index=0 if d_g=="Male" else 1)
            u_age, u_height, u_target_w = st.number_input("Age", value=d_a), st.number_input("Height (cm)", value=d_h), st.number_input("Target Weight (kg)", value=d_tw)
            u_target_steps, u_target_cal, u_target_sleep = st.number_input("Steps Goal", value=d_ts), st.number_input("Calories Goal", value=d_tc), st.number_input("Sleep Goal", value=d_tsl)

        st.markdown("### 🏃 Activity")
        u_steps, u_weight, u_focus = st.number_input("Steps Today", 0), st.number_input("Weight (kg)", 0.0), st.text_input("Workout", "Resistance Training")

        st.markdown("### 🥗 Nutrition")
        u_cals = st.number_input("Calories", 0)
        m1, m2, m3, m4 = st.columns(4)
        u_prot, u_carb, u_fats, u_fiber = m1.number_input("P", 0.0), m2.number_input("C", 0.0), m3.number_input("F", 0.0), m4.number_input("Fib", 0.0)
        u_fast = st.text_input("Fasting Ratio", "16:8")
        
        st.markdown("### 💤 Recovery")
        s1, s2 = st.columns(2)
        u_sl_h, u_sl_m = s1.number_input("Hrs", 0, 24), s2.number_input("Min", 0, 59)
        u_tea, u_dig = st.number_input("Tea Cups", 0), st.number_input("Digestion", 0)
        u_supps = st.multiselect("Supplements", ["Vitamin D3", "Magnesium", "Zinc", "Omega 3", "Other"])
        u_c_supp = st.text_input("Custom Name") if "Other" in u_supps else ""

        st.markdown("### 📸 Media")
        u_notes = st.text_area("Daily Journal")
        u_photos = st.file_uploader("Upload Photos", accept_multiple_files=True, key=f"uploader_{date_str}")

        if st.button("SYNC DATA", use_container_width=True):
            supps_final = [s for s in u_supps if s != "Other"] + ([u_c_supp] if u_c_supp else [])
            new_row = {"Date": date_str, "User_ID": uid, "User_Name": u_name, "User_Age": u_age, "User_Gender": u_gender, "User_Height": u_height, "User_Target_W": u_target_w, "Target_Steps": u_target_steps, "Target_Sleep": u_target_sleep, "Target_Calories": u_target_cal, "Weight": u_weight, "Steps": u_steps, "Sleep_H": u_sl_h, "Sleep_M": u_sl_m, "Calories": u_cals, "Protein": u_prot, "Carbs": u_carb, "Fats": u_fats, "Fiber": u_fiber, "Tea_Cups": u_tea, "Toilet_Visits": u_dig, "Workout": u_focus, "Supplements": ", ".join(supps_final), "Fasting_Ratio": u_fast, "Daily_Notes": u_notes if u_notes.strip() else "Sync complete. 🌟", "Mood": "🙂"}
            df = pd.concat([df[~((df["Date"] == date_str) & (df["User_ID"] == uid))], pd.DataFrame([new_row])], ignore_index=True)
            save_data(df, DB_FILE)
            if u_photos: st.session_state[f"img_{date_str}_{uid}"] = [p.getvalue() for p in u_photos]
            st.rerun()

    # DASHBOARD
    st.markdown(f'<div class="welcome-banner"><h3>{get_ai_motivation()}</h3><p style="opacity:0.9;">System Status for {u_name} • {log_date.strftime("%B %d, %Y")}</p></div>', unsafe_allow_html=True)
    day_data = df[(df["Date"] == date_str) & (df["User_ID"] == uid)]
    
    if not day_data.empty:
        row = day_data.iloc[0]
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="main-heading">🧬 BMI Status</div>', unsafe_allow_html=True)
            bmi = row['Weight'] / ((u_height/100)**2) if row['Weight'] > 0 else 0
            status, col = ("Underweight", "#3b82f6") if bmi < 18.5 else ("Healthy Weight", "#10b981") if bmi < 25 else ("Overweight", "#f59e0b") if bmi < 30 else ("Obese", "#ef4444")
            fig = go.Figure(go.Indicator(mode="gauge+number", value=bmi, number={'font':{'color':col, 'size':45}, 'suffix': ' BMI'}, gauge={'axis':{'range':[15,40]}, 'bar':{'color':col}}))
            fig.update_layout(height=250, margin=dict(t=0,b=0,l=20,r=20), paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
            st.markdown(f"<center><b style='font-size:1.4rem; color:{col};'>{status}</b></center>", unsafe_allow_html=True)

        with c2:
            st.markdown('<div class="main-heading">🎯 Target Progress</div>', unsafe_allow_html=True)
            st.write(f"👣 Steps: {row['Steps']} / {u_target_steps}")
            st.progress(min(1.0, row['Steps']/max(1, u_target_steps)))
            st.write(f"🍎 Calories: {row['Calories']} / {u_target_cal}")
            st.progress(min(1.0, row['Calories']/max(1, u_target_cal)))
            st.write(f"💤 Sleep: {row['Sleep_H']}h / {u_target_sleep}h")
            st.progress(min(1.0, row['Sleep_H']/max(1, u_target_sleep)))

        st.markdown('<div class="main-heading">📊 Performance Summary</div>', unsafe_allow_html=True)
        t1, t2, t3, t4 = st.columns(4)
        with t1: st.markdown(f'<div class="tile" style="border-top-color:#3b82f6;"><div class="tile-header">Movement</div><div class="tile-value">🏃 {row["Workout"]}</div><div class="tile-sub">{row["Steps"]:,} steps</div></div>', unsafe_allow_html=True)
        with t2: st.markdown(f'<div class="tile" style="border-top-color:#10b981;"><div class="tile-header">Nutrition</div><div class="tile-value">🥗 {row["Calories"]} kcal</div><div class="tile-sub">P:{row["Protein"]}g C:{row["Carbs"]}g F:{row["Fats"]}g</div></div>', unsafe_allow_html=True)
        with t3: st.markdown(f'<div class="tile" style="border-top-color:#f59e0b;"><div class="tile-header">Metabolic</div><div class="tile-value">⏳ {row["Fasting_Ratio"]}</div><div class="tile-sub">🧻 {row["Toilet_Visits"]} visits</div></div>', unsafe_allow_html=True)
        with t4: st.markdown(f'<div class="tile" style="border-top-color:#8b5cf6;"><div class="tile-header">Recovery</div><div class="tile-value">💤 {row["Sleep_H"]}h {row["Sleep_M"]}m</div><div class="tile-sub">🍵 {row["Tea_Cups"]} cups tea</div></div>', unsafe_allow_html=True)

        st.markdown('<div class="main-heading">📸 Daily Media & Journal</div>', unsafe_allow_html=True)
        # CLEANED: Removed the 'glass-card' div from here to remove the block
        if f"img_{date_str}_{uid}" in st.session_state:
            cols = st.columns(4)
            for i, img_bytes in enumerate(st.session_state[f"img_{date_str}_{uid}"]):
                cols[i%4].image(img_bytes, use_container_width=True)
        st.info(f"**Supplements:** {row['Supplements']}")
        st.info(f"**Journal Note:** {row['Daily_Notes']}")
    else:
        st.info("No entry found for this date. Use the sidebar to log your biology!")
