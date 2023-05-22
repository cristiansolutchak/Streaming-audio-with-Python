<!-- # Readme - Servidor de Transmissão de Áudio

Este é um código Python que implementa um servidor de transmissão de áudio. O servidor utiliza sockets TCP e UDP para se comunicar com clientes e transmitir um arquivo de áudio WAV para eles.

## Pré-requisitos

Certifique-se de ter as seguintes bibliotecas instaladas antes de executar o código:

- `socket`: Biblioteca de rede para criar e manipular sockets.
- `time`: Biblioteca para lidar com funções relacionadas ao tempo.
- `wave`: Biblioteca para ler e gravar arquivos de áudio no formato WAV.
- `json`: Biblioteca para serializar/deserializar dados no formato JSON.

## Configuração do servidor

O servidor é configurado com as seguintes constantes:

```python
HOST = socket.gethostbyname(socket.gethostname())
PORT = 5050
ADDRESS = (HOST, PORT)
MAXIMUM_CONNECTIONS_BACKLOG = 5
CHUNK = 1024
```

- `HOST`: Obtém o endereço IP da máquina em que o código está sendo executado.
- `PORT`: O número da porta em que o servidor será executado.
- `ADDRESS`: A tupla contendo o endereço IP e a porta do servidor.
- `MAXIMUM_CONNECTIONS_BACKLOG`: O número máximo de conexões pendentes permitidas pelo servidor.
- `CHUNK`: O tamanho dos chunks de áudio que serão transmitidos para o cliente.

## Configuração do servidor TCP

O servidor TCP é inicializado e vinculado ao endereço definido. Ele aguarda por conexões de clientes em uma determinada porta e imprime o endereço do cliente quando uma nova conexão é estabelecida.

```python
tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_server.bind(ADDRESS)

tcp_server.listen(MAXIMUM_CONNECTIONS_BACKLOG)
print(f'[tcp server] Listening on: {HOST}')

tcp_client, client_address = tcp_server.accept()
print(f'[tcp server] New connection from: {client_address}')
```

## Configurações do fluxo de áudio

Em seguida, o arquivo de áudio WAV é aberto e algumas configurações importantes são extraídas dele, como a largura de amostra, a quantidade de canais e a taxa de quadros. Essas configurações são armazenadas em um dicionário e serializadas em JSON para serem enviadas ao cliente.

```python
wave_file = wave.open('server/aaa.wav', 'rb')

audio_stream_configurations = {
    'width': wave_file.getsampwidth(),
    'channel_amount': wave_file.getnchannels(),
    'framerate': wave_file.getframerate(),
}

audio_stream_configurations_data = json.dumps(audio_stream_configurations)

tcp_client.sendall(bytes(audio_stream_configurations_data, 'utf-8'))
```

## Configuração do servidor UDP

O servidor UDP é inicializado e vinculado a uma porta diferente do servidor TCP. Ele espera por mensagens de início de conexão do cliente e imprime o endereço do cliente quando uma nova conexão é estabelecida.

```python
udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_server.bind((HOST, 6060))

data, client_address = udp_server.recvfrom(CHUNK)
print(f'[udp server] New connection from: {client_address}')
print(f'[udp server] Received starting message: {data.decode()}')
```

## Transmissão de áudio

Em seguida, o servidor começa a transmitir os chunks de áudio para o cliente


adicionar as bibliotecas -->

# Streaming de Áudio - Servidor

Este é um arquivo README.md que explica o código de um servidor de streaming de áudio em Python.

## Funcionalidade

O código implementa um servidor de streaming de áudio que permite que os clientes se conectem, escolham uma música e recebam os frames de áudio correspondentes para reprodução. Ele utiliza os protocolos TCP e UDP para essa finalidade.

## Dependências

O servidor de streaming de áudio requer as seguintes bibliotecas Python:

- `json`: Utilizada para codificar e decodificar dados em formato JSON.
- `os`: Utilizada para interagir com o sistema operacional e manipular arquivos e diretórios.
- `socket`: Utilizada para a comunicação por meio dos protocolos TCP e UDP.
- `threading`: Utilizada para criar threads e lidar com múltiplas conexões de clientes simultaneamente.
- `time`: Utilizada para adicionar atrasos entre o envio de frames de áudio.
- `wave`: Utilizada para ler e manipular arquivos de áudio no formato WAV.

Certifique-se de ter essas bibliotecas instaladas em seu ambiente Python antes de executar o código.

## Configuração do Servidor

Antes de iniciar o servidor, é necessário configurar algumas variáveis no código:

- `HOST`: O endereço IP do servidor. Neste caso, está definido como "127.0.0.1", que se refere ao endereço de loopback (localhost).
- `TCP_ADDRESS`: A tupla contendo o endereço IP e a porta para o servidor TCP. Neste caso, está definido como `(HOST, 9090)`.
- `UDP_ADDRESS`: A tupla contendo o endereço IP e a porta para o servidor UDP. Neste caso, está definido como `(HOST, 9191)`.
- `SONGS_PATH`: O caminho para o diretório onde as músicas estão armazenadas. Certifique-se de que as músicas estejam presentes nesse diretório.
- `CHUNK`: O tamanho do bloco de frames de áudio que será enviado de cada vez.

## Inicialização do Servidor

A função `start()` é responsável por inicializar o servidor. Ela cria os sockets TCP e UDP e configura o socket TCP para escutar por conexões entrantes. Em seguida, inicia um loop infinito para esperar por novas conexões de clientes. Quando uma nova conexão é estabelecida, é criada uma nova thread para lidar com o cliente na função `handle_client()`.

## Manipulação do Cliente

A função `handle_client(client, client_address)` é responsável por lidar com a conexão de um cliente específico. Primeiro, a lista de músicas disponíveis é convertida em formato JSON e enviada ao cliente por meio do protocolo TCP. Em seguida, o cliente envia a escolha da música e o servidor lê o arquivo de áudio correspondente.

As configurações do fluxo de áudio, como a largura dos samples, a quantidade de canais, a taxa de amostragem e a quantidade total de frames, são obtidas do arquivo WAV e também enviadas ao cliente por meio do protocolo TCP.

O endereço UDP do cliente é recebido do cliente via socket UDP. Em seguida, o servidor lê os frames de áudio do arquivo WAV e envia esses frames para o cliente por meio do socket UDP. O envio é realizado em blocos de tamanho `CHUNK` até que todos os frames ten

ham sido enviados.

## Encerramento do Servidor

Quando o servidor é encerrado, seja por uma interrupção de execução ou por qualquer outro motivo, as conexões dos sockets TCP e UDP são fechadas usando o método `close()`.

## Executando o Servidor

Para executar o servidor de streaming de áudio, siga as etapas abaixo:

1. Certifique-se de ter todas as dependências instaladas em seu ambiente Python.

2. Defina as configurações do servidor, como o endereço IP e as portas TCP e UDP, conforme necessário.

3. Verifique se o diretório especificado em `SONGS_PATH` contém os arquivos de áudio das músicas que deseja disponibilizar para streaming.

4. Execute o código Python.

5. O servidor estará ouvindo por conexões entrantes. Os clientes podem se conectar ao servidor usando o endereço IP e a porta TCP especificados.