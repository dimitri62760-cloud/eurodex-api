import os
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "Serveur Eurodex API actif !"

@app.route('/scan', methods=['POST'])
def scan_coin():
    if 'image' not in request.files:
        return jsonify({'error': 'Aucune image reçue'}), 400

    file = request.files['image']
    image_path = "temp_scan.jpg"
    file.save(image_path)

    # Simulation de reconnaissance (on améliorera la logique plus tard)
    result_title = "Traité de Rome [France]"
    result_year = "2007"

    if os.path.exists(image_path):
        os.remove(image_path)

    return jsonify({
        'status': 'success',
        'title': result_title,
        'year': result_year
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)