import streamlit as st
import pandas as pd
import os
import random
from datetime import date, datetime
import plotly.graph_objects as go

# ================= GLOBAL CONSTANTS =================
DB_FILE = "synclife_v33.csv"

def get_daily_quote():
    day_name = datetime.now().strftime("%A")
    morning_quotes = [
        f"✨ {day_name} is your canvas. Paint a masterpiece of discipline.",
        "🔥 The body achieves what the mind believes.",
        "⚡ Energy flows where intention goes.",
        "🏆 Victory is bought with the sweat of today.",
        "🍏 Your health is an investment, not an expense.",
        "💪 Character is what you do when no one is watching."
    ]
    return random.choice(morning_quotes)

COLUMNS = [
    "Date", "User_Name", "User_Age", "User_Gender", "User_Height", "User_Target_W",
    "Target_Steps", "Target_Sleep", "Target_Water", "Target_Calories",
    "Weight", "Steps", "Sleep_H", "Sleep_M", "Calories", "Protein", "Carbs", "Fats", "Fiber",
    "Tea_Cups", "Toilet_Visits", "Workout", "Supplements", 
    "Fasting_Ratio", "Daily_Notes", "Mood"
]

def load_data():
    if not os.path.exists(DB_FILE): return pd.DataFrame(columns=COLUMNS)
    df = pd.read_csv(DB_FILE)
    df["Date"] = df["Date"].astype(str)
    for col in COLUMNS:
        if col not in df.columns: df[col] = 0
    return df

def save_data(df):
    df.to_csv(DB_FILE, index=False)

