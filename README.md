# Virtual Coach

Virtual Coach – Uma aplicação de inteligência artificial para o monitoramento de atividades físicas e predição de gastos calóricos

https://user-images.githubusercontent.com/26602158/186296067-0c249aa4-ef7a-454c-adb3-db3632a66906.mp4?width=300&height=300

A Figura a seguir apresenta uma visão geral do experimento desenvolvido para o monitoramento de atividade física. Na etapa 1 é possível registrar por meio de uma câmera uma pose inicial e final para que a aplicação capture as coordenadas e aprenda os estados definidos como corretos. Na etapa 2 a aplicação inicia o monitoramento pela câmera da execução da pose inicial e final do exercício para o qual foi treinada, provendo feedback em tempo real para que o usuário possa acompanhar a qualidade da execução e corrigir sua postura durante a execução do exercício, bem como monitorar a frequência cardíaca por meio da smart band Miband 4. Por fim na etapa 3 é possível realizar a análise dos resultados obtidos comparando a execução com as posições de referência e avaliar o esforço despendido pela medição da frequência cardíaca durante a execução.

<img src="https://github.com/trgrocha/VirtualCoach/blob/main/imagens/overview.png"/>

Ambiente utilizado para o desenvolvimento Linux Ubuntu 22.04.1 LTS.<br>
A aplicação foi desenvolvida me linguagem de programação Python 3.9.2 utilizando as seguintes bibliotecas. <br>
<br>
• scikit-learn - 1.1.1<br>
• pandas - 1.4.1<br>
• numpy - 1.19.5<br>
• opencv-python -4.5.3.56<br>
• mediapipe - 0.8.7.2<br>
• curses-menu - 0.5.0<br>
• bluepy.btle – 1.3.0<br>

<h1>Tela da aplicação e suas funcionalidades</h1>

<img src="https://github.com/trgrocha/VirtualCoach/blob/main/imagens/menu.png"/>

Descrição das funcionalidades: <br>

1 - Restart Learning - Função que apaga o arquivo onde são armazenadas as posições do corpo humano.<br>
2 - Inform training position - Função que captura as posições do corpo humano a partir da câmera.<br>
3 - Execute Learning - Função que executa o processo de aprendizado para classificar as posições capturadas.<br>
4 - Test Learning - Função para realização dos testes após a realização do aprendizado.<br>
5 - Prediction of calories burned - Função para predição de gasto calorico com bases na média da freqência cardíaca.<br>
6 - Heart Rate Monitor - Função que monitora a freqência cardíaca em tempo real a partir da smart band da Xiomi.<br>
<br>

Monitoramento em tempo real da freqência cardíaca

<img src="https://github.com/trgrocha/VirtualCoach/blob/main/imagens/monitor.jpg"/>

