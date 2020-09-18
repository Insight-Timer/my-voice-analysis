import os
from parselmouth.praat import run_file
import numpy as np
from scipy.stats import binom, ks_2samp, ttest_ind


class MyVoiceAnalysis:
    """
    A class to perform voice analysis to audio file.
    Usage:
    mva = __import__('my-voice-analysis')
    m = mva.MyVoiceAnalysis('/path/to/praat-file.praat')
    total = m.total('/path/to/audio.wav')
    """

    def __init__(self, praat_file):
        self.praat_file = praat_file
        self.objects = None

    def __get_objects(self, soundfile):
        if self.objects is not None:
            return self.objects

        soundfile_dir = os.path.dirname(soundfile) + '/'
        self.objects = run_file(self.praat_file, -20, 2, 0.3, "yes", soundfile,
                                soundfile_dir, 80, 400, 0.01, capture_output=True)
        return self.objects

    def total(self, soundfile):
        """
        Returns all stats
        """
        objects = self.__get_objects(soundfile)
        z1 = str(objects[1])
        z2 = z1.strip().split()
        z3 = np.array(z2)
        z4 = np.array(z3)[np.newaxis]
        z5 = z4.T

        return {
            "num_syllables": int(z5[0, 0]),
            "num_pauses": int(z5[1, 0]),
            "speech_rate": int(z5[2, 0]),
            "articulation_rate": int(z5[3, 0]),
            "speaking_duration_no_pauses": float(z5[4, 0]),
            "speaking_duration_with_pauses": float(z5[5, 0]),
            "speaking_ratio": float(z5[6, 0]),
            "f0_mean": float(z5[7, 0]),
            "f0_std": float(z5[8, 0]),
            "f0_median": float(z5[9, 0]),
            "f0_min": float(z5[10, 0]),
            "f0_max": float(z5[11, 0]),
            "f0_quantile25": float(z5[12, 0]),
            "f0_quan75": float(z5[13, 0])
        }

    def num_syllables(self, soundfile):
        """
        Returns number of syllables
        """
        objects = self.__get_objects(soundfile)
        z1 = str(objects[1])
        z2 = z1.strip().split()
        return int(z2[0])

    def num_pauses(self, soundfile):
        """
        Returns number of pauses
        """
        objects = self.__get_objects(soundfile)
        z1 = str(objects[1])
        z2 = z1.strip().split()
        return int(z2[1])

    def speech_rate(self, soundfile):
        """
        Returns rate of speech (syllables / sec original duration)
        """
        objects = self.__get_objects(soundfile)
        z1 = str(objects[1])
        z2 = z1.strip().split()
        return int(z2[2])

    def articulation_rate(self, soundfile):
        """
        Returns articulation rate (syllables / sec speaking duration)
        """
        objects = self.__get_objects(soundfile)
        z1 = str(objects[1])
        z2 = z1.strip().split()
        return int(z2[3])

    def speaking_duration_no_pauses(self, soundfile):
        """
        Returns speaking duration in seconds (speaking duration without pauses)
        """
        objects = self.__get_objects(soundfile)
        z1 = str(objects[1])
        z2 = z1.strip().split()
        return float(z2[4])

    def speaking_duration_with_pauses(self, soundfile):
        """
        Returns speaking duration in seconds (speaking duration with pauses)
        """
        objects = self.__get_objects(soundfile)
        z1 = str(objects[1])
        z2 = z1.strip().split()
        return float(z2[5])

    def speaking_ratio(self, soundfile):
        """
        Return speaking ratio: (speaking duration) / (original duration)
        """
        objects = self.__get_objects(soundfile)
        z1 = str(objects[1])
        z2 = z1.strip().split()
        return float(z2[6])

    def ppp_score_percentage(self, soundfile):
        """
        Returns Pronunciation posteriori probability score percentage
        """
        objects = self.__get_objects(soundfile)
        z1 = str(objects[1])
        z2 = z1.strip().split()
        z4 = float(z2[14])  # will be the floating point number 8.3
        db = binom.rvs(n=10, p=z4, size=10000)
        a = np.array(db)
        b = np.mean(a)*100/10
        return b


