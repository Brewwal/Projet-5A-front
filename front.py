from flask import Flask, render_template, request, send_file, redirect, after_this_request
import pandas as pd
import os
import shutil
#import module anon


app = Flask(__name__)
def is_valid_file(file):
    return file and file.filename.endswith('.csv')

# Répertoire de téléchargement
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Variable globale pour suivre l'état de l'application
anon_state = False

def clear_uploads_folder():
    folder_path = app.config['UPLOAD_FOLDER']
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")

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
        anon_state = True

        return render_template('index.html', toanon=toanon, anon_state=anon_state)

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
    toanon = pd.read_csv(file_path)

    # Appliquer les options d'anonymisation
    for i, option in enumerate(options):
        if option == 'delete':
            # Supprimer la colonne correspondante
            column_to_delete = toanon.columns[i]
            print(f"Deleting column: {column_to_delete}")
            toanon = toanon.drop(columns=[column_to_delete])
            print("Data after deletion:")
            print(toanon)
        elif option == 'modify':
            # Appliquer la modification selon votre logique
            pass
        # Ajoutez d'autres conditions pour les autres options

    # Enregistrez le fichier anonymisé
    anonymized_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'anonymized.csv')
    toanon.to_csv(anonymized_file_path, index=False)

    @after_this_request
    def clear_uploads(response):
        # Supprimer le fichier non-anonymisé du dossier "uploads"
        clear_uploads_folder()
        return response

    return send_file(anonymized_file_path, as_attachment=True)



if __name__ == '__main__':
    app.run(debug=True)