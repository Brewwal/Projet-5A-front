from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

# Fonction pour initialiser l'objet pandas
def init_pandas_object():
    data = {
        'Nom': ['John Doe', 'Jane Doe'],
        'Âge': [30, 25],
        'Ville': ['New York', 'Los Angeles']
    }
    df = pd.DataFrame(data)
    return df

# Route pour afficher la page HTML avec le tableau
@app.route('/')
def index():
    pandas_object = init_pandas_object()
    return render_template('table.html', pandas_object=pandas_object)

if __name__ == '__main__':
    app.run(debug=True)