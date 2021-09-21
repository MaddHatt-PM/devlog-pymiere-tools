import pymiere
import os
from pymiere.wrappers import time_from_seconds

target_folder = input ("Enter in filepath to song stem folder: ")
song_name = target_folder.split("\\")[-1]

song_files = []
for root, dir, files in os.walk(target_folder):
    song_files.extend(files)

for i in range(0, len(song_files)):
    song_files[i] = target_folder + "\\" + song_files[i]

project = pymiere.objects.app.project

for item in project.rootItem.children:
    if item.name == "[03] Music":
        new_song_bin = item.createBin(song_name)

project.importFiles(
    song_files,
    suppressUI=True,
    targetBin=new_song_bin,
    importAsNumberedStills=False
)

imported_stems = new_song_bin.children

sequence_name = "seq - " + song_name
sequence_preset_path = r"M:\Scripting Resources\Mixed Song.sqpreset"
project.newSequence(sequenceName=sequence_name, pathToSequencePreset=sequence_preset_path)

for i in range(0, len(imported_stems)):
    project.activeSequence.audioTracks[i].insertClip(imported_stems[i], time_from_seconds(0))