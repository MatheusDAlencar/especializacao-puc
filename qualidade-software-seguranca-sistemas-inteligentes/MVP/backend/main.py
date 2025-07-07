from flask import Flask, request, jsonify
from flask_cors import CORS
from pdf2image import convert_from_path
from PIL import Image
from scipy.sparse import hstack, csr_matrix
import os
import re
import joblib
import pandas as pd
import pytesseract
import traceback
import io
import tempfile

## 1. CONFIGURAÇÃO DA APLICAÇÃO E CARREGAMENTO DOS MODELOS DESENVOLVIDOS NO COLAB ## 

app = Flask(__name__)
CORS(app)

try:
    MODEL_PATH = "modelo_peticao_inicial.pkl"
    VECTORIZER_PATH = "vectorizer_peticao.pkl"
    
    # Carrega o modelo vencedor (CART) e o vetorizador
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
    print("Modelo (CART) e Vetorizador carregados com sucesso.")
except FileNotFoundError:
    print(f"Erro: Arquivos de modelo não encontrados. Certifique-se de que '{MODEL_PATH}' e '{VECTORIZER_PATH}' estão na mesma pasta.")
    model = None
    vectorizer = None

# Novamente vão ser percebidas várias ações de logs e respostas de funcionamento das features,
# porque há importante preocupção aqui acerca da performance

## 2. REPLICAÇÃO DA PIPELINE DE PRÉ-PROCESSAMENTO ##

# Optei por replicar aqui por motivos de integração e desempenho
# É justamente o mesmo que se encontra no Notebook

strong_signals = {
    "enderecamento": [r"\bEXCELENT[ÍI]SSIMO(?:A)?\s+SENHOR(?:A)?\s+JUIZ(?:A)?\b", r"\bEXMO(?:\.|º)?\s+SR(?:\.|ª)?\s+DR(?:\.|ª)?\s+JUIZ\b"],
    "tutela": [r"\b(?:[IVX]+|\d+\.)?DA[S]?\s+TUTELA[S]?\s+(?:DE\s+)?(?:URG[ÊE]NCI?A|PROVIS[ÓO]RIA|ANTECIPADA)\b", 
               r"\bNECESS[ÁA]RIO\s+DEFERIMENTO\s+DA\s+TUTELA\b", r"\b(?:[IVX]+|\d+\.)?DO[S]?\s+(?:PEDID[OÓ]?[S]?\s+)?(?:DE\s+)?LIMINAR[ES]?\b", 
               r"\bTUTELA\s+ANTECIPADA\b"],
    "provas": [r"\b(?:[IVX]+|\d+\.)?(?:PROTESTA\s+(?:POR|O\s+POR)|REQUER\s+(?:O[A]?\s+PRODU[ÇC][ÃA]O\s+DE)?)\s+PROVA[S]?\b", 
               r"\bREQUER\s+PROVA[S]?\b"],
    "encerramento": [r"\b(?:[IVX]+|\d+\.)?(?:TERMO[S]?\s+EM\s+QUE|NESTE[S]?\s+TERMOS)\b", r"\bP\.?E\.?D\.?\b", 
                     r"\b(?:[LO]CAL(?:IDADE)?|CIDADE)\s*[,;]?\s*\d{1,2}\s+DE\s+\w+\s+DE\s+\d{4}\b"],
    "citacao": [r"\b(?:[IVX]+|\d+\.)?(?:A\s+)?CITA[ÇC][AÃ]?[OÃ]?[S]?\s+(?:DA[S]?\s+)?(?:REQUERIDA[S]?|REQUERIDO[S]?)\b"],
    "preliminares": [r"\b(?:[IVX]+|\d+\.)?DO[S]?\s+PRELIMINAR[ES]?\b"],
    "justica_gratuita": [r"\b(?:[IVX]+|\d+\.)?DA[S]?\s+(?:GRATUIDADE[S]?\s+(?:DE\s+)?JUSTI[ÇC]A|JUSTI[ÇC]A\s+GRATUITA)\b", 
                         r"\bGRATUIDADE\s+DOS\s+EMOLUMENTOS\b"],
    "prioridade": [r"\b(?:[IVX]+|\d+\.)?DA[S]?\s+PRIORIDADE\s+NA\s+TRAMITA[ÇC][ÃA]O\s+PROCESSUAL\b"],
    "acao": [r"\bA[ÇC][ÃA]O\s+(?:DE|REVISIONAL|MONIT[ÓO]RIA|ORDIN[ÁA]RIA|CAUTELAR|INDENIZAT[ÓO]RIA)\b", 
             r"\bEXECU[ÇC][ÃA]O\s+DE\s+T[ÍI]TULO\s+EXTRAJUDICIAL\b", r"\bVEM\s+PROPOR\b"],
}