def myspgend(m, p):
    sound = p+"/"+m+".wav"
    sourcerun = p+"/myspsolution.praat"
    path = p+"/"
    try:
        objects = run_file(sourcerun, -20, 2, 0.3, "yes",
                           sound, path, 80, 400, 0.01, capture_output=True)
        # This will print the info from the sound object, and objects[0] is a parselmouth.Sound object
        print(objects[0])
        # This will print the info from the textgrid object, and objects[1] is a parselmouth.Data object with a TextGrid inside
        z1 = str(objects[1])
        z2 = z1.strip().split()
        z3 = float(z2[8])  # will be the integer number 10
        z4 = float(z2[7])  # will be the floating point number 8.3
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
            print("Voice not recognized")
            exit()

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
            print(
                "a Male, mood of speech: Showing no emotion, normal, p-value/sample size= :%.2f" % (mmm), (nnn))
        elif z4 > 114 and z4 <= 135:
            print(
                "a Male, mood of speech: Reading, p-value/sample size= :%.2f" % (mmm), (nnn))
        elif z4 > 135 and z4 <= 163:
            print(
                "a Male, mood of speech: speaking passionately, p-value/sample size= :%.2f" % (mmm), (nnn))
        elif z4 > 163 and z4 <= 197:
            print("a female, mood of speech: Showing no emotion, normal, p-value/sample size= :%.2f" % (mmm), (nnn))
        elif z4 > 197 and z4 <= 226:
            print(
                "a female, mood of speech: Reading, p-value/sample size= :%.2f" % (mmm), (nnn))
        elif z4 > 226 and z4 <= 245:
            print(
                "a female, mood of speech: speaking passionately, p-value/sample size= :%.2f" % (mmm), (nnn))
        else:
            print("Voice not recognized")
    except:
        print("Try again the sound of the audio was not clear")


def myspf0mean(m, p):
    sound = p+"/"+m+".wav"
    sourcerun = p+"/myspsolution.praat"
    path = p+"/"
    try:
        objects = run_file(sourcerun, -20, 2, 0.3, "yes",
                           sound, path, 80, 400, 0.01, capture_output=True)
        # This will print the info from the sound object, and objects[0] is a parselmouth.Sound object
        print(objects[0])
        # This will print the info from the textgrid object, and objects[1] is a parselmouth.Data object with a TextGrid inside
        z1 = str(objects[1])
        z2 = z1.strip().split()
        z3 = int(z2[3])  # will be the integer number 10
        z4 = float(z2[7])  # will be the floating point number 8.3
        print("f0_mean=", z4, "# Hz global mean of fundamental frequency distribution")
    except:
        z4 = 0
        print("Try again the sound of the audio was not clear")
    return


def myspf0sd(m, p):
    sound = p+"/"+m+".wav"
    sourcerun = p+"/myspsolution.praat"
    path = p+"/"
    try:
        objects = run_file(sourcerun, -20, 2, 0.3, "yes",
                           sound, path, 80, 400, 0.01, capture_output=True)
        # This will print the info from the sound object, and objects[0] is a parselmouth.Sound object
        print(objects[0])
        # This will print the info from the textgrid object, and objects[1] is a parselmouth.Data object with a TextGrid inside
        z1 = str(objects[1])
        z2 = z1.strip().split()
        z3 = int(z2[3])  # will be the integer number 10
        z4 = float(z2[8])  # will be the floating point number 8.3
        print("f0_SD=", z4,
              "# Hz global standard deviation of fundamental frequency distribution")
    except:
        z4 = 0
        print("Try again the sound of the audio was not clear")
    return


