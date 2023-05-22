# Readme - Cliente de Recebimento de Áudio

Este é um código Python que implementa um cliente para receber e reproduzir um stream de áudio transmitido por um servidor. O cliente utiliza sockets TCP e UDP para se comunicar com o servidor e receber os dados de áudio.

## Pré-requisitos

Certifique-se de ter as seguintes bibliotecas instaladas antes de executar o código:

- `socket`: Biblioteca de rede para criar e manipular sockets.
- `json`: Biblioteca para serializar/deserializar dados no formato JSON.
- `audio_stream`: Biblioteca que lida com a reprodução de áudio em tempo real.
- `pyaudio`: Biblioteca de áudio para a captura e reprodução de áudio.

## Configuração do cliente

O cliente é configurado com as seguintes constantes:

```python
SERVER_HOST = '10.0.25.93'
SERVER_PORT = 5050
SERVER_ADDRESS = (SERVER_HOST, SERVER_PORT)
CHUNK = 1024
```

- `SERVER_HOST`: O endereço IP do servidor ao qual o cliente irá se conectar.
- `SERVER_PORT`: O número da porta do servidor.
- `SERVER_ADDRESS`: A tupla contendo o endereço IP e a porta do servidor.
- `CHUNK`: O tamanho dos chunks de áudio que serão recebidos do servidor.

## Configurações do stream de áudio

O cliente estabelece uma conexão TCP com o servidor e recebe as configurações do stream de áudio em formato JSON. Essas configurações incluem a largura de amostra, a quantidade de canais e a taxa de quadros.

```python
tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_client.connect(SERVER_ADDRESS)

audio_stream_configurations_data_string = tcp_client.recv(CHUNK).decode()
audio_stream_configurations = json.loads(audio_stream_configurations_data_string)
```

## Configuração do stream de reprodução

O cliente utiliza a biblioteca `pyaudio` para configurar o stream de reprodução de áudio. As configurações obtidas do servidor são utilizadas para definir a largura de amostra, a quantidade de canais e a taxa de quadros do stream.

```python
py_audio = PyAudio()

audio_stream = PyAudioStream(
    audio=py_audio,
    width=audio_stream_configurations['width'],
    channel_amount=audio_stream_configurations['channel_amount'],
    framerate=audio_stream_configurations['framerate'],
)
```

## Configuração do cliente UDP

O cliente estabelece uma conexão UDP com o servidor enviando uma mensagem de início de conexão. Neste exemplo, a mensagem é simplesmente "Hello World".

```python
udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_client.sendto(b'Hello World', (SERVER_HOST, 6060))
```

## Recebimento e reprodução do áudio

O cliente inicia um loop em que recebe os chunks de áudio do servidor através do socket UDP e os escreve no stream de reprodução.

```python
try:
    data = udp_client.recv(4096)

    while data:
        data = udp_client.recv(4096)
        audio_stream.write(data)
```

## Finalização do cliente

Após a conclusão do loop de recebimento de áudio, o cliente finaliza o stream de reprodução, termina a instância do `pyaudio` e fecha as conexões com os sockets.

```python
finally:
    audio_stream.stop()
    py_audio.terminate()
    udp_client.close()
