from flask import Flask, render_template, request, send_file, redirect
import pandas as pd
import os
#import module anon

app = Flask(__name__)
def is_valid_file(file):
    return file and file.filename.endswith('.csv')

# Répertoire de téléchargement
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if is_valid_file(file):
        # Créer le répertoire "uploads" s'il n'existe pas
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        toanon = pd.read_csv(file_path)

        # Debug: Afficher toanon
        print(type(toanon))
        print(toanon)

        return render_template('index.html', toanon=toanon)

    else:
        return "Format de fichier non autorisé. Veuillez télécharger un fichier CSV."



@app.route('/process', methods=['POST'])
def process():
    options = request.form.getlist('options[]')

    # Charger le fichier CSV
    uploaded_files = os.listdir(app.config['UPLOAD_FOLDER'])
    if not uploaded_files:
        return "Aucun fichier CSV n'a été uploadé."

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_files[0])
    toano = pd.read_csv(file_path)

    # Appliquer les options d'anonymisation
    for i, option in enumerate(options):
        if option == 'delete':
            toanon = toanon.drop(columns=[i])
        elif option == 'modify':
            # Appliquer la modification selon votre logique
            pass
        # Ajoutez d'autres conditions pour les autres options

    # Enregistrez le fichier anonymisé
    anonymized_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'anonymized.csv')
    toanon.to_csv(anonymized_file_path, index=False)

    return send_file(anonymized_file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)