def myspf0med(m, p):
    sound = p+"/"+m+".wav"
    sourcerun = p+"/myspsolution.praat"
    path = p+"/"
    try:
        objects = run_file(sourcerun, -20, 2, 0.3, "yes",
                           sound, path, 80, 400, 0.01, capture_output=True)
        # This will print the info from the sound object, and objects[0] is a parselmouth.Sound object
        print(objects[0])
        # This will print the info from the textgrid object, and objects[1] is a parselmouth.Data object with a TextGrid inside
        z1 = str(objects[1])
        z2 = z1.strip().split()
        z3 = int(z2[3])  # will be the integer number 10
        z4 = float(z2[9])  # will be the floating point number 8.3
        print("f0_MD=", z4, "# Hz global median of fundamental frequency distribution")
    except:
        z4 = 0
        print("Try again the sound of the audio was not clear")
    return


def myspf0min(m, p):
    sound = p+"/"+m+".wav"
    sourcerun = p+"/myspsolution.praat"
    path = p+"/"
    try:
        objects = run_file(sourcerun, -20, 2, 0.3, "yes",
                           sound, path, 80, 400, 0.01, capture_output=True)
        # This will print the info from the sound object, and objects[0] is a parselmouth.Sound object
        print(objects[0])
        # This will print the info from the textgrid object, and objects[1] is a parselmouth.Data object with a TextGrid inside
        z1 = str(objects[1])
        z2 = z1.strip().split()
        z3 = int(z2[10])  # will be the integer number 10
        z4 = float(z2[10])  # will be the floating point number 8.3
        print("f0_min=", z3, "# Hz global minimum of fundamental frequency distribution")
    except:
        z3 = 0
        print("Try again the sound of the audio was not clear")
    return


def myspf0max(m, p):
    sound = p+"/"+m+".wav"
    sourcerun = p+"/myspsolution.praat"
    path = p+"/"
    try:
        objects = run_file(sourcerun, -20, 2, 0.3, "yes",
                           sound, path, 80, 400, 0.01, capture_output=True)
        # This will print the info from the sound object, and objects[0] is a parselmouth.Sound object
        print(objects[0])
        # This will print the info from the textgrid object, and objects[1] is a parselmouth.Data object with a TextGrid inside
        z1 = str(objects[1])
        z2 = z1.strip().split()
        z3 = int(z2[11])  # will be the integer number 10
        z4 = float(z2[11])  # will be the floating point number 8.3
        print("f0_max=", z3, "# Hz global maximum of fundamental frequency distribution")
    except:
        z3 = 0
        print("Try again the sound of the audio was not clear")
    return


def myspf0q25(m, p):
    sound = p+"/"+m+".wav"
    sourcerun = p+"/myspsolution.praat"
    path = p+"/"
    try:
        objects = run_file(sourcerun, -20, 2, 0.3, "yes",
                           sound, path, 80, 400, 0.01, capture_output=True)
        # This will print the info from the sound object, and objects[0] is a parselmouth.Sound object
        print(objects[0])
        # This will print the info from the textgrid object, and objects[1] is a parselmouth.Data object with a TextGrid inside
        z1 = str(objects[1])
        z2 = z1.strip().split()
        z3 = int(z2[12])  # will be the integer number 10
        z4 = float(z2[11])  # will be the floating point number 8.3
        print("f0_quan25=", z3,
              "# Hz global 25th quantile of fundamental frequency distribution")
    except:
        z3 = 0
        print("Try again the sound of the audio was not clear")
    return


def myspf0q75(m, p):
    sound = p+"/"+m+".wav"
    sourcerun = p+"/myspsolution.praat"
    path = p+"/"
    try:
        objects = run_file(sourcerun, -20, 2, 0.3, "yes",
                           sound, path, 80, 400, 0.01, capture_output=True)
        # This will print the info from the sound object, and objects[0] is a parselmouth.Sound object
        print(objects[0])
        # This will print the info from the textgrid object, and objects[1] is a parselmouth.Data object with a TextGrid inside
        z1 = str(objects[1])
        z2 = z1.strip().split()
        z3 = int(z2[13])  # will be the integer number 10
        z4 = float(z2[11])  # will be the floating point number 8.3
        print("f0_quan75=", z3,
              "# Hz global 75th quantile of fundamental frequency distribution")
    except:
        z3 = 0
        print("Try again the sound of the audio was not clear")
    return
