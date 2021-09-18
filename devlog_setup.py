import os
import time
import pymiere
from pymiere.core import check_premiere_is_alive
from pymiere.wrappers import move_clip, time_from_seconds

def create_folder_structure():
    current_dir = os.getcwd()
    folders_to_create = (
        r"Project Files",
        r"Dialogue Audio",
        r"Graphics",
        r"OBS Output",
        r"IRL Footage"
    )

    anim_delay = 0.075

    # create folder directories
    for folder in folders_to_create:
        final_directory = os.path.join(current_dir, folder)

        if not os.path.exists(final_directory):
            os.makedirs(final_directory)
            time.sleep(anim_delay)


def setup_premiere_project():
    # set up premiere project
    current_dir = os.getcwd()
    if check_premiere_is_alive(crash=False) == False:
        while check_premiere_is_alive(crash=False) == False:
            time.sleep(1)
        time.sleep(5)

    project = pymiere.objects.app.project

    print("creating project file....")
    project_name = current_dir.split("\\")[-1] + r"-01.prproj"
    project_path = os.path.join(current_dir, r"Project Files", project_name)
    if os.path.exists(project_path) is False:
        pymiere.objects.app.newProject(project_path)

    pymiere.objects.app.openDocument(project_path)

    # Create bins
    print("creating bins....")
    bins = (
    "[01] Reusable Sequences",
    "[02] Dialogues",
    "[03] Music",
    "[04] Sound Effects",
    "[05] IRL Footage",
    "[06] Drawables Footage",
    "[07] Coding Footage",
    "[08] OBS Footage",
    "[09] Subsequences",
    "[10] Color Mattes",
    )

    for bin in bins:
        project.rootItem.createBin(bin)
        time.sleep(0.2)

    # Create main sequence
    print("creating main sequence....")
    sequence_name = "MAIN"
    sequence_preset_path = r"M:\Scripting Resources\MaddHatt Youtube.sqpreset"
    project.newSequence(sequenceName=sequence_name, pathToSequencePreset=sequence_preset_path).sequenceID # project.newSequence() was not in pymiere by default, added it manually


def import_audio():
    audio_dir = os.getcwd() + "\\Dialogue Audio\\"
    audio_files = []
    for root, dir, files in os.walk(audio_dir):
        audio_files.extend(files)

    for i in range(0, len(audio_files)):
        audio_files[i] = os.path.join(audio_dir,audio_files[i])
        
    project = pymiere.objects.app.project
    print("importing dialogue....")

    for item in project.rootItem.children:
        if item.name == "[02] Dialogues":
            dialogue_bin = item

    success = project.importFiles(
        audio_files,
        suppressUI=True,
        targetBin=dialogue_bin,
        importAsNumberedStills=False
    )

    print("inserting dialogue to timeline....")
    for item in reversed(dialogue_bin.children):
        project.activeSequence.audioTracks[-1].insertClip(item, time_from_seconds(0))
    
    offset = 4.0
    print("offsetting dialogue by 4 seconds....")
    audio_clips = project.activeSequence.audioTracks[-1].clips
    for i in range(len(audio_clips) - 1, 0, -1):
        clip = audio_clips[i]
        clip.end = time_from_seconds(clip.end.seconds + offset * i)
        clip.start = time_from_seconds(clip.start.seconds + offset * i)

def import_intro():
    introPath = r'M:\Production Repository\Reusable Sequences\Intro Title Sequence.prproj'

    project = pymiere.objects.app.project
    for item in project.rootItem.children:
        if item.name == "[01] Reusable Sequences":
            sequence_bin = item

    print("importing intro sequence....")
    print("this takes a while....")
    time.sleep(0.2)
    project.importSequences2(introPath, ["1017fd4a-ec3e-4934-8f25-977a5ca93bb8"])

    for item in project.rootItem.children:
        if item.name == "Intro":
            item.moveBin(sequence_bin)
        elif item.name == "Intro Sequence":
            item.moveBin(sequence_bin)
            project.activeSequence.videoTracks[0].insertClip(item, time_from_seconds(0)) # Adds the audio anyways

os.system("cls")
setup_premiere_project()
import_audio()
import_intro()
pymiere.objects.app.project.save()