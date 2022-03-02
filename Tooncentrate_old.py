from pysinewave import SineWave
from time import sleep, time
from random import randrange, choice
from tqdm import tqdm

class Tooncentrate(object):
    def __init__(self, base_scale=None, volume=1, interval=6, bpm=120, measures=1, notes_in_measure=16,
                 breathing_room=0.125):
        self.bpm = bpm
        self.interval = interval
        # Default to E Natural Minor if no scale provided... feels cleaner to do this here than have a big array
        # in the function declaration
        self.base_scale = base_scale if base_scale else [329.64, 370.0, 415.32, 440.0, 493.88, 554.36, 587.32, 659.24]
        self.volume = volume
        self.measures = measures
        self.notes_in_measure = notes_in_measure
        self.sine = SineWave(decibels_per_second=3900, pitch_per_second=500)
        self.sine.set_frequency(self.base_scale[0])
        self.sine.set_volume(self.volume)
        self.beat_length = self.calculate_beat_length()
        self.breathing_room_length = self.beat_length - breathing_room


    def calculate_beat_length(self):
        return (60 / self.bpm)

    def play(self):
        clock_start_time = time()
        self.sine.play()
        sleep(1)
        self.sine.sinewave_generator.set_amplitude(0.01)

        for note in self.notes():
            self.sine.sinewave_generator.set_amplitude(0.01)
            clock_note_start = clock_start_time + note['start']
            clock_note_stop = clock_start_time + note['stop']
            clock_beat_end = clock_start_time + note['total']
            if note['note']:
                self.sine.set_frequency(note['note'])

                while time() < clock_note_start:
                    sleep(.05)
                self.sine.sinewave_generator.set_amplitude(1)

                while time() < clock_note_stop:
                    sleep(.05)
                self.sine.sinewave_generator.set_amplitude(0.01)

            while time() < clock_beat_end:
                sleep(.05)

        sleep(self.beat_length * 4)
        self.sine.stop()


    def notes(self):
        output = []
          # E Natural Minor
        for note_count in range(self.measures * self.notes_in_measure):
            start_time = note_count * self.beat_length
            total_time = start_time + self.breathing_room_length
            output.append( {
                'start': start_time,
                'stop': total_time - self.breathing_room_length,
                'total': total_time,
                'note': self.randomnote()
            })
        return output

    def randomnote(self):
        shifter = randrange(0, 7)
        frequency = choice(self.base_scale)
        if shifter == 1:
            return frequency * randrange(2, 4)
        elif shifter == 2:
            return frequency // randrange(2, 4)
        elif shifter < 6:
            return frequency
        return None

    def start(self):
        self.play()
        while True:
            for _ in tqdm([_ for _ in range(0, self.interval * 60, self.bpm)]):
                sleep(1)
            self.play()
