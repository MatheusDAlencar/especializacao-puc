# Meu Front

Este pequeno projeto é o trabalho final da Disciplina **Sprint: Qualidade de Software, Segurança e Sistemas Inteligentes** 

O objetivo aqui é demonstrar o aprendizado obtido a partir das aulas.

O projeto se baseia em um projeto real que toquei ao longo de 2025. Trata-se de um classificador de documentos. Ele se faz necessário porque, em
geral, os sistemas de processo judicial eletrônico sofrem muito com inputs de dados imprecisos dos usuários e um classificador de petições iniciais
seria um primeiro passo muito importante visando o objetivo final de correção do problema apontado. Esse problema é particularmente importante porque
ele é a causa da extrema dificuldade atual de planejar qualquer estruturação do Sistema de Justiça com base em dados, visando aumentar sua eficiência.
Em síntese, as informações disponíveis não são confiáveis, uma vez que são extraídas dos sistemas de processo judicial eletrônico, mas eles são 
alimentados por usuários do mundo jurídico, que, na média, têm muito baixo cuidado com a precisão e qualidade dos dados que são inseridos nos sistemas.
Isso leva a problemas como, por exemplo, não se saber exatamente quantos processos de cada matéria existem de fato, uma vez que isso dependeria de 
uma adequada classificação de classe e assunto de todos os processos conforme as tabelas processuais unificadas do CNJ 
(conferir em: <https://www.cnj.jus.br/sgt/consulta_publica_assuntos.php> e <https://www.cnj.jus.br/sgt/consulta_publica_classes.php>).
Como isso não ocorre, fica-se sem saber a realidade do que se discute de fato no Judiciário. Para corrigir esse problema, seria necessário automatizar
a reclassificação de classes e assuntos dos processos. Isso, contudo, traz outro problema anterior: quais documentos servem para reclassificar classe
e assunto de um processo em andamento? Aí entra o papel do classificador de documentos. Em geral, o documento que delimita a classe e o assunto de um
processo é a petição inicial, daí a importância de saber se um documento é ou não petição inicial, para, por meio dele, no futuro, encontrar a classe
e o assunto de um processo judicial, permitindo a correção das bases de dados e diagnósticos mais precisos da realidade do Judiciário, viabilizando
modelos de gestão baseados em evidências e, em última instância, a eficiência administrativa na prestação do serviço de Justiça aos cidadãos que mais
necessitam da pronta e justa resposta judicial.

---
## Como executar

Basta fazer o download do projeto e abrir o arquivo index.html no seu browser.