def extract_text_from_file(file_path: str, filename: str) -> str:
    text = ""
    try:
        if filename.lower().endswith('.pdf'):
            pages = convert_from_path(file_path)
            for page in pages:
                text += pytesseract.image_to_string(page, lang='por')
        elif filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            image = Image.open(file_path)
            text = pytesseract.image_to_string(image, lang='por')
    except Exception as e:
        print(f"Erro ao processar o arquivo {filename}: {e}")
        traceback.print_exc()
        raise e
    return text

def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d+', '', text)
    text = text.strip()
    return text

def extract_regex_features(text: str, signal_dict: dict) -> dict:
    features = {}
    for category, patterns in signal_dict.items():
        count = sum(len(re.findall(pattern, text, re.IGNORECASE)) for pattern in patterns)
        features[f"feature_{category}"] = count
    return features

def preprocess_and_featurize(text: str):
    cleaned_text = clean_text(text)
    regex_features = extract_regex_features(text, strong_signals)
    regex_features_df = pd.DataFrame([regex_features])
    X_tfidf = vectorizer.transform([cleaned_text])
    X_regex = csr_matrix(regex_features_df.values)
    X_combined = hstack([X_tfidf, X_regex])
    return X_combined

## 3. DEFINIÇÃO DO ENDPOINT QUE SERÁ CONSUMIDO PELA INTERFACE DO APLICAÇÃO FULLSTACK ##

@app.route('/classificar', methods=['POST'])
def classificar_documento():
    if not model or not vectorizer:
        return jsonify({"error": "Modelo não carregado. Verifique os logs do servidor."}), 500

    if 'file' not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado."}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "Nenhum arquivo selecionado."}), 400

# Quando o usuário subir seu documento, precisamos salvar como temp file para ter o armazenamento temporário e permitir processar o resultado
   
    try:
        with tempfile.NamedTemporaryFile(delete=True, suffix=os.path.splitext(file.filename)[1]) as temp:
            file.save(temp.name)
            extracted_text = extract_text_from_file(temp.name, file.filename)

        if not extracted_text.strip():
            return jsonify({"error": "Não foi possível extrair texto do documento."}), 400

        features = preprocess_and_featurize(extracted_text)

        # Trazendo o modelo vencedor para classificar e dizer se o documento oferecido pelo usuário é ou não petição inicial
        
        try:
            prediction = model.predict(features)
        except Exception as e:
            return jsonify({"error": f"Erro durante a predição: {e}"}), 500

        is_peticao_inicial = bool(prediction[0])
        resultado = "O documento é uma petição inicial" if is_peticao_inicial else "O documento não é uma petição inicial"
        
        return jsonify({
            "filename": file.filename,
            "is_peticao_inicial": is_peticao_inicial,
            "resultado": resultado
        })

    except Exception as e:
        return jsonify({"error": f"Ocorreu um erro inesperado: {str(e)}"}), 500

@app.route("/")
def index():
    return "API do Classificador de Petição Inicial está no ar. Use a interface para enviar um documento para o classificador."

if __name__ == '__main__':
    app.run(debug=True, port=8000)