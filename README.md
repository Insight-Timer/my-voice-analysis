# My Voice Analysis

> IMPORTANT: This is a forked version of my-voice-analysis package, see [here the original version](https://github.com/Shahabks/my-voice-analysis). The goal is to provides cleaner and better api for developers. But all credits are belongs to the original author.

My-Voice Analysis is a Python library for the analysis of voice (simultaneous speech, high entropy) without the need of a transcription. It breaks utterances and detects syllable boundaries, fundamental frequency contours, and formants. Its built-in functions recognise and measures 

1.	gender recognition, 
2.	speech mood (semantic analysis), 
3.	pronunciation posterior score 
4.	articulation-rate, 
5.	speech rate,
6.	filler words, 
7.	f0 statistics, 

The library was developed based upon the idea introduced by Nivja DeJong and Ton Wempe [1], Paul Boersma and David Weenink [2], Carlo Gussenhoven [3], S.M Witt and S.J. Young [4] and Yannick Jadoul [5]. Peaks in intensity (dB) that are preceded and followed by dips in intensity are considered as potential syllable cores. 
My-Voice Analysis is unique in its aim to provide a complete quantitative and analytical way to study acoustic features of a speech. Moreover, those features could be analysed further by employing Python’s functionality to provide more fascinating insights into speech patterns. 

This library is for Linguists, scientists, developers, speech and language therapy clinics and researchers.   

Please note that My-Voice Analysis is currently in initial state though in active development. While the amount of functionality that is currently present is not huge, more will be added over the next few months.

## Installation

This package doesn't available through PyPi, please install it directly via git:

```
pip install --upgrade git+git://github.com/Insight-Timer/my-voice-analysis.git
```

## NOTE: 

Audio files must be in WAV format, recorded at 44kHz sample frame and 16 bits of resolution.  

## Example usage

```
>>> from my_voice_analysis import Analyser
>>> a = Analyser()
>>> a.start('/tmp/output.wav')
>>> a.result()
{'num_syllables': 1982, 'num_pauses': 244, 'speech_rate': 2, 'articulation_rate': 4, 'speaking_duration_no_pauses': 557.1, 'speaking_duration_with_pauses': 853.5, 'speaking_ratio': 0.7, 'f0_mean': 181.13, 'f0_std': 43.87, 'f0_median': 189.9, 'f0_min': 70.0, 'f0_max': 394.0, 'f0_quantile25': 172.0, 'f0_quantile75': 206.0}
```

**Gender recognition and mood of speech:**
```
>>> a.gender_mood()
('female', 'no_emotion', 4.450885724080103e-147)
```

**Pronunciation posteriori probability score percentage:**
```
>>> a.ppp_score_percentage()
70.185
```

**Detect and count number of syllables:**
```
>>> a.num_syllables()
1982
```

**Detect and count number of fillers and pauses:**
```
>>> a.num_pauses()
244
```

**Measure the rate of speech (speed):**
```
>>> a.speech_rate()
2
```

**Measure the articulation (speed):**
```
>>> a.articulation_rate()
4
```

**Measure speaking time (excluding fillers and pause):**
```
>>> a.speaking_duration_no_pauses()
557.1
```

**Measure total speaking duration (including fillers and pauses):**
```
>>> a.speaking_duration_with_pauses()
853.5
```

**Measure ratio between speaking duration and total speaking duration:**
```
>>> a.speaking_ratio()
0.7
```

**Measure fundamental frequency distribution**:
```
>>> a.f0_values()
{'mean': 181.13, 'std': 43.87, 'med': 189.9, 'min': 70.0, 'max': 394.0, 'q25': 172.0, 'q75': 206.0}
```

## Praat file
By default when you initialise the `Analyser` class, it using the original `myspsolution.praat` by default. If you want to provides your own `praat` file, pass the file path during initialisation.
```
a = Analyser('/path/to/file.praat')
```

## Development

My-Voice-Analysis was developed by Sab-AI Lab in Japan (previously called Mysolution). It is part of a project to develop Acoustic Models for linguistics in Sab-AI Lab. That is planned to enrich the functionality of My-Voice Analysis by adding more advanced functions as well as adding a language models. Please see Myprosody https://github.com/Shahabks/myprosody and Speech-Rater https://shahabks.github.io/Speech-Rater/)

## References and Acknowledgements

1.	DeJong N.H, and Ton Wempe [2009]; “Praat script to detect syllable nuclei and measure speech rate automatically”; Behavior Research Methods, 41(2).385-390.
2.	 Paul Boersma and David Weenink;  http://www.fon.hum.uva.nl/praat/
3.	Gussenhoven C. [2002]; “ Intonation and Interpretation: Phonetics and Phonology”; Centre for Language Studies, Univerity of Nijmegen, The Netherlands.  
4.	Witt S.M and Young S.J [2000]; “Phone-level pronunciation scoring and assessment or interactive language learning”; Speech Communication, 30 (2000) 95-108.
5.	Jadoul, Y., Thompson, B., & de Boer, B. (2018). Introducing Parselmouth: A Python interface to Praat. Journal of Phonetics,
   71, 1-15. https://doi.org/10.1016/j.wocn.2018.07.001 (https://parselmouth.readthedocs.io/en/latest/)
6. Projects https://parselmouth.readthedocs.io/en/docs/examples.html

 ## MIT License
 
 ```
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```


