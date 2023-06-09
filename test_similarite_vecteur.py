import streamlit as st
import spacy
from sklearn.metrics.pairwise import cosine_similarity
import csv

nlp = spacy.load("fr_dep_news_trf")

# Fonction pour effectuer l'analyse de comparaison de similarité
def compare_similarity(terms):
    similarites = []

    for i in range(len(terms)):
        for j in range(i + 1, len(terms)):  # Commencer la boucle à i + 1 au lieu de 0 afin d'éviter les analyses redondantes
            if i != j:
                terme1 = terms[i]
                terme2 = terms[j]

                doc1 = nlp(terme1)
                doc2 = nlp(terme2)

                print(f"\nvecteur 1 : {doc1.vector}")
                print(f"\nvecteur 2 : {doc2.vector}")

                # Vérifier si les deux termes existent
                if doc1.has_vector and doc2.has_vector:
                    similarity = cosine_similarity([doc1.vector], [doc2.vector])

                    similarites.append({
                        "Terme 1": terme1,
                        "Terme 2": terme2,
                        "Score de similarité": similarity[0][0]
                    })

    print(f'smilarites : {similarites}')
    return similarites

# Fonction pour exporter les résultats au format CSV
def export_to_csv(data):
    csv_file = "resultats_similarite.csv"
    with open(csv_file, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["Terme 1", "Terme 2", "Score de similarité"])
        writer.writeheader()
        writer.writerows(data)

    return csv_file

# Configuration de l'application Streamlit
st.title("Comparaison de Similarité")
st.sidebar.title("Paramètres")

# Champ de texte pour saisir les termes à comparer
terms_input = st.sidebar.text_area("Termes à comparer (un terme par ligne)")

if st.sidebar.button("Comparer"):
    # Séparer les termes saisis en une liste
    terms = terms_input.split("\n")

    # Effectuer l'analyse de comparaison de similarité
    similarites = compare_similarity(terms)

    # Création du tableau final avec trois colonnes
    tableau_final = []
    for similarite in similarites:
        tableau_final.append(similarite)

    # Ajouter une nouvelle colonne "risque" au tableau final
    for row in tableau_final:
        score_similarite = row['Score de similarité']
        
        if score_similarite > 0.7:
            row['Risque'] = "Risque fort de cannibalisation"
        elif score_similarite > 0.4:
            row['Risque'] = "Risque moyen de cannibalisation"
        else:
            row['Risque'] = "Risque faible de cannibalisation"
    
    tableau_final_trie = sorted(tableau_final, key=lambda x: x['Score de similarité'], reverse=True)

    # Afficher le tableau final trié
    st.table(tableau_final_trie)



    #if st.sidebar.button("Exporter"):
        # Exporter les résultats au format CSV
        # csv_file = export_to_csv(tableau_final)

        # Afficher le bouton de téléchargement du fichier CSV
        #st.sidebar.download_button(label="Télécharger le fichier CSV",data="tableau_final")
