#!/usr/bin/env python3

import os
import shutil
import sys

# Dictionary mapping image file signatures (magic numbers) to corresponding image file extensions
FILE_SIGNATURES = {
    b'\xff\xd8\xff': 'jpg',
    b'\x89\x50\x4e\x47\x0d\x0a\x1a\x0a': 'png',
    b'\x47\x49\x46\x38\x37\x61': 'gif',
    b'\x47\x49\x46\x38\x39\x61': 'gif',
    b'\x42\x4d': 'bmp',
}


def restore_files(folder_path):
    # Create a directory to store restored files
    restored_dir = os.path.join(folder_path, "Restored_Files")
    os.makedirs(restored_dir, exist_ok=True)
    
    
    try:
        # Iterate over files in the given folder
        for filename in os.listdir(folder_path):
            filepath = os.path.join(folder_path, filename)
            if os.path.isfile(filepath):
                with open(filepath, 'rb') as f:
                    # Read the first few bytes to identify the file signature
                    file_signature = f.read(8)
                    for signature, extension in FILE_SIGNATURES.items():
                        if file_signature.startswith(signature):
                            # Move the file to corresponding folder based on image type
                            image_folder = os.path.join(restored_dir, extension)
                            os.makedirs(image_folder, exist_ok=True)
                            new_filename = f"{filename}.{extension}"  # Adding the extension back to filename
                            shutil.copy(filepath, os.path.join(image_folder, new_filename))
                            print(f"Restored: {filename} -> {new_filename} ({extension.upper()})")
                            break
                    else:
                        print(f"Could not identify type for file: {filename}")
    except Exception as e:
        print(f"An error occurred: {e}")


def main():
    # Check if folder path is provided as an argument
    if len(sys.argv) != 2:
        print("Error! Missing argument: ./FileRestore.py <folder_path>")
        sys.exit(1)
    
    folder_path = sys.argv[1]
    
    # Check if the provided path is a directory
    if not os.path.isdir(folder_path):
        print("Error: Provided path is not a directory.")
        sys.exit(1)
        
    print(f"Restoring files in folder: {folder_path}")
    restore_files(folder_path)
    print("Restoration complete.")

if __name__ == "__main__":
    main()
    