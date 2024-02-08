from flask import Flask, render_template, request, send_file
from io import BytesIO
from pypdf import PdfReader
from wordcloud import WordCloud, STOPWORDS

app = Flask(__name__)

# Função para extrair texto do PDF
def extrair_texto_pdf(caminho_pdf):
    reader = PdfReader(BytesIO(caminho_pdf))
    texto = ""
    for pagina in reader.pages:
        texto += pagina.extract_text() if pagina.extract_text() else ''
    return texto

# Função para gerar a nuvem de palavras
def gerar_nuvem_palavras(conectivos, texto):
    nuvem_palavras = WordCloud(stopwords=conectivos, background_color='white', width=800, height=400).generate(texto)
    return nuvem_palavras

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/gerar_nuvem', methods=['POST'])
def gerar_nuvem():
    conectivos_iniciais = {"o", "de", "da", "na", "no", "esse", "aquele", "aquela", "naquele", "aquilo", "aquele", "do", "a", "e"}
    conectivos = set(STOPWORDS)
    conectivos.update(conectivos_iniciais)

    arquivo_pdf = request.files['pdf']
    conectivos_personalizados = request.form.get('conectivos', '').split(',')
    conectivos.update(map(str.strip, conectivos_personalizados))

    if arquivo_pdf:
        texto = extrair_texto_pdf(arquivo_pdf.read())
        nuvem = gerar_nuvem_palavras(conectivos, texto)

        img_buffer = BytesIO()
        nuvem.to_image().save(img_buffer, format='PNG')
        img_buffer.seek(0)

        return send_file(img_buffer, mimetype='image/png')
    else:
        return 'Erro: Nenhum arquivo PDF enviado.'

if __name__ == "__main__":
    app.run(debug=True)
