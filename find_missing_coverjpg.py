import os
import sys
import shutil


def find_and_fix_folders(folder_path, audio_extensions=None, image_extensions=None):
    """
    Find subfolders containing audio files but missing 'cover.jpg', and handle them.

    Parameters:
    - folder_path (str): The path of the folder to scan.
    - audio_extensions (set): Set of audio file extensions to check.
    - image_extensions (set): Set of image file extensions to check.

    Returns:
    - List of folder paths that could not be fixed (multiple or no images).
    """
    if audio_extensions is None:
        audio_extensions = {'.flac', '.mp3', '.aac', '.wav', '.ogg', '.m4a'}

    if image_extensions is None:
        image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif'}

    unresolved_folders = []

    # Traverse the directory
    for root, dirs, files in os.walk(folder_path):
        # Create a lowercase list of file names
        files_lower = [file.lower() for file in files]
        has_audio = any(file.lower().endswith(tuple(audio_extensions))
                        for file in files)
        # Check specifically for lowercase 'cover.jpg'
        has_cover = 'cover.jpg' in [file for file in files]

        if has_audio and not has_cover:
            # Find image files
            image_files = [
                os.path.join(root, file)
                for file in files
                if file.lower().endswith(tuple(image_extensions))
            ]

            if len(image_files) == 1:
                # If exactly one image, copy it as 'cover.jpg'
                single_image = image_files[0]
                cover_path = os.path.join(root, 'cover.jpg')
                try:
                    shutil.copy(single_image, cover_path)
                    print(f"Created cover.jpg in: {
                          root} (from {single_image})")
                except Exception as e:
                    print(f"Error copying image {
                          single_image} to {cover_path}: {e}")
            else:
                # If no images or multiple images, save the folder for reporting
                unresolved_folders.append(root)

    return unresolved_folders


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python find_folders.py <folder_path>")
        sys.exit(1)

    folder_to_scan = sys.argv[1]

    if not os.path.isdir(folder_to_scan):
        print("Invalid folder path. Please check the path and try again.")
        sys.exit(1)

    unresolved = find_and_fix_folders(folder_to_scan)

    if unresolved:
        with open("output.txt", 'w') as f:
            for folder in unresolved:
                f.write(folder + '\n')
        print("\nFolders with multiple or no images (could not create cover.jpg):")
        for folder in unresolved:
            print(f"{folder}")
    else:
        print("All folders processed successfully!")
