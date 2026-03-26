import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Dashboard BI & AI", layout="wide")

st.title("📊 Dashboard BI & AI")

API_URL = "http://127.0.0.1:8001"
# ----------------------------
# KPI PRODUITS
# ----------------------------
st.header("📦 KPI Produits")

col1, col2, col3 = st.columns(3)

try:
    total = requests.get(f"{API_URL}/kpi/total_products").json()["total"]
    value = requests.get(f"{API_URL}/kpi/total_value").json()["total_value"]
    stock = requests.get(f"{API_URL}/kpi/in_stock").json()["in_stock"]

    col1.metric("Total Produits", total)
    col2.metric("Valeur Stock", f"{value} DH")
    col3.metric("En Stock", stock)

except:
    st.warning("⚠️ API non lancée")

# ----------------------------
# LISTE PRODUITS
# ----------------------------
st.header("📋 Liste Produits")

try:
    data = requests.get(f"{API_URL}/items/").json()["items"]
    if data:
        df = pd.DataFrame([item for item in data])
        st.dataframe(df)
    else:
        st.info("Aucun produit")
except:
    pass

# ----------------------------
# AJOUT PRODUIT
# ----------------------------
st.header("➕ Ajouter Produit")

name = st.text_input("Nom")
price = st.number_input("Prix", min_value=0.0)
sales = st.number_input("Sales", min_value=0)
views = st.number_input("Views", min_value=0)

if st.button("Ajouter produit"):
    res = requests.post(f"{API_URL}/items/", json={
        "name": name,
        "price": price,
        "in_stock": True,
        "sales": sales,
        "views": views
    })
    st.success("Produit ajouté ✔️")

# ----------------------------
# PREDICTION AI
# ----------------------------
st.header("🤖 Prédiction demande")

if st.button("Prédire"):
    res = requests.post(f"{API_URL}/predict", json={
        "name": name,
        "price": price,
        "in_stock": True,
        "sales": sales,
        "views": views
    })
    st.success(f"Prediction: {res.json()['prediction']}")

# ----------------------------
# KPI BANQUE
# ----------------------------
st.header("🏦 KPI Banque")

col1, col2, col3 = st.columns(3)

try:
    kpi = requests.get(f"{API_URL}/kpi/clients").json()
    col1.metric("Clients", kpi["total_clients"])
    col2.metric("Revenu moyen", round(kpi["avg_income"], 2))
    col3.metric("Taux défaut", round(kpi["default_rate"], 2))
except:
    st.warning("API banque non prête")

# ----------------------------
# AJOUT CLIENT
# ----------------------------
st.header("➕ Ajouter Client")

age = st.number_input("Age", min_value=18)
income = st.number_input("Revenu", min_value=0.0)
debt = st.number_input("Dette", min_value=0.0)
default = st.selectbox("Défaut", [0,1])

if st.button("Ajouter client"):
    requests.post(f"{API_URL}/clients/", json={
        "age": age,
        "income": income,
        "debt": debt,
        "default": default
    })
    st.success("Client ajouté ✔️")