# Streaming de Áudio - Cliente

Este é um arquivo README.md que explica o código de um cliente de streaming de áudio em Python.

## Funcionalidade

O código implementa um cliente de streaming de áudio que se conecta a um servidor, escolhe uma música para reprodução e recebe os frames de áudio correspondentes para reprodução local. Ele utiliza os protocolos TCP e UDP para essa finalidade.

## Dependências

O cliente de streaming de áudio requer as seguintes bibliotecas Python:

- `json`: Utilizada para codificar e decodificar dados em formato JSON.
- `socket`: Utilizada para a comunicação por meio dos protocolos TCP e UDP.
- `threading`: Utilizada para criar threads para receber os frames de áudio.
- `time`: Utilizada para adicionar atrasos entre o recebimento de frames de áudio.
- `pyaudio`: Utilizada para reproduzir o áudio recebido.

Certifique-se de ter essas bibliotecas instaladas em seu ambiente Python antes de executar o código.

## Configuração do Cliente

Antes de executar o cliente, é necessário configurar algumas variáveis no código:

- `SERVER_HOST`: O endereço IP do servidor ao qual o cliente se conectará. Neste caso, está definido como "127.0.0.1", que se refere ao endereço de loopback (localhost).
- `SERVER_TCP_ADDRESS`: A tupla contendo o endereço IP e a porta para o servidor TCP. Neste caso, está definido como `(SERVER_HOST, 9090)`.
- `SERVER_UDP_ADDRESS`: A tupla contendo o endereço IP e a porta para o servidor UDP. Neste caso, está definido como `(SERVER_HOST, 9191)`.

Certifique-se de que o servidor esteja em execução e configurado corretamente antes de iniciar o cliente.

## Executando o Cliente

Para executar o cliente de streaming de áudio, siga as etapas abaixo:

1. Certifique-se de ter todas as dependências instaladas em seu ambiente Python.

2. Defina as configurações do cliente, como o endereço IP e as portas TCP e UDP do servidor, conforme necessário.

3. Execute o código Python.

4. O cliente se conectará ao servidor e receberá as opções de músicas disponíveis.

5. Escolha uma música digitando o ID correspondente.

6. O cliente enviará a escolha da música ao servidor e receberá as configurações do fluxo de áudio.

7. O cliente iniciará a reprodução do áudio recebido por meio do PyAudio.

8. Aguarde até que a reprodução seja concluída.

9. O cliente será encerrado, fechando as conexões TCP e liberando os recursos de áudio.

Certifique-se de ter uma conexão de rede adequada para se comunicar com o servidor e receber os dados de áudio corretamente. Para que a conexão ocorra de forma correta o servidor e o clinte devem estar na mesma rede local.