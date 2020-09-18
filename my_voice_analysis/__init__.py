import os
from parselmouth.praat import run_file
import numpy as np
from scipy.stats import binom, ks_2samp, ttest_ind


class Analyser:
    """
    A class to perform voice analysis to audio file.
    Usage:
    from my_voice_analysis import Analyser
    a = Analyser('/path/to/praat-file.praat')
    total = a.total('/path/to/audio.wav')
    """

    GENDER_MALE = 'male'
    GENDER_FEMALE = 'female'

    MOOD_NO_EMOTION = 'no_emotion'
    MOOD_READING = 'reading'
    MOOD_PASSIONATE = 'passionate'

    def __init__(self, praat_file=None):
        if praat_file is not None:
            self.praat_file = praat_file
        else:
            self.praat_file = os.path.join(
                os.path.dirname(__file__), 'myspsolution.praat')
        self.objects = None

    def __get_objects(self):
        if self.objects is not None:
            return self.objects
        raise Exception('start() has not been called yet')

    def start(self, soundfile):
        soundfile_dir = os.path.dirname(soundfile) + '/'
        self.objects = run_file(self.praat_file, -20, 2, 0.3, "yes", soundfile,
                                soundfile_dir, 80, 400, 0.01, capture_output=True)
        return self

    def result(self):
        """
        Returns all stats
        """
        objects = self.__get_objects()
        z1 = str(objects[1]).strip().split()
        z2 = np.array(z1)
        z3 = np.array(z2)[np.newaxis]
        z4 = z3.T

        return {
            "num_syllables": int(z4[0, 0]),
            "num_pauses": int(z4[1, 0]),
            "speech_rate": int(z4[2, 0]),
            "articulation_rate": int(z4[3, 0]),
            "speaking_duration_no_pauses": float(z4[4, 0]),
            "speaking_duration_with_pauses": float(z4[5, 0]),
            "speaking_ratio": float(z4[6, 0]),
            "f0_mean": float(z4[7, 0]),
            "f0_std": float(z4[8, 0]),
            "f0_median": float(z4[9, 0]),
            "f0_min": float(z4[10, 0]),
            "f0_max": float(z4[11, 0]),
            "f0_quantile25": float(z4[12, 0]),
            "f0_quantile75": float(z4[13, 0])
        }

    def num_syllables(self):
        """
        Returns number of syllables
        """
        objects = self.__get_objects()
        z1 = str(objects[1]).strip().split()
        return int(z1[0])

    def num_pauses(self):
        """
        Returns number of pauses
        """
        objects = self.__get_objects()
        z1 = str(objects[1]).strip().split()
        return int(z1[1])

    def speech_rate(self):
        """
        Returns rate of speech (syllables / sec original duration)
        """
        objects = self.__get_objects()
        z1 = str(objects[1]).strip().split()
        return int(z1[2])

    def articulation_rate(self):
        """
        Returns articulation rate (syllables / sec speaking duration)
        """
        objects = self.__get_objects()
        z1 = str(objects[1]).strip().split()
        return int(z1[3])

    def speaking_duration_no_pauses(self):
        """
        Returns speaking duration in seconds (speaking duration without pauses)
        """
        objects = self.__get_objects()
        z1 = str(objects[1]).strip().split()
        return float(z1[4])

    def speaking_duration_with_pauses(self):
        """
        Returns speaking duration in seconds (speaking duration with pauses)
        """
        objects = self.__get_objects()
        z1 = str(objects[1]).strip().split()
        return float(z1[5])

    def speaking_ratio(self):
        """
        Return speaking ratio: (speaking duration) / (original duration)
        """
        objects = self.__get_objects()
        z1 = str(objects[1]).strip().split()
        return float(z1[6])

    def ppp_score_percentage(self):
        """
        Returns Pronunciation posteriori probability score percentage
        """
        objects = self.__get_objects()
        z1 = str(objects[1]).strip().split()
        z2 = float(z1[14])  # will be the floating point number 8.3
        db = binom.rvs(n=10, p=z2, size=10000)
        a = np.array(db)
        b = np.mean(a)*100/10
        return b

    def gender_mood(self):
        """
        Returns voice gender and speech mood
        """
        objects = self.__get_objects()
        z1 = str(objects[1])
        z2 = z1.strip().split()
        z3 = float(z2[8])
        z4 = float(z2[7])
        if z4 <= 114:
            g = 101
            j = 3.4
        elif z4 > 114 and z4 <= 135:
            g = 128
            j = 4.35
        elif z4 > 135 and z4 <= 163:
            g = 142
            j = 4.85
        elif z4 > 163 and z4 <= 197:
            g = 182
            j = 2.7
        elif z4 > 197 and z4 <= 226:
            g = 213
            j = 4.5
        elif z4 > 226:
            g = 239
            j = 5.3
        else:
            return (None, None, None)

        def teset(a, b, c, d):
            d1 = np.random.wald(a, 1, 1000)
            d2 = np.random.wald(b, 1, 1000)
            d3 = ks_2samp(d1, d2)
            c1 = np.random.normal(a, c, 1000)
            c2 = np.random.normal(b, d, 1000)
            c3 = ttest_ind(c1, c2)
            y = ([d3[0], d3[1], abs(c3[0]), c3[1]])
            return y

        nn = 0
        mm = teset(g, j, z4, z3)

        while (mm[3] > 0.05 and mm[0] > 0.04 or nn < 5):
            mm = teset(g, j, z4, z3)
            nn = nn+1
        nnn = nn

        if mm[3] <= 0.09:
            mmm = mm[3]
        else:
            mmm = 0.35
        if z4 > 97 and z4 <= 114:
            return (Analyser.GENDER_MALE, Analyser.MOOD_NO_EMOTION, mmm)
        elif z4 > 114 and z4 <= 135:
            return (Analyser.GENDER_MALE, Analyser.MOOD_READING, mmm)
        elif z4 > 135 and z4 <= 163:
            return (Analyser.GENDER_MALE, Analyser.MOOD_PASSIONATE, mmm)
        elif z4 > 163 and z4 <= 197:
            return (Analyser.GENDER_FEMALE, Analyser.MOOD_NO_EMOTION, mmm)
        elif z4 > 197 and z4 <= 226:
            return (Analyser.GENDER_FEMALE, Analyser.MOOD_READING, mmm)
        elif z4 > 226 and z4 <= 245:
            return (Analyser.GENDER_FEMALE, Analyser.MOOD_PASSIONATE, mmm)
        else:
            return (None, None, None)

    def f0_values(self):
        """
        Returns fundamental frequency distribution values (Hz)
        """
        objects = self.__get_objects()
        z1 = str(objects[1]).strip().split()
        return {
            'mean': float(z1[7]),
            'std': float(z1[8]),
            'med': float(z1[9]),
            'min': float(z1[10]),
            'max': float(z1[11]),
            'q25': float(z1[12]),
            'q75': float(z1[13])
        }
