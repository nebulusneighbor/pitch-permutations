# Pitch Permutations
Mathematical tool to understand the limits of Western musical scale construction in 12 tones

code_12pos folder contains python code that can be run to generate permutations and images.

Generated images can be found in scales in 12 positions media folder. 

This table demonstrates the number of unique rotations. Patterns that don't self describe are unique rotations. Modes for example are inherently self-described because they are the same pattern just shifted or rotated. e.g. the dorian mode and ionian mode are not unique, but the major scale and the harmonic minor scale are unique rotations. This table defines the total number of unique rotations for 0-12 note scales in 12 possible positions. 
![table_12pos_unique_permutations_fixed1](https://github.com/nebulusneighbor/pitch-permutations/assets/15897123/08121f76-442d-4d13-a5ed-f485b0007134)

Running scale_check_7.py will print all unique rotations of 7 notes (includes major scale, harmonic minor, etc.). A non-exhaustive list of 7-note scales are searched for, ones that are found are printed to console and also shown as a labeled image (may need to zoom!)
