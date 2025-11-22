import streamlit as st
import spacy
import re
import unicodedata
import requests
import random
import time

# Charger le modèle spaCy 
nlp = spacy.load("fr_core_news_lg") 

# Normaliser le texte saisi
def normalize_text(text):
    # enlever les accents
    text = ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    )
    # supprimer les espaces multiples
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Normaliser la date trouvée dans le texte saisi    
def normalize_date(text):
    months_en_fr = {
        "january":"01", "jan":"01", "janvier":"01",
        "february":"02", "feb":"02","fevrier":"02",
        "march":"03", "mar":"03","mars":"03",
        "april":"04", "apr":"04","avril":"04",
        "may":"05","mai":"05",
        "june":"06", "jun":"06","juin":"06",
        "july":"07", "jul":"07","juillet":"07",
        "august":"08", "aug":"08","aout":"08",
        "september":"09", "sep":"09","septembre":"09",
        "october":"10", "oct":"10","octobre":"10",
        "november":"11", "nov":"11","novembre":"11",
        "december":"12", "dec":"12","decembre":"12"
    }
    
    def replacer(match):
        day, month, year = match.groups()
        # Si month est numérique (02/01/2001)
        if month.isdigit():
            month_num = f"{int(month):02d}"
        else:
            month_num = months_en_fr.get(month.lower(), None)
        return f"{int(day):02d}-{month_num}-{year}"
    
    # 1️⃣ jj/mm/aaaa
    pattern1 = re.compile(r"(\d{1,2})/(\d{1,2})/(\d{4})")
    text = pattern1.sub(replacer, text)
    
    # 2️⃣ jj Month yyyy
    pattern2 = re.compile(r"(\d{1,2})\s([a-zA-Z]+)\s(\d{4})")
    text = pattern2.sub(replacer, text)
    
    return text

# Fonction pour extraire les entités
def extract_entities(text):
    doc = nlp(text)
    entities = {"PER": [], "LOC": [], "ORG": []}
    for ent in doc.ents:
        if ent.label_ in entities:
            entities[ent.label_].append(ent.text)
    return entities

def extract_email(text):
    match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    return match.group(0) if match else "unknown"

def extract_phone(text):
    match = re.search(r"\+?\d[\d\s]{7,}", text)
    return match.group(0) if match else "unknown"

def extract_birthdate(text):
    pattern = r"(\d{2}-\d{2}-\d{4})"
    match = re.search(pattern, text)
    return match.group(0) if match else "unknown"

def extract_university_regex(text):
    # Cherche après 'étudiant', 'étudier', 'inscrit'
    match = re.search(r"(?:étudiant(?:e)?|étudier|inscrit(?:e)?)\s+(?:à|en)\s+([A-Z][\w\s\-']+)", text)
    if match:
        return match.group(1)
    return None

def extract_location_regex(text):
    # Cherche après 'résidant', 'habite'
    match = re.search(r"(?:résidant(?:e)?|habite)\s+à\s+([A-Z][\w\s\-']+)", text)
    if match:
        return match.group(1)
    return None


# 🔹 Fonction build_profile
def build_profile(text):
    # spaCy NER
    doc = nlp(text)

    profile = {"name": "unknown", "location": "unknown", 
               "university": "unknown",
               "email": "unknown", "phone": "unknown",
               "birthdate": "unknown"}

    # Liste de mots invalides pour le nom
    invalid_person_words = ["etudiant", "etudiante", "professeur", 
                            "ingénieur", "chercheur", "doctorant", "stagiaire"]

    # NER pour Location et University
    for ent in doc.ents:
        if ent.label_ == "LOC":
            profile["location"] = ent.text
        if ent.label_ == "ORG":
            profile["university"] = ent.text

    # Fallback regex pour University et Location
    uni_fallback = extract_university_regex(text)
    if uni_fallback:
        profile["university"] = uni_fallback
    
    loc_fallback = extract_location_regex(text)
    if loc_fallback:
        profile["location"] = loc_fallback

    # 🔹 Nom : priorité à la regex "Je suis / Je m'appelle"
    match_name = re.search(
        r"(?:Je m'appelle|Je suis)\s+([A-Z][a-z]+(?:[-\s][A-Z][a-z]+)*)",
        text
    )
    if match_name:
        profile["name"] = match_name.group(1)
    else:
        # Sinon, prendre le premier PER valide détecté par spaCy
        for ent in doc.ents:
            if ent.label_ == "PER":
                if ent.text.lower() not in invalid_person_words:
                    profile["name"] = ent.text
                    break

    # Email
    email_match = re.search(r"[\w\.-]+@[\w\.-]+", text)
    if email_match:
        profile["email"] = email_match.group(0)
    
    # Téléphone
    phone_match = re.search(r"\+?\d[\d\s]{7,}", text)
    if phone_match:
        profile["phone"] = phone_match.group(0)
    
    # Date de naissance
    date_match = re.search(r"(\d{2}-\d{2}-\d{4})", text)
    if date_match:
        profile["birthdate"] = date_match.group(1)

    return profile


# 🔹 Streamlit UI
st.title("🧠 Extraction de Profil Avatar 🧠")

text_input = st.text_area("Présentez-vous pour créer votre profil :")

if st.button("Générer le profil"):
    if text_input.strip() == "":
        st.warning("Veuillez entrer un texte.")
    else:
        text_input = normalize_text(text_input)
        text_input = normalize_date(text_input)
        profile = build_profile(text_input)

        # 🔹 Avatar cartoon via DiceBear (styles variés)
        styles = ["adventurer", "avataaars", "bottts", "pixel-art", "micah"]
        style = random.choice(styles)
        # Seed unique pour nom ou aléatoire
        seed = profile['name'] + str(int(time.time())) if profile['name'] != "unknown" else str(random.randint(1,100000))
        avatar_url = f"https://api.dicebear.com/6.x/{style}/svg?seed={seed}"

        # 🔹 Affichage du profil
        st.subheader("🎯 Mon profil")
        cols = st.columns([1,2])
        cols[0].image(avatar_url, width=200)
        with cols[1]:
            st.markdown(f"**Nom Et Prénom:** {profile['name']}")
            st.markdown(f"**Université:** {profile['university']}")
            st.markdown(f"**Adresse:** {profile['location']}")
            st.markdown(f"**Date De Naissance:** {profile['birthdate']}")
            st.markdown(f"**Email:** {profile['email']}")
            st.markdown(f"**Téléphone:** {profile['phone']}")

