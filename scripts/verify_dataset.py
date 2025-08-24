#!/usr/bin/python3


import pandas as pd
import os
import soundfile as sf

# --- Configuration ---
# Define the paths to our data files and folders.
# Using os.path.join makes our script work on any operating system (Windows, Mac, Linux).
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # This gets the main project folder "kisii-asr/"
METADATA_PATH = os.path.join(BASE_DIR, "data", "metadata.csv")
AUDIO_FOLDER = os.path.join(BASE_DIR, "data", "audio")

# --- Main Verification Logic ---
def verify_dataset():
    """
    Reads the metadata, checks for file existence, audio integrity, and transcript validity.
    """
    print("--- Starting Dataset Verification ---")

    # 1. Check if the metadata file exists
    if not os.path.exists(METADATA_PATH):
        print(f"❌ ERROR: Metadata file not found at: {METADATA_PATH}")
        return

    # 2. Read the metadata using pandas
    try:
        # We specify the separator is '|' and there is no header row
        metadata = pd.read_csv(METADATA_PATH, sep='|', header=None, names=['filename', 'transcription'])
        print(f"✅ Successfully loaded metadata for {len(metadata)} files.")
    except Exception as e:
        print(f"❌ ERROR: Could not read metadata file. Error: {e}")
        return

    # Keep track of any issues we find
    issues_found = 0

    # 3. Loop through each row in our metadata
    for index, row in metadata.iterrows():
        audio_filename = row['filename']
        transcription = row['transcription']

        # Construct the full path to the audio file
        audio_path = os.path.join(AUDIO_FOLDER, audio_filename)

        # 3a. Check if the audio file exists
        if not os.path.exists(audio_path):
            print(f"  - ❌ MISSING FILE: The file '{audio_filename}' is listed in the CSV but not found in the audio folder.")
            issues_found += 1
            continue # Skip to the next row

        # 3b. Check if the transcription is valid (not empty or just whitespace)
        # We check if it's a string first to avoid errors
        if not isinstance(transcription, str) or not transcription.strip():
            print(f"  - ❌ EMPTY TRANSCRIPT: The audio file '{audio_filename}' has an empty transcript.")
            issues_found += 1

        # 3c. Check if the audio file is readable/uncorrupted
        try:
            # We use soundfile to try and open it and get info.
            # If this fails, the file is likely corrupted.
            sf.info(audio_path)
        except Exception as e:
            print(f"  - ❌ CORRUPT AUDIO: Could not read audio file '{audio_filename}'. Error: {e}")
            issues_found += 1

    # --- Final Report ---
    print("\n--- Verification Complete ---")
    if issues_found == 0:
        print("✅ Success! No issues found in your dataset.")
    else:
        print(f"⚠️ Found {issues_found} issues. Please review the messages above and fix them.")


# This part makes the script runnable from the command line
if __name__ == "__main__":
    verify_dataset()
