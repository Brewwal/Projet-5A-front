from flask import Flask, render_template, request, send_file
import os
#import ARX ?

app = Flask(__name__)

# Répertoire de téléchargement
DOWNLOAD_FOLDER = 'uploads'
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    # Vérifier si le formulaire est soumis correctement
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    # Vérifier si le fichier est sélectionné
    if file.filename == '':
        return redirect(request.url)

    # Vérifier si le fichier est autorisé
    if file and file.filename.endswith('.csv'):
        # Sauvegarder le fichier dans le répertoire d'uploads
        file_path = os.path.join(app.config['DOWNLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Appeler votre module de traitement avec le chemin du fichier
        #Module resultat_path = votre_module_de_anonymisation.anonymiser(file_path)

        # Retourner le chemin du fichier anonymisé pour le téléchargement
        return send_file(resultat_path, as_attachment=True)

    else:
        return "Format de fichier non autorisé. Veuillez télécharger un fichier CSV."

if __name__ == '__main__':
    app.run(debug=True)