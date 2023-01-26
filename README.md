# Faster rVAD

## Description
This repository provides a Python implementation that is much faster than the Python code provided in the original repository.

I also include code for saving and loading rVAD results, as well as a function to convert the rVAD results (which are masks for windows) to masks that can be applied to the wav-file (sample wise masking).

In order to get the masking, run `rVAD_fast.py`

Below are the speed comparison of this implementation vs the original implementation (not including time to read the wav file, or writing the results). It was tested on a 23 minute and 29 second wav file, at 16000Hz sampling rate, on an i7-6700HQ CPU @ 2.60GHz.

|Original|Improved|
|-|-|
|340s|6.0s|

Note that there are minor differences in results compared to the original python algorithm provided by the authors due to float inaccuracies. In the test file I used there were 140912 windows, and my implementation differed in 27 of them.

`speechproc_old.py` contains the original implementation, whereas `speechproc.py` contains my implementation. They can be interchanged by changing the imports in `rVAD_fast.py`

Additional todos include improving readability of code, making it more pythonic (much of the code uses indexing from 1), and adding docstring to high level functions.

---

Python libraries for an unsupervised method for robust voice activity detection (rVAD) or speech activity detection (SAD), as presented in [rVAD: An Unsupervised Segment-Based Robust Voice Activity Detection Method, Computer Speech & Language, 2020](https://www.sciencedirect.com/science/article/pii/S0885230819300920) or its [arXiv version](https://arxiv.org/abs/1906.03588). 

The rVAD method consists of two passes of denoising followed by a VAD stage. It has been applied as a preprocessor for a wide range of applications, such as speech recognition, speaker identification, language identification, age and gender identification, self-supervised learning, human-robot interaction, audio archive segmentation, and so on as in [Google Scholar](https://scholar.google.com/citations?view_op=view_citation&hl=en&user=fugL2E8AAAAJ&citation_for_view=fugL2E8AAAAJ:-mN3Mh-tlDkC).  

The method is unsupervised to make it applicable to a broad range of acoustic environments, and it is optimized considering both noisy and clean conditions. 

The rVAD (out of the box) ranks the 4th place (out of 27 supervised/unsupervised systems) in a Fearless Steps Speech Activity Detection Challenge. 

The rVAD paper is among [the most cited articles from Computer Speech and Language published since 2018](https://www.journals.elsevier.com/computer-speech-and-language/most-cited-articles) (the 6th place), in 2023.


## Reference VAD for Aurora 2 database:
The frame-by-frame reference VAD was generated from the clean set of Aurora 2 using forced-alignment speech recognition and has been used as a 'ground truth' for evaluating VAD algorithms. Our study shows that forced-alignment ASR performs as well as a human expert labeler for generating VAD references, as detailed in [Comparison of Forced-Alignment Speech Recognition and Humans for Generating Reference VAD](https://www.isca-speech.org/archive/interspeech_2015/papers/i15_2937.pdf). Here are the generated [reference VAD for the training set](Aurora2TrainSet-ReferenceVAD.zip) and the [reference VAD for the test set](Aurora2TestSet-ReferenceVAD.zip). 

