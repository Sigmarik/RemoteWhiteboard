import socket
import pygame
import threading

events = []
test_surf = pygame.Surface([1, 1])
log = open('log.txt', 'w')

def client_work(conn):
    global events
    index = 0
    while True:
        try:
            try:
                ln = int(conn.recv(1).decode())
                ln = int(conn.recv(ln).decode())
            except:
                ln = 1024
            inp = conn.recv(ln).decode()
            try:
                val = eval(inp)
                for el in val:
                    pygame.draw.line(*([test_surf] + el))
                events = events + val
                conn.send(b'o')
            except:
                conn.send(b'e')
            #print('sended')
            com_arr = events[index:]
            evs = str(com_arr).encode()
            conn.send(str(len(str(len(evs)))).encode())
            conn.send(str(len(evs)).encode())
            conn.send(evs)
            report = conn.recv(1).decode()
            if report == 'o':
                index += len(com_arr)
        except Exception as E:
            print('ERROR', E, file=log)

sock = socket.socket()
IP = input('Введите IP, на котором хотите запустить сервер -> ')
if IP == '':
    IP = 'localhost'
port = input('Введите порт -> ')
if port == '':
    port = '9090'
sock.bind(('', int(port)))
print('Server created!')
print('Создан сервер на', IP + ':' + port, file=log)
while True:
    sock.listen(1)
    conn, addr = sock.accept()
    print('connected ->', addr, file=log)
    th = threading.Thread(target=client_work, args=[conn])
    th.start()
