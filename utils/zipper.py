import os
import zipfile

def zip_folder(folder_path, zip_name):
    # folder_path is the absolute path to the folder to zip
    # zip_name is the name of the zip file to create (e.g., "python.zip")
    # We'll place the zip file in the parent directory of folder_path (i.e., ./files/)
    parent_dir = os.path.dirname(folder_path)
    zip_path = os.path.join(parent_dir, f"{zip_name}.zip")

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.endswith(".zip") or file == ".DS_Store":
                    continue
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, parent_dir))
    
    print(f"Zipped {folder_path} to {zip_path}")

def update_all_zips(base_path):
    if not os.path.exists(base_path):
        return
    for entry in os.listdir(base_path):
        full_path = os.path.join(base_path, entry)
        if os.path.isdir(full_path):
            zip_folder(full_path, entry)
