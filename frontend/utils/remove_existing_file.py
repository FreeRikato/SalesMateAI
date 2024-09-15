import os


def remove_existing_file(save_path, file_name):
    """Remove an existing file with the same base name, even with a different extension."""
    base_name, _ = os.path.splitext(file_name)
    for ext in [".pdf", ".txt"]:
        existing_file = os.path.join(save_path, base_name + ext)
        if os.path.exists(existing_file):
            os.remove(existing_file)
