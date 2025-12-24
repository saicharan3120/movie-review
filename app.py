import sqlite3
import streamlit as st

st.set_page_config(page_title="Movie Review Portal", layout="wide")

# ---------------- DATABASE ----------------
conn = sqlite3.connect("reviews.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    movie TEXT,
    name TEXT,
    suc_id TEXT,
    section TEXT,
    department TEXT,
    rating REAL
)
""")
conn.commit()

def add_review(movie, name, suc_id, section, department, rating):
    cursor.execute("""
    INSERT INTO reviews (movie, name, suc_id, section, department, rating)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (movie, name, suc_id, section, department, rating))
    conn.commit()

def get_reviews(movie):
    cursor.execute("SELECT * FROM reviews WHERE movie = ?", (movie,))
    return cursor.fetchall()

def get_average(movie):
    cursor.execute("SELECT AVG(rating) FROM reviews WHERE movie = ?", (movie,))
    avg = cursor.fetchone()[0]
    return round(avg, 2) if avg else 0

def get_user_count(movie):
    cursor.execute("SELECT COUNT(*) FROM reviews WHERE movie = ?", (movie,))
    return cursor.fetchone()[0]

# ---------------- MOVIES ----------------
movies = ["Salaar", "SVSC", "Srimanthudu", "Gabbarsingh", "OG"]

# ---------------- ADMIN PANEL ----------------
st.sidebar.title("🛠 Admin Panel")

st.sidebar.markdown("### 👥 User Count per Movie")
for m in movies:
    st.sidebar.write(f"{m}: {get_user_count(m)} users")

st.sidebar.markdown("---")
st.sidebar.markdown("### 📋 User Review Details")

admin_movie = st.sidebar.selectbox("Select Movie", movies)
reviews = get_reviews(admin_movie)

if reviews:
    for i, r in enumerate(reviews, start=1):
        st.sidebar.markdown(f"""
        **User {i}**
        - Name: {r[2]}
        - SUC ID: {r[3]}
        - Section: {r[4]}
        - Department: {r[5]}
        - Rating: ⭐ {r[6]}
        ---
        """)
else:
    st.sidebar.info("No reviews yet")

# ---------------- USER SIDE ----------------
st.title("🎬 Movie Review Portal")

name = st.text_input("Enter Your Name")
suc_id = st.text_input("Enter Your SUC ID")
section = st.text_input("Enter Your Section")
department = st.text_input("Enter Your Department")

movie = st.selectbox("Choose a Movie", movies)

rating = st.slider("Give Rating (0–5 ⭐)", 0.0, 5.0, step=0.5)

if st.button("Submit Review"):
    if name.strip() == "":
        st.warning("⚠️ Name is required")
    else:
        add_review(movie, name, suc_id, section, department, rating)
        st.success("✅ Review submitted successfully")

# ---------------- SUMMARY ----------------
st.markdown("### ⭐ Movie Ratings Summary")

for m in movies:
    st.write(
        f"🎬 {m} | ⭐ Average: {get_average(m)} | 👥 Users: {get_user_count(m)}"
    )
