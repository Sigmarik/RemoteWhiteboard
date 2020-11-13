import socket
import pygame
import threading
from math import *
import time

def net_update():
    global events
    #print(len(events))
    evs = str(events).encode()
    sock.send(str(len(str(len(evs)))).encode())
    sock.send(str(len(evs)).encode())
    sock.send(evs)
    report = sock.recv(1).decode()
    ln = int(sock.recv(1).decode())
    ln = int(sock.recv(ln).decode())
    part = sock.recv(ln).decode()
    try:
        part = eval(part)
        #print(part)
        for el in part:
            pygame.draw.line(*([scr] + el))
            pygame.draw.circle(scr, el[0], el[1], max(0, (el[3] - 1) // 2))
            pygame.draw.circle(scr, el[0], el[2], max(0, (el[3] - 1) // 2))
            #print([scr] + el)
        sock.send(b'o')
    except ZeroDivisionError:
        sock.send(b'e')
        print('ERROR')
    if report == 'o':
        events = []

def dist(A, B):
    return sqrt((A[0] - B[0]) * (A[0] - B[0]) + (A[1] - B[1]) * (A[1] - B[1]))

sock = socket.socket()
IP = input('Введите IP адрес сервера -> ')
if IP == '':
    IP = 'localhost'
port = input('Введите порт -> ')
if port == '':
    port = '9090'
sock.connect((IP, int(port)))
kg = True
scr = pygame.display.set_mode([600, 600])
scr.fill([255] * 3)
last_pos = None
width = 2
events = []
tm = time.monotonic()
while kg:
    mpos = list(pygame.mouse.get_pos())
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            kg = False
        if event.type == pygame.KEYDOWN:
            nm = pygame.key.name(event.key)
            try:
                width = int(nm)
            except ValueError:
                _=0
    if any(pygame.mouse.get_pressed()):
        if last_pos != None:
            if dist(last_pos, mpos) > 1:
                if pygame.mouse.get_pressed()[2]:
                    pygame.draw.line(scr, [255]*3, last_pos, mpos, 20)
                    pygame.draw.circle(scr, [255]*3, last_pos, 10)
                    pygame.draw.circle(scr, [255]*3, mpos, 10)
                    events.append([[255]*3, last_pos, mpos, 20])
                else:
                    pygame.draw.line(scr, [0, 0, 0], last_pos, mpos, width)
                    pygame.draw.circle(scr, [0] * 3, last_pos, max(0, (width - 1) // 2))
                    pygame.draw.circle(scr, [0]*3, mpos, max(0, (width - 1) // 2))
                    events.append([[0, 0, 0], last_pos, mpos, width])
                last_pos = mpos.copy()
        else:
            last_pos = mpos.copy()
    else:
        last_pos = None
    pygame.display.update()
    if time.monotonic() - tm > 1:
        net_update()
        tm = time.monotonic()
pygame.quit()
