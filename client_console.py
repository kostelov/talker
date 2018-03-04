from client import User
from handler import ConsoleReceiver, ConsoleSender
from threading import Thread

client = User('Nick')
client.start()

listener = ConsoleReceiver(client.sock)
thread_listener = Thread(target=listener.pull)
thread_listener.daemon = True
thread_listener.start()

speaker = ConsoleSender(client.sock, client.login)
thread_speaker = Thread(target=speaker.pull)
thread_speaker.daemon = True
thread_speaker.start()

while True:
    if not thread_listener.is_alive:
        break
    if not thread_speaker.is_alive:
        break

client.stop()
