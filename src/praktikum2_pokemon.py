import os

import requests
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Baca konfigurasi dari file .env (jika ada), nilai bawaan dipakai bila kosong
if os.path.isfile(".env"):
    with open(".env", encoding="utf-8") as env_file:
        for line in env_file:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                os.environ.setdefault(key.strip(), value.strip().strip("\"'"))
BASE_URL = os.getenv("POKEAPI_BASE_URL", "https://pokeapi.co/api/v2").rstrip("/")
DEFAULT_LIMIT = int(os.getenv("POKEMON_DEFAULT_LIMIT", "10"))
MIN_LIMIT = int(os.getenv("POKEMON_MIN_LIMIT", "5"))
MAX_LIMIT = int(os.getenv("POKEMON_MAX_LIMIT", "30"))
TIMEOUT = float(os.getenv("REQUEST_TIMEOUT", "10"))

st.title("Visualisasi Data Pokémon")

# Input jumlah Pokémon
limit = st.slider(
    "Pilih jumlah Pokémon yang ingin ditampilkan:",
    MIN_LIMIT, MAX_LIMIT, DEFAULT_LIMIT,
)

url = f"{BASE_URL}/pokemon?limit={limit}"
response = requests.get(url, timeout=TIMEOUT)

pokemon_list = []

if response.status_code == 200:
    data = response.json()

    # Loop untuk ambil detail tiap Pokémon
    for item in data["results"]:
        detail = requests.get(item["url"], timeout=TIMEOUT).json()
        pokemon_list.append({
            "name": detail["name"].capitalize(),
            "height": detail["height"],
            "weight": detail["weight"],
            "base_experience": detail["base_experience"],
            "abilities": len(detail["abilities"]),
        })

    # Ubah jadi DataFrame
    df = pd.DataFrame(pokemon_list)
    st.subheader("Data Pokémon")
    st.dataframe(df)

    # Metrik statistik
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Rata-rata Tinggi", f"{df['height'].mean():.2f}")
    with col2:
        st.metric("Rata-rata Berat", f"{df['weight'].mean():.2f}")
    with col3:
        st.metric("Rata-rata Ability", f"{df['abilities'].mean():.2f}")

    st.header("📊 Visualisasi Data Pokémon")

    # Bar chart dan barh chart sejajar
    colA, colB = st.columns(2)

    with colA:
        st.write("### Grafik Tinggi Pokémon")
        fig1, ax1 = plt.subplots()
        ax1.bar(df["name"], df["height"], color="skyblue")
        ax1.set_xlabel("Nama Pokémon")
        ax1.set_ylabel("Tinggi")
        ax1.tick_params(axis="x", rotation=45)
        st.pyplot(fig1)

    with colB:
        st.write("### Grafik Berat Pokémon")
        fig2, ax2 = plt.subplots()
        ax2.barh(df["name"], df["weight"], color="orange")
        ax2.set_xlabel("Berat")
        ax2.set_ylabel("Nama Pokémon")
        st.pyplot(fig2)

    # Scatter dan histogram sejajar
    colC, colD = st.columns(2)

    with colC:
        st.write("### Scatter Plot Tinggi vs Berat")
        fig3, ax3 = plt.subplots()
        ax3.scatter(df["height"], df["weight"], color="green")
        ax3.set_xlabel("Tinggi")
        ax3.set_ylabel("Berat")
        st.pyplot(fig3)

    with colD:
        st.write("### Histogram Jumlah Ability")
        fig4, ax4 = plt.subplots()
        ax4.hist(df["abilities"], bins=range(1, 6), color="purple", rwidth=0.8)
        ax4.set_xlabel("Jumlah Ability")
        ax4.set_ylabel("Frekuensi")
        st.pyplot(fig4)
else:
    st.error("Gagal mengambil data dari PokeAPI.")