import io
import os

import matplotlib.pyplot as plt
import numpy as np
import requests
import streamlit as st
from PIL import Image

API_URL = os.getenv("API_URL", "http://localhost:8000")

CLASS_INFO = {
    "glioma": {
        "title": "Gliome",
        "color": "#e63946",
        "accent": "#ffebee",
        "description": "Tumeur infiltrante prenant naissance dans les cellules gliales du tissu cérébral.",
        "badge": "🔴 Tumeur maligne / Gliale",
        "icon": "⚠️",
    },
    "meningioma": {
        "title": "Méningiome",
        "color": "#f39c12",
        "accent": "#fff8e1",
        "description": "Tumeur généralement bénigne issue des méninges protectrices du système nerveux central.",
        "badge": "🟠 Méningée",
        "icon": "🔍",
    },
    "notumor": {
        "title": "Sain (Pas de tumeur)",
        "color": "#2a9d8f",
        "accent": "#e8f8f5",
        "description": "Examen IRM sans anomalie néoplasique décelable. Tissu cérébral normal.",
        "badge": "🟢 Tissu Sain",
        "icon": "✅",
    },
    "pituitary": {
        "title": "Tumeur Pituitaire (Hypophysaire)",
        "color": "#8e44ad",
        "accent": "#f3e5f5",
        "description": "Lésion située dans la région sellaire affectant la glande hypophyse.",
        "badge": "🟣 Hypophysaire",
        "icon": "🔬",
    },
}

