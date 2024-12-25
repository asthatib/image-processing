# image-processing questions
1. controlling tilt:
During aerial maneuvers, UAV or drones have to position themselves by controlling tilt and
height. Experimental robotics use ArUco markers (you can consider them as QR codes) which
are placed on the grounds for adjusting their position. However, fixed size visual patterns can be
used in remote terrain for drone positioning. Indian flag serves as a good localizer by military
drones. At the current non-optimal position, drone sees the image as shown in ‘input’, then it
adjusts its position (tilt and height) continuously with minimum movement till it sees the final
‘reference’ image. Note there is no need of rotation along Z-(height)-axis (yaw). Your task is to
generate the ‘reference’ image for the input seen by drone.
Your function should take input as an image array and it should return the output as an
image array. Here input size may vary but each reference image is having a size 600x600 pixels,
radius of circle = 100, center of circle is (300,300), circle width = 2 and spoke width = 1 pixel.

2. sound identifier
There are four qualities of bricks used in the construction, having different costs according
to their quality. So they do, via making different sounds when struck together.
We will consider only 2 quality bricks here - low and high. Properly cooked red soil
bricks are of high quality. The furnace melts ferrites and imparts a metal-like quality to these
bricks. Therefore, when high-quality bricks are struck together, they produce a sound resembling
that of metal, while low-quality bricks sound like cardboard banged together.
You will be provided with audio (.mp3 files) of these brick sounds. You can analyze it in the
image domain via audio-to-spectrogram conversion using windowed Fourier transforms. You
may use various python libraries for getting spectrogram, like the below pseudo-code:
: import librosa
: y, sr = librosa.load(audio_path, sr=None) %sr=None preserves sampling rate
: n_fft = 2048 %FFT points, adjust as you need
: hop_length = 512 %Sliding amount for windowed FFT (adjust as needed)
: spec = librosa.feature.melspectrogram(y, sr, n_fft, hop_length, fmax=22000)
: # spec_db = perform power to decibel (db) image transformation of `spec'
: # decibel conversion → 10 log(
P
max(P)
), where P is the spectral power
: # inspect spec_db images via displaying them before designing your algorithm
Write the python program, which can process the brick sounds and outputs their quality in
terms of metal (high) or cardboard (low) quality.

3. optimal character recognition
To digitize written knowledge, we need to scan the images and then
use optical character recognition (OCR), an image processing algorithm to digitize it. However, the scanned images are often
not horizontally aligned, which causes OCR to fail or
produce erroneous digitization. These scanned images need to be re-rotated so that the final text
appears perfectly aligned horizontally in a readable form.
Design a python program to realign scanned text always in a horizontal viewing manner. Your program will be tested
on various different input images where in the output any text character should not be cut and
image should be horizontally aligned.
