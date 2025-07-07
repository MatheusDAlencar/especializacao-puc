import pytest
from main import app  

## Testes ##
# Como o backend é simples e não tem persistência de dados, optei por deixar o teste de validação de requisitos de desemepenho no próprio Notebook e
# aqui implementar um teste de validação de respostas do classificador, que devem ser corretas, reforçando a alta precisão obtida nos testes no Notebook.

# Criação do 'client' de teste para a aplicação

@pytest.fixture
def client():
    # Coloca o app em modo de teste para facilitar a depuração
    app.config['TESTING'] = True
    # O client nos permite fazer requisições à API sem precisar rodar o servidor
    with app.test_client() as client:
        yield client

# Abaixo estão os testes da API que validam o funcionamento adequado e a precisão do classificador, conforme os testes no Notebook  

def test_classificacao_peticao_inicial(client):
    """
    Testa se o endpoint classifica corretamente um documento que É uma Petição Inicial.
    """
    file_path = 'backend\tests\dados_test\Exemplo_PI.pdf'
    
    with open(file_path, 'rb') as f:
        # O 'data' aqui simula um formulário de upload de arquivo
        data = {
            'file': (f, 'Exemplo_PI')
        }
        # Usa o client para fazer uma requisição POST para o nosso endpoint
        response = client.post('/classificar', content_type='multipart/form-data', data=data)

    # Primeiro verifica se a requisição foi bem-sucedida (código de status 200 OK)
    assert response.status_code == 200
    
    # Em seguida, converte a resposta JSON em um dicionário Python
    json_data = response.get_json()
    
    # Enfim, verifica se o resultado da classificação está correto
    assert json_data['resultado'] == "O documento é uma petição inicial"
    assert json_data['is_peticao_inicial'] is True

def test_classificacao_outro_documento(client):
    """
    Testa se o endpoint classifica corretamente um documento que NÃO É uma Petição Inicial.
    """
    file_path = 'backend\tests\dados_test\Exemplo_Contestacao.pdf'
    
    with open(file_path, 'rb') as f:
        data = {
            'file': (f, 'Exemplo_Contestacao.pdf')
        }
        response = client.post('/classificar', content_type='multipart/form-data', data=data)

    assert response.status_code == 200
    json_data = response.get_json()
    
    # Verifica se o resultado da classificação está correto para um "não-PI"
    assert json_data['resultado'] == "O documento não é uma petição inicial"
    assert json_data['is_peticao_inicial'] is False

def test_sem_arquivo_enviado(client):
    """
    Testa o comportamento da aplicação quando nenhum arquivo é enviado.
    """
    response = client.post('/classificar')
    
    # Esperamos um erro 400 (Bad Request)
    assert response.status_code == 400
    json_data = response.get_json()
    assert 'error' in json_data
    assert json_data['error'] == "Nenhum arquivo enviado."