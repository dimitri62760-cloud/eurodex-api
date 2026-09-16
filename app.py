import os
import cv2
import numpy as np
from flask import Flask, request, jsonify

app = Flask(__name__)

# Base de données de référence sur le serveur (Nom, Année, et nom du fichier image associé)
# Ces images devront être stockées dans un dossier "images" sur ton serveur
COINS_DATABASE = [
    {"title": "Traité de Rome [France]", "year": "2007", "filename": "france_co2007.jpg"},
    {"title": "Présidence française de l'UE [France]", "year": "2008", "filename": "france_co2008.jpg"},
    {"title": "10 ans de l'UEM [France]", "year": "2009", "filename": "france_co2009.jpg"},
    {"title": "Pièce courante (Arbre / Semeuse) [France]", "year": "1999", "filename": "france_2euro.jpg"}
]

@app.route('/', methods=['GET'])
def home():
    return "Serveur Eurodex API actif et intelligent !"

@app.route('/scan', methods=['POST'])
def scan_coin():
    if 'image' not in request.files:
        return jsonify({'error': 'Aucune image reçue'}), 400
        
    file = request.files['image']
    uploaded_path = "temp_scan.jpg"
    file.save(uploaded_path)
    
    try:
        # Charger l'image envoyée par le téléphone en nuances de gris
        img_cap = cv2.imread(uploaded_path, cv2.IMREAD_GRAYSCALE)
        if img_cap is None:
            return jsonify({'error': 'Image invalide'}), 400

        # Normaliser l'image capturée à une taille fixe (ex: 32x32 pixels) pour la comparaison
        small_cap = cv2.resize(img_cap, (32, 32))

        best_match = COINS_DATABASE[0]
        min_diff = float('inf')

        # Comparer avec chaque pièce de référence stockée sur le serveur
        for coin in COINS_DATABASE:
            ref_path = os.path.join("images", coin["filename"])
            if os.path.exists(ref_path):
                img_ref = cv2.imread(ref_path, cv2.IMREAD_GRAYSCALE)
                if img_ref is not None:
                    small_ref = cv2.resize(img_ref, (32, 32))
                    
                    # Calcul de la différence absolue entre les pixels
                    diff = np.sum(cv2.absdiff(small_cap, small_ref))
                    
                    if diff < min_diff:
                        min_diff = diff
                        best_match = coin

        # Nettoyage du fichier temporaire
        if os.path.exists(uploaded_path):
            os.remove(uploaded_path)

        # Renvoyer le vrai résultat trouvé par le serveur
        return jsonify({
            'status': 'success',
            'title': best_match['title'],
            'year': best_match['year']
        })

    except Exception as e:
        if os.path.exists(uploaded_path):
            os.remove(uploaded_path)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)