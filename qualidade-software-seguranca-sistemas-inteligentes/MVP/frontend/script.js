
const uploadArea = document.getElementById('upload-area');
const fileInput = document.getElementById('file-input');
const fileLink = document.getElementById('file-link');
const resultArea = document.getElementById('result-area');
const spinner = document.getElementById('spinner');

// URL da API.
const API_URL = 'http://127.0.0.1:8000/classificar';

// --- Event Listeners para Upload ---

// Abrir o seletor de arquivos ao clicar no link
fileLink.addEventListener('click', (e) => {
    e.preventDefault();
    fileInput.click();
});

// Abrir o seletor de arquivos ao clicar na área de upload
uploadArea.addEventListener('click', () => {
     fileInput.click();
});

// Lidar com o arquivo selecionado pelo input
fileInput.addEventListener('change', () => {
    const files = fileInput.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
});

// --- Lógica para arrastar e soltar (Drag and Drop) ---

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    uploadArea.addEventListener(eventName, preventDefaults, false);
});

['dragenter', 'dragover'].forEach(eventName => {
    uploadArea.addEventListener(eventName, () => uploadArea.classList.add('highlight'), false);
});

['dragleave', 'drop'].forEach(eventName => {
    uploadArea.addEventListener(eventName, () => uploadArea.classList.remove('highlight'), false);
});

uploadArea.addEventListener('drop', (e) => {
    const dt = e.dataTransfer;
    const files = dt.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
}, false);


// --- Função Principal para Enviar o Arquivo para o Classificador ---

async function handleFile(file) {
    // Limpa resultado anterior e mostra o 'spinner' de carregamento
    resultArea.textContent = '';
    resultArea.style.color = '#66FF66'; // Reseta a cor para o padrão verde
    spinner.style.display = 'block';

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            body: formData,
        });

        spinner.style.display = 'none'; // Esconde o spinner

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `Erro de servidor: ${response.status}`);
        }

        const data = await response.json();
        
        resultArea.textContent = data.resultado;

    } catch (error) {
        spinner.style.display = 'none';
        console.error('Erro ao enviar o arquivo:', error);
        resultArea.textContent = `Erro: ${error.message}`;
        resultArea.style.color = '#FF6666'; // Muda a cor do texto para vermelho em caso de erro
    }
}