st.set_page_config(
    page_title="BrainScan AI — Diagnostic IRM Intelligent",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .main-header {
        background: linear-gradient(135deg, #0d3b66 0%, #001e3d 100%);
        border-radius: 16px;
        padding: 2.2rem 2.5rem;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px rgba(13, 59, 102, 0.15);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .header-text h1 {
        font-size: 2.2rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.5px;
        color: #ffffff !important;
    }

    .header-text p {
        font-size: 1.05rem;
        color: #b0c7de;
        margin: 0.5rem 0 0 0;
        font-weight: 400;
    }

    .header-badge {
        background: rgba(255, 255, 255, 0.12);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 0.6rem 1.2rem;
        border-radius: 30px;
        font-size: 0.85rem;
        font-weight: 600;
        color: #e2eafc;
        text-align: right;
    }

    .result-banner {
        border-radius: 14px;
        padding: 1.8rem;
        border-left: 8px solid;
        margin-bottom: 1.5rem;
        box-shadow: 0 6px 20px rgba(0,0,0,0.06);
    }

    .stButton>button {
        background: linear-gradient(135deg, #0d3b66 0%, #1d4ed8 100%) !important;
        color: white !important;
        border: none !important;
        padding: 0.75rem 1.5rem !important;
        font-size: 1.05rem !important;
        font-weight: 600 !important;
        border-radius: 10px !important;
        box-shadow: 0 4px 12px rgba(29, 78, 216, 0.25) !important;
        transition: all 0.2s ease !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 16px rgba(29, 78, 216, 0.35) !important;
    }
    </style>

    <div class="main-header">
        <div class="header-text">
            <h1>🧠 BrainScan AI</h1>
            <p>Système Intelligent d'Aide au Diagnostic et Détection Précoce des Tumeurs Cérébrales (IRM)</p>
        </div>
        <div class="header-badge">
            🇲🇦 MedTech Maroc<br>
            <span style="color: #64dfdf;">Version Production 1.0</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("### 🏥 À propos de BrainScan AI")
    st.write(
        "BrainScan AI est une solution d'imagerie médicale développée pour "
        "assister les radiologues et neurochirurgiens marocains dans l'analyse "
        "rapide et sécurisée des IRM cérébrales."
    )
    st.divider()

    st.markdown("### 📋 Classes diagnostiques")
    for cls, info in CLASS_INFO.items():
        st.markdown(
            f"""
            <div style="background:{info['accent']}; border-left:4px solid {info['color']}; padding:0.6rem 0.8rem; border-radius:6px; margin-bottom:0.5rem;">
                <strong style="color:{info['color']}">{info['badge']}</strong><br>
                <small style="color:#555;">{info['description']}</small>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.divider()
    st.markdown("### 🔌 État du service")
    try:
        resp = requests.get(f"{API_URL}/health", timeout=2)
        if resp.ok and resp.json().get("status") == "ok":
            model_ok = resp.json().get("model_loaded", False)
            if model_ok:
                st.success("🟢 API connectée (Modèle CNN opérationnel)")
            else:
                st.warning("🟠 API en ligne (Modèle en attente de chargement)")
        else:
            st.error("🔴 API indisponible")
    except Exception:
        st.error("🔴 Service API hors ligne")

col_upload, col_result = st.columns([1, 1], gap="large")

with col_upload:
    st.markdown("### 📤 Téléversement de l'IRM")
    uploaded = st.file_uploader(
        "Déposez une coupe IRM au format image",
        type=["jpg", "jpeg", "png", "bmp"],
        help="Formats autorisés : JPG, JPEG, PNG, BMP",
    )

    if uploaded:
        img = Image.open(uploaded)
        st.image(img, caption=f"IRM sélectionnée : {uploaded.name}", width="stretch")
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.metric("Résolution", f"{img.size[0]} × {img.size[1]} px")
        with col_m2:
            st.metric("Format source", str(img.format or uploaded.type).upper())
    else:
        st.info("ℹ️ Veuillez téléverser une image IRM cérébrale (T1/T2 pondérée) pour débuter l'évaluation.")

with col_result:
    st.markdown("### 🔬 Diagnostic et Prédiction")

    if uploaded:
        analyze_btn = st.button("⚡ Analyser l'image IRM", width="stretch")
        if analyze_btn:
            with st.spinner("Traitement et inférence CNN en cours..."):
                try:
                    buf = io.BytesIO()
                    img.save(buf, format="PNG")
                    buf.seek(0)

                    response = requests.post(
                        f"{API_URL}/predict",
                        files={"file": (uploaded.name, buf, "image/png")},
                        timeout=30,
                    )

                    if response.ok:
                        result = response.json()
                        predicted = result["predicted_class"]
                        confidence = result["confidence"]
                        probs = result["probabilities"]

                        info = CLASS_INFO.get(
                            predicted,
                            {
                                "title": predicted.capitalize(),
                                "color": "#1f2937",
                                "accent": "#f3f4f6",
                                "description": "Classe prédite.",
                                "badge": predicted,
                                "icon": "ℹ️",
                            },
                        )

                        conf_pct = confidence * 100

                        st.markdown(
                            f"""
                            <div class="result-banner" style="background-color:{info['accent']}; border-color:{info['color']};">
                                <div style="display:flex; justify-content:space-between; align-items:center;">
                                    <h2 style="margin:0; color:{info['color']}; font-size:1.8rem;">
                                        {info['icon']} {info['title'].upper()}
                                    </h2>
                                    <span style="background:{info['color']}; color:white; padding:0.4rem 1rem; border-radius:20px; font-weight:700; font-size:1.1rem;">
                                        {conf_pct:.1f}%
                                    </span>
                                </div>
                                <p style="margin:0.8rem 0 0 0; color:#374151; font-size:1.05rem; line-height:1.5;">
                                    {info['description']}
                                </p>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                        st.markdown("#### 📊 Distribution des probabilités de classe")
                        sorted_probs = sorted(probs.items(), key=lambda x: x[1], reverse=True)
                        labels = [CLASS_INFO.get(p[0], {}).get("title", p[0]) for p in sorted_probs]
                        values = [p[1] * 100 for p in sorted_probs]
                        colors = [CLASS_INFO.get(p[0], {}).get("color", "#6b7280") for p in sorted_probs]

                        fig, ax = plt.subplots(figsize=(6, 2.8))
                        bars = ax.barh(labels, values, color=colors, edgecolor="none", height=0.55)
                        ax.set_xlim(0, 100)
                        ax.set_xlabel("Niveau de confiance (%)", fontsize=10, fontweight="600")
                        ax.invert_yaxis()
                        for bar, val in zip(bars, values):
                            ax.text(
                                val + 1.5,
                                bar.get_y() + bar.get_height() / 2,
                                f"{val:.1f}%",
                                va="center",
                                fontsize=9,
                                fontweight="bold",
                            )
                        ax.spines[["top", "right", "left"]].set_visible(False)
                        ax.grid(axis="x", linestyle="--", alpha=0.3)
                        plt.tight_layout()
                        st.pyplot(fig)
                        plt.close()

                        st.caption(
                            "⚠️ **Avertissement médical** : BrainScan AI est un outil d'aide à la décision clinique. "
                            "Le diagnostic définitif relève de la responsabilité du praticien qualifié."
                        )
                    else:
                        st.error(f"Erreur API ({response.status_code}) : {response.text}")

                except requests.exceptions.ConnectionError:
                    st.error("Impossible de joindre le serveur API BrainScan (`http://localhost:8000`). Vérifiez son lancement.")
                except Exception as e:
                    st.error(f"Une anomalie est survenue lors de l'analyse : {e}")
    else:
        st.markdown(
            """
            <div style="border: 2px dashed #cbd5e1; border-radius: 12px; padding: 2.5rem; text-align: center; color: #64748b;">
                <p style="font-size: 1.1rem; margin: 0;">Aucune analyse en attente.</p>
                <small>Chargez une image IRM à gauche pour afficher les résultats.</small>
            </div>
            """,
            unsafe_allow_html=True,
        )