# ================= DYNAMIC STYLING =================
st.set_page_config(page_title="SyncLife Pro", page_icon="🌿", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }
    .welcome-banner {
        background: linear-gradient(135deg, #0d9488 0%, #2563eb 100%);
        color: white; padding: 40px; border-radius: 30px; text-align: center; margin-bottom: 25px;
    }
    .glass-card {
        background: rgba(128, 128, 128, 0.08);
        border: 1px solid rgba(128, 128, 128, 0.2);
        border-radius: 24px; padding: 22px; margin-bottom: 15px;
    }
    .tile {
        padding: 15px; border-radius: 18px; background: rgba(128, 128, 128, 0.04);
        border-top: 4px solid #10b981; text-align: center; height: 100%;
    }
    .tile-header { font-size: 0.75rem; font-weight: 800; color: #10b981; text-transform: uppercase; }
    .tile-value { font-size: 1.2rem; font-weight: 700; margin-top: 4px; }
    
    /* MODIFIED FOR DARK MODE VISIBILITY */
    .custom-tip {
        background: rgba(59, 130, 246, 0.15); 
        border-left: 5px solid #60a5fa;
        padding: 15px; border-radius: 12px; 
        margin-top: 10px; font-size: 0.95rem; 
        color: inherit; /* This ensures text adapts to Light/Dark mode */
    }
    </style>
""", unsafe_allow_html=True)

df = load_data()

# ================= PERSISTENT PROFILE DEFAULTS =================
if not df.empty:
    last = df.iloc[-1]
    d_name = last.get("User_Name", "User")
    d_age = int(last.get("User_Age", 25))
    d_gender = last.get("User_Gender", "Male")
    d_height = float(last.get("User_Height", 170.0))
    d_tw = float(last.get("User_Target_W", 70.0))
    d_ts = int(last.get("Target_Steps", 10000))
    d_tc = int(last.get("Target_Calories", 2000))
    d_tsl = float(last.get("Target_Sleep", 8.0))
else:
    d_name, d_age, d_gender, d_height, d_tw = "User", 25, "Male", 170.0, 70.0
    d_ts, d_tc, d_tsl = 10000, 2000, 8.0

# ================= SIDEBAR & STATE LOGIC =================
with st.sidebar:
    st.markdown("## 🌿 SyncLife Pro")
    log_date = st.date_input("Log Date", date.today())
    date_str = log_date.strftime("%Y-%m-%d")

    existing_entry = df[df["Date"] == date_str]
    current_notes_val = str(existing_entry.iloc[0]["Daily_Notes"]) if not existing_entry.empty else ""

    with st.expander("👤 Full Profile & Goals", expanded=False):
        u_name = st.text_input("Full Name", value=d_name)
        c1, c2 = st.columns(2)
        u_age = c1.number_input("Age", value=d_age)
        u_gender = c2.selectbox("Gender", ["Male", "Female", "Other"], index=0)
        u_height = st.number_input("Height (cm)", value=d_height)
        u_target_w = st.number_input("Target Weight (kg)", value=d_tw)
        st.divider()
        u_target_steps = st.number_input("Daily Steps Goal", value=d_ts)
        u_target_cal = st.number_input("Daily Calorie Goal", value=d_tc)
        u_target_sleep = st.number_input("Daily Sleep Goal (H)", value=d_tsl)

    st.markdown("### 🏃 Activity")
    u_steps = st.number_input("Steps Today", 0)
    u_weight = st.number_input("Today's Weight (kg)", 0.0)
    u_focus = st.text_input("Workout", "Resistance Training")

    st.markdown("### 🥗 Nutrition")
    u_cals = st.number_input("Total Calories", 0)
    m1, m2, m3, m4 = st.columns(4)
    u_prot = m1.number_input("P", 0.0); u_carb = m2.number_input("C", 0.0)
    u_fats = m3.number_input("F", 0.0); u_fiber = m4.number_input("Fib", 0.0)
    u_fast_ratio = st.text_input("Fasting Window", "16:8")
    
    st.markdown("### 💤 Recovery")
    s1, s2 = st.columns(2)
    u_sleep_h = s1.number_input("Sleep (hrs)", 0, 24); u_sleep_m = s2.number_input("Sleep (min)", 0, 59)
    u_tea = st.number_input("Green Tea (cups)", 0)
    u_toilet = st.number_input("Digestion (Visits)", 0)
    
    u_supp_options = st.multiselect("Supplements", ["Vitamin D3", "Magnesium Glycinate", "Zinc Picolinate", "Omega 3 Fish Oil", "Creatine Monohydrate", "Other"])
    u_custom_supp = ""
    if "Other" in u_supp_options:
        u_custom_supp = st.text_input("Type your other supplements here...")

    st.markdown("### 📓 Journal")
    u_notes = st.text_area("Daily Journal", value=current_notes_val, key=f"note_v33_{date_str}")
    u_photos = st.file_uploader("Upload Daily Media", accept_multiple_files=True, key=f"photo_v33_{date_str}")

    if st.button("SYNC DAILY DATA", use_container_width=True):
        if u_photos: st.session_state[f"stored_images_{date_str}"] = u_photos
        
        final_supps = [s for s in u_supp_options if s != "Other"]
        if u_custom_supp: final_supps.append(u_custom_supp)
        
        new_row = {
            "Date": date_str, "User_Name": u_name, "User_Age": u_age, "User_Gender": u_gender,
            "User_Height": u_height, "User_Target_W": u_target_w, "Target_Steps": u_target_steps,
            "Target_Sleep": u_target_sleep, "Target_Calories": u_target_cal,
            "Weight": u_weight, "Steps": u_steps, "Sleep_H": u_sleep_h, "Sleep_M": u_sleep_m,
            "Calories": u_cals, "Protein": u_prot, "Carbs": u_carb, "Fats": u_fats, "Fiber": u_fiber,
            "Tea_Cups": u_tea, "Toilet_Visits": u_toilet, "Workout": u_focus,
            "Supplements": ", ".join(final_supps), "Fasting_Ratio": u_fast_ratio, "Daily_Notes": u_notes, "Mood": "🙂"
        }
        df = pd.concat([df[df["Date"] != date_str], pd.DataFrame([new_row])], ignore_index=True)
        save_data(df); st.rerun()

# ================= DASHBOARD =================
st.markdown(f'<div class="welcome-banner"><h1>{get_daily_quote()}</h1><p>SyncLife Intel • {u_name} • {log_date.strftime("%B %d, %Y")}</p></div>', unsafe_allow_html=True)

if not existing_entry.empty:
    row = existing_entry.iloc[0]
    total_sleep = float(row['Sleep_H']) + (float(row['Sleep_M'])/60)
    
    c1, c2 = st.columns([1, 1.2])
    with c1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 🧬 Physiological Status")
        bmi = row['Weight'] / ((u_height/100)**2) if row['Weight'] > 0 else 0
        status, col = ("Healthy", "#10b981") if 18.5 <= bmi < 25 else ("Needs Attention", "#f59e0b")
        fig = go.Figure(go.Indicator(mode="gauge+number", value=bmi, number={'font':{'color':col}}, gauge={'axis':{'range':[15,35]}, 'bar':{'color':col}}))
        fig.update_layout(height=200, margin=dict(t=0, b=0), paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(f"<center><b>Weight: {row['Weight']}kg</b> | <b>BMI: {bmi:.1f}</b> ({status})</center>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 🎯 Target Progress")
        st.write(f"👣 Steps: {row['Steps']:,} / {row['Target_Steps']:,}")
        st.progress(min(1.0, row['Steps']/max(1, row['Target_Steps'])))
        st.write(f"🍎 Calories: {row['Calories']} / {row['Target_Calories']} kcal")
        st.progress(min(1.0, row['Calories']/max(1, row['Target_Calories'])))
        st.write(f"💤 Sleep: {total_sleep:.1f}h / {row['Target_Sleep']}h")
        st.progress(min(1.0, total_sleep/max(1, row['Target_Sleep'])))
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("## 📊 Performance Summary")
    t1, t2, t3, t4 = st.columns(4)
    with t1: 
        st.markdown(f'<div class="tile" style="border-top-color:#3b82f6;"><div class="tile-header">Movement</div><div class="tile-value">🏃 {row["Workout"]}</div><div class="tile-sub">{row["Steps"]:,} steps</div></div>', unsafe_allow_html=True)
    with t2: 
        st.markdown(f'<div class="tile" style="border-top-color:#10b981;"><div class="tile-header">Nutrition</div><div class="tile-value">🥗 {row["Calories"]} kcal</div><div class="tile-sub">P:{row["Protein"]}g C:{row["Carbs"]}g F:{row["Fats"]}g Fib:{row["Fiber"]}g</div></div>', unsafe_allow_html=True)
    with t3: 
        st.markdown(f'<div class="tile" style="border-top-color:#f59e0b;"><div class="tile-header">Metabolic</div><div class="tile-value">⏳ {row["Fasting_Ratio"]}</div><div class="tile-sub">🧻 {row["Toilet_Visits"]} visits</div></div>', unsafe_allow_html=True)
    with t4: 
        st.markdown(f'<div class="tile" style="border-top-color:#8b5cf6;"><div class="tile-header">Recovery</div><div class="tile-value">💤 {row["Sleep_H"]}h {row["Sleep_M"]}m</div><div class="tile-sub">🍵 {row["Tea_Cups"]} cups tea</div></div>', unsafe_allow_html=True)

    # --- AI SMART COACH ---
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 💡 AI Smart Coach")
    
    has_tips = False
    if row['Steps'] < row['Target_Steps']:
        st.markdown(f'<div class="custom-tip">🏃 **Movement:** You are {int(row["Target_Steps"] - row["Steps"])} steps away from your goal. A short walk before bed helps insulin sensitivity.</div>', unsafe_allow_html=True)
        has_tips = True
    if row['Fiber'] < 25:
        st.markdown('<div class="custom-tip">🥦 **Nutrition:** Fiber is low. Aim for 25g+ to stabilize blood sugar and support gut microbes.</div>', unsafe_allow_html=True)
        has_tips = True
    if row['Toilet_Visits'] < 1:
        st.markdown('<div class="custom-tip">🧻 **Metabolic:** Digestion visits are low. Consider extra hydration and magnesium to support motility.</div>', unsafe_allow_html=True)
        has_tips = True
    if total_sleep < row['Target_Sleep']:
        st.markdown('<div class="custom-tip">🌙 **Recovery:** Sleep was under target. Prioritize a cool, dark room tonight to maximize growth hormone release.</div>', unsafe_allow_html=True)
        has_tips = True
    
    if not has_tips:
        st.success("🌟 All systems go! You hit every target today. Keep this momentum!")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 📸 Daily Media & Journal")
    if f"stored_images_{date_str}" in st.session_state:
        img_cols = st.columns(4)
        for idx, img in enumerate(st.session_state[f"stored_images_{date_str}"]):
            with img_cols[idx % 4]: st.image(img, use_container_width=True)
    st.info(f"**Supplements Today:** {row['Supplements'] if row['Supplements'] else 'None'}")
    st.info(f"**Journal Entry:** {row['Daily_Notes'] if row['Daily_Notes'] else 'No notes written today.'}")
    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.markdown(f"<div style='text-align:center; padding:100px;'><h2>Ready to log your day, {u_name}? 👋</h2><p>Select a date and fill out your metrics in the sidebar.</p></div>", unsafe_allow_html=True)
