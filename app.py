from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from stl import mesh
import os
import math

# Configurações
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'stl'}
PRECO_FILAMENTO = 68  # Valor do filamento por grama
PESO_FILAMENTO = 1000  # Peso do rolo de filamento em gramas
DENSIDADE_FILAMENTO = 1.24  # Densidade em g/cm³
DIAMETRO_FILAMENTO = 1.75  # Diâmetro do filamento em mm
VELOCIDADES_IMPRESSAO = {'normal': 50, 'alta': 80}  # Velocidade de impressão (mm/s)
LUCRO = 1.5  # Margem de lucro

# Cria o app Flask
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Função para verificar se o arquivo é um STL
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Função para fazer o upload do arquivo STL
def upload_stl(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return filepath
    return None

# Função para calcular o volume da peça a partir do arquivo STL
def volume_fatiamento(filepath):
    your_mesh = mesh.Mesh.from_file(filepath)
    volume = your_mesh.get_mass_properties()[0]  # Volume em mm³
    return volume

# Função para calcular o preço e tempo da impressão
def preco_fatiamento(volume_mm3):
    # Convertendo volume de mm³ para cm³
    volume_cm3 = volume_mm3 / 1000.0
    peso_peca = volume_cm3 * DENSIDADE_FILAMENTO  # Peso em gramas

    # Calcula o comprimento necessário de filamento em mm
    area_secao_filamento = math.pi * (DIAMETRO_FILAMENTO / 2) ** 2
    comprimento_filamento_mm = (peso_peca / DENSIDADE_FILAMENTO) / area_secao_filamento * 1000  # Convertendo para mm

    # Calcula o tempo estimado de impressão em minutos
    tempo_impressao = comprimento_filamento_mm / VELOCIDADES_IMPRESSAO['normal'] / 60  # Tempo em minutos

    # Calcula o preço da peça
    preco_por_grama = PRECO_FILAMENTO / PESO_FILAMENTO
    preco_peca = peso_peca * preco_por_grama * LUCRO
    return tempo_impressao, preco_peca

# Rota principal para exibir o formulário e resultados
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Recebe o arquivo do formulário
        file = request.files.get('file')
        filepath = upload_stl(file)
        
        if not filepath:
            return render_template("index.html", error="Arquivo inválido ou não enviado.")

        # Calcula o volume e o preço
        volume = volume_fatiamento(filepath)
        tempo_impressao, preco_peca = preco_fatiamento(volume)

        # Exclui o arquivo após o cálculo
        os.remove(filepath)

        # Passa os resultados para a página HTML
        return render_template("index.html", volume=volume, tempo=tempo_impressao, preco=preco_peca)

    return render_template("index.html")

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
