# KeshetCompress
WAV Compressor for Keshet-Orion games

Keshet-Orion games store their WAV file within custom \*.gnd files. 

Each GND file can contain multiple WAV files.

This Python module extracts the WAV files from the GND files, allowing them to be compressed to OGG format. 

A batch file later allows to reconstruct the GND files, in order to play the game.

This module depends on the [Ogg2Wav](https://github.com/OldGames/Ogg2Wav) module.
