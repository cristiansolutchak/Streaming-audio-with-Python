import json
import queue
import socket
import threading
import time
import pyaudio

SERVER_HOST = socket.gethostbyname(socket.gethostname())
SERVER_TCP_ADDRESS = (SERVER_HOST, 9090)
SERVER_UDP_ADDRESS = (SERVER_HOST, 9191)

client_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_tcp.connect(SERVER_TCP_ADDRESS)

client_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

audio = pyaudio.PyAudio()

def receive_udp(chunk):
    data = client_udp.recv(chunk)
    client_udp.sendto(b'', SERVER_UDP_ADDRESS)

    return data

def load_frames(frames_queue):
    while True:
        frames = receive_udp(4096)

        if not frames:
            break

        frames_queue.put(frames)

try:
    song_choices_data = client_tcp.recv(1024)
    song_choices = json.loads(song_choices_data.decode())

    for index, song in enumerate(song_choices):
        print(f"{index + 1} - {song['name']}")

    print()

    chosen_song = None

    while not chosen_song:
        chosen_song_input = input("Insira uma música (id): ")

        if not chosen_song_input.isdigit():
            print("Valor inválido! Insira apenas inteiros.")
            continue

        chosen_song_id = int(chosen_song_input) - 1

        for song in song_choices:
            if song["id"] == chosen_song_id:
                chosen_song = song
                break
        
        if not chosen_song:
            print("Valor inválido! Escolha apenas os IDs disponíveis.")

    chosen_song_data = json.dumps(chosen_song).encode()
    client_tcp.sendall(chosen_song_data)

    audio_stream_configuration_data = client_tcp.recv(1024)
    audio_stream_configuration = json.loads(audio_stream_configuration_data.decode())

    audio_stream = audio.open(
        format=audio.get_format_from_width(
            audio_stream_configuration["width"]
        ),
        channels=audio_stream_configuration["channel_amount"],
        rate=audio_stream_configuration["framerate"],
        output=True,
        frames_per_buffer=4096
    )

    client_udp.sendto(b'',  SERVER_UDP_ADDRESS)

    frames_queue = queue.Queue(maxsize=audio_stream_configuration["frames_amount"])

    load_frames_thread = threading.Thread(
        target=load_frames, 
        args=(frames_queue,)
    )
    load_frames_thread.start()

    print(f"Agora tocando: {chosen_song['name']}")

    time.sleep(1)

    while not frames_queue.empty():
        frames = frames_queue.get()
        audio_stream.write(frames)
finally:
    client_tcp.close()
    audio_stream.close()
    audio.terminate()