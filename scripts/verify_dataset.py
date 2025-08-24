#!/usr/bin/python3


# Import necessary libraries
import pandas as pd
import os
import soundfile as sf

# --- Configuration ---
# Define the paths to our data files and folders.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
METADATA_PATH = os.path.join(BASE_DIR, "data", "metadata.csv")
AUDIO_FOLDER = os.path.join(BASE_DIR, "data", "audio")


# --- Helper Function 1: Load Metadata ---
def load_metadata(file_path):
    """
    Loads the dataset's metadata file.
    Returns a pandas DataFrame or None if it fails.
    """
    if not os.path.exists(file_path):
        print(f"❌ ERROR: Metadata file not found at: {file_path}")
        return None

    try:
        metadata = pd.read_csv(file_path, sep='|', header=None, names=['filename', 'transcription'])
        print(f"✅ Successfully loaded metadata for {len(metadata)} files.")
        return metadata
    except Exception as e:
        print(f"❌ ERROR: Could not read metadata file. Error: {e}")
        return None


# --- Helper Function 2: Validate a Single Entry ---
def validate_single_entry(row, audio_folder):
    """
    Validates one row from the metadata (one audio file).
    Returns a list of error messages found for this entry.
    """
    errors = []
    audio_filename = row['filename']
    audio_path = os.path.join(audio_folder, audio_filename)

    # Check 1: Audio file existence
    if not os.path.exists(audio_path):
        errors.append(f"MISSING FILE: '{audio_filename}' not found.")
        return errors # No need to check other things if file is missing

    # Check 2: Transcript validity
    transcription = row['transcription']
    if not isinstance(transcription, str) or not transcription.strip():
        errors.append(f"EMPTY TRANSCRIPT for '{audio_filename}'.")

    # Check 3: Audio file readability
    try:
        sf.info(audio_path)
    except Exception:
        errors.append(f"CORRUPT AUDIO: Could not read '{audio_filename}'.")

    return errors


# --- Main Function: Orchestrator ---
def run_verification():
    """
    Main function to run the complete verification process.
    """
    print("--- Starting Dataset Verification ---")
    metadata = load_metadata(METADATA_PATH)

    # Stop if metadata loading failed
    if metadata is None:
        return

    total_issues = 0
    # Loop through each entry and validate it
    for index, row in metadata.iterrows():
        errors = validate_single_entry(row, AUDIO_FOLDER)
        if errors:
            for error in errors:
                print(f"  - ❌ {error}")
            total_issues += len(errors)

    # --- Final Report ---
    print("\n--- Verification Complete ---")
    if total_issues == 0:
        print("✅ Success! No issues found in your dataset.")
    else:
        print(f"⚠️ Found {total_issues} issues. Please review and fix them.")


# This makes the script runnable from the command line
if __name__ == "__main__":
    run_verification()
