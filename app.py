import os
from flask import Flask, request, render_template, redirect, url_for, send_from_directory, flash, session

app = Flask(__name__)
# Přidání SECRET_KEY je nutné pro používání session a flash zpráv
app.secret_key = 'super_secret_key'

UPLOAD_FOLDER = 'uploaded_files'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'html', 'csv'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- Nová route pro základní URL / ---
@app.route('/')
def home():
    html_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'index.html')
    if os.path.exists(html_file_path):
        return redirect(url_for('o2site'))
    else:
        return redirect(url_for('upload_files'))

# --- Route pro nahrávání souborů ---
@app.route('/upload_files', methods=['GET', 'POST'])
def upload_files():
    if 'original_filenames' not in session:
        session['original_filenames'] = {}
        
    if request.method == 'POST':
        html_file = request.files.get('html_file')
        csv_file = request.files.get('csv_file')

        uploaded_count = 0

        # Zpracování nahrání HTML souboru
        if html_file and html_file.filename != '' and allowed_file(html_file.filename):
            html_filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'index.html')
            html_file.save(html_filepath)
            session['original_filenames']['index.html'] = html_file.filename
            flash(f'Soubor "{html_file.filename}" byl úspěšně nahrán jako index.html.', 'success')
            uploaded_count += 1
            
        # Zpracování nahrání CSV souboru
        if csv_file and csv_file.filename != '' and allowed_file(csv_file.filename):
            csv_filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'data.csv')
            csv_file.save(csv_filepath)
            session['original_filenames']['data.csv'] = csv_file.filename
            flash(f'Soubor "{csv_file.filename}" byl úspěšně nahrán jako data.csv.', 'success')
            uploaded_count += 1
            
        if uploaded_count == 0:
            flash('Nebyly nahrány žádné platné soubory. Vyberte prosím alespoň jeden soubor.', 'error')

        return redirect(url_for('upload_files'))

    return render_template('upload.html', uploaded_files=session.get('original_filenames', {}))

# --- Nová route pro smazání souboru ---
@app.route('/delete_file', methods=['POST'])
def delete_file():
    filename_to_delete = request.form.get('filename')
    
    # Bezpečnostní kontrola, aby nešlo smazat cokoliv jiného
    if filename_to_delete in ['index.html', 'data.csv']:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename_to_delete)
        if os.path.exists(file_path):
            os.remove(file_path)
            session['original_filenames'].pop(filename_to_delete, None)
            flash(f'Soubor {filename_to_delete} byl úspěšně smazán.', 'success')
        else:
            flash(f'Soubor {filename_to_delete} se nepodařilo najít.', 'error')
    else:
        flash('Neplatný požadavek na smazání souboru.', 'error')
        
    return redirect(url_for('upload_files'))

# --- Existující route pro zobrazení O2 stránky ---
@app.route('/o2site')
def o2site():
    html_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'index.html')
    if os.path.exists(html_file_path):
        return send_from_directory(app.config['UPLOAD_FOLDER'], 'index.html')
    else:
        return redirect(url_for('upload_files'))

# Route pro obsluhu dalších souborů
@app.route('/uploaded_files/<filename>')
def serve_uploaded_files(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)