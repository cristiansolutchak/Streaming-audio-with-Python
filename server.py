import json
import os
import socket
import threading
import time
import wave

HOST = "127.0.0.1"
TCP_ADDRESS = (HOST, 9090)
UDP_ADDRESS = (HOST, 9191)

SONGS_PATH = "server/songs"
CHUNK = 1024

server_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_tcp.bind(TCP_ADDRESS)

server_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_udp.bind(UDP_ADDRESS)

clients = []

songs = []

for song_index, song_path in enumerate(os.listdir(SONGS_PATH)):
    last_dot_index = song_path.rfind(".")
    song_name = song_path[:last_dot_index]
    song = {
        "id": song_index,
        "name": song_name, 
        "path": f"server/songs/{song_path}",
    }
    songs.append(song)

song_choices_data = json.dumps(songs).encode()

def send_tcp(data, client):
    client.settimeout(2)
    client.sendall(data)
    client.settimeout(None)

def send_udp(message, address):
    server_udp.sendto(message, address)
    server_udp.recvfrom(1024)

def disconnect_client(client):
    clients.remove(client)
    client.close()

def handle_client(client, client_address):
    print(f"[CONEXÃO] Nova conexão de: {client_address}")

    clients.append(client)

    print(f"[CONEXÃO] Total de conexões: {len(clients)}")

    try:
        send_tcp(song_choices_data, client)

        chosen_song_data = client.recv(CHUNK)
        chosen_song = json.loads(chosen_song_data.decode())
        
        wave_file = wave.open(chosen_song["path"], "rb")

        audio_stream_configuration = {
            "width": wave_file.getsampwidth(),
            "channel_amount": wave_file.getnchannels(),
            "framerate": wave_file.getframerate(),
            "frames_amount": wave_file.getnframes(),
        }

        audio_stream_configuration_data = json.dumps(audio_stream_configuration).encode()
        send_tcp(audio_stream_configuration_data, client)

        _, client_udp_address = server_udp.recvfrom(CHUNK)

        while True:
            frames = wave_file.readframes(CHUNK)

            if not frames:
                break

            server_udp.sendto(frames, client_udp_address)
            # send_udp(frames, client_udp_address)
            time.sleep(0.01)
    # except:
        # pass
    finally:
        print(f"[CONEXÃO] Cliente em {client_address} desconectou")

        wave_file.close()
        disconnect_client(client)

def start():
    server_tcp.listen()

    print("[INICIANDO] Servidor iniciando ...")

    while True:
        client, client_address = server_tcp.accept()
        
        handle_client_thread = threading.Thread(
            target=handle_client,
            args=(client, client_address)
        )

        handle_client_thread.start()

try:
    start()
finally:
    print("[FECHANDO] Fechando servidor ...")

    server_tcp.close()
    server_udp.close()