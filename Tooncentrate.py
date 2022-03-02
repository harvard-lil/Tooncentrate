from time import sleep, time
from random import randrange, choice
from collections import deque
from tqdm import tqdm
import numpy
import pygame

VOL_WHISPER = 1024
VOL_QUIET = 2048
VOL_MODERATE = 3072
VOL_MAX = 4096

class Tooncentrate(object):
    def __init__(self, base_scale=None, volume=VOL_QUIET, interval=6, bpm=100, beats=2, notes_in_beat=4,
                 breathing_room_percent=20, sustain=3.25, soften_attack=3, bookend=True):
        self.bpm = bpm
        self.interval = interval
        # Default to E Natural Minor if no scale provided... feels cleaner to do this here than have a big array
        # in the function declaration
        self.base_scale = base_scale if base_scale else [329.64, 370.0, 415.32, 440.0, 493.88, 554.36, 587.32, 659.24]
        self.volume = volume
        self.beats = beats
        self.notes_in_beat = notes_in_beat
        self.sample_rate = 44100
        self.note_length = self.calculate_note_clock_length()
        self.note_sample_count = int(self.note_length * self.sample_rate)
        self.breathing_room_length = self.note_length * (breathing_room_percent * 0.01)
        self.sustain_length = self.note_length * sustain
        self.attack_length = soften_attack
        self.bookend = bookend
        pygame.mixer.init(self.sample_rate, -16, 1, 512)

    def calculate_note_clock_length(self):
        return (60 / self.bpm) / self.notes_in_beat

    def play(self):
        if self.bookend:
            notes = deque([self.getnote() for _ in range((self.beats * self.notes_in_beat) - 2)])
            notes.appendleft(self.getnote(first=True))
            notes.append(self.getnote(last=True))
        else:
            notes = deque([self.getnote() for _ in range(self.beats * self.notes_in_beat)])

        for count, note in enumerate(notes):
            started = time()
            if note is not None:
                sound = pygame.sndarray.make_sound(note)
                #sound.play(maxtime=int(self.note_length - self.breathing_room_length))
                sound.play(loops=0)
                sleep(self.note_length + self.breathing_room_length)
            else:
                sleep(self.note_length)

    def notes(self):
        return

    def getnote(self, first=False, last=False):
        if not first and not last:
            frequency = choice(self.base_scale)
            wildcard = randrange(0, 7)
            if wildcard == 0:
                return None
            if wildcard == 1:
                frequency *= randrange(2, 4)
            elif wildcard == 2:
                frequency //= randrange(2, 4)
        elif first:
            frequency = self.base_scale[-1]
        else:
            frequency = self.base_scale[0]
        return self.gen_tone(frequency)

    def start(self):
        self.play()
        while True:
            for _ in tqdm([_ for _ in range(0, self.interval * 60, self.bpm)]):
                sleep(1)
            self.play()


    def gen_tone(self, hz):
        # adapted from https://shallowsky.com/blog/programming/python-play-chords.html
        """Compute N samples of a sine wave with given frequency and peak amplitude.
           Defaults to one second.
        """
        length = self.sample_rate / float(hz)
        omega = numpy.pi * 2 / length
        xvalues = numpy.arange(int(length)) * omega
        onecycle = self.volume * numpy.sin(xvalues)
        return numpy.resize(onecycle, (self.note_sample_count,)).astype(numpy.int16)