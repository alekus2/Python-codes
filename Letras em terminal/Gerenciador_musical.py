import time
import sys
import pygame
import os
offset_ms = 0
coontador = 0
def type_print(text, delay=0.03):
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write("\n")
    sys.stdout.flush()

entries = []
with open('A man without love.txt', 'r', encoding='utf-8') as arquivo:
    for linha in arquivo:
        if not linha.strip():
            continue
        tempo = linha[:11].strip()
        tempo = tempo.replace("[", "").replace("]", "")
        inicio, fim = tempo.split("-")

        def to_seconds(t):
            parts = t.split(":")
            mins = int(parts[0])
            secs = float(parts[1].replace(",", "."))
            return mins * 60.0 + secs

        start_s = to_seconds(inicio)
        end_s = to_seconds(fim)

        start_ms = int(start_s * 1000)
        end_ms = int(end_s * 1000)

        text = linha[11:].strip()
        os.system('cls')
        entries.append({'start_ms': start_ms, 'end_ms': end_ms, 'text': text})

entries.sort(key=lambda e: e['start_ms'])
pygame.mixer.init()
pygame.mixer.music.load('A Man Without Love_spotdown.org.mp3')
pygame.mixer.music.play()

t0 = time.monotonic()
clock = pygame.time.Clock()

for entry in entries:
    target = entry['start_ms'] + offset_ms
    while True:
        pos = pygame.mixer.music.get_pos() 
        if pos < 0:
            pos = int((time.monotonic() - t0) * 1000)
        if pos >= target:
            type_print(entry['text'])
            break
        remaining_ms = target - pos
        sleep_s = min(0.1, max(0.01, remaining_ms / 1000.0 / 2.0))
        time.sleep(sleep_s)
        clock.tick(60)  
while pygame.mixer.music.get_busy():
    time.sleep(0.2)