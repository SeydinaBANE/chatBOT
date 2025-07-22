Ce projet est un chatbot minimal en Python utilisant LangChain et le modèle LLaMA via Ollama, avec une interface web simple réalisée avec Streamlit.



Fonctionnalités :

Pose des questions en langage naturel
Réponses générées via un modèle LLaMA local (via Ollama)
Interface web simple et réactive avec Streamlit
Historique de conversation basique


Installation :

git clone https://github.com/ton_utilisateur/nom_du_depot.git
cd nom_du_depot

Installer les dépendances :

pip install streamlit langchain langchain-community

Télécharger le modèle Ollama :

ollama pull tinyllama

Utilisation :

streamlit run app.py
