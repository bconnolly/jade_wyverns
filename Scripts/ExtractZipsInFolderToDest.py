import zipfile
import os

folder_name = "D:\\Documents\\FE3H Homebrew\\vanilla_out_zips\\zipped_zips"
destination_dir = "D:\\Documents\\vm-shared-folders\\homebrew\\vanilla_out"

for zipped_file in os.listdir(folder_name):

    file_name = os.path.join(folder_name, zipped_file)

    try:
        with zipfile.ZipFile(file_name, 'r') as zip_ref:
            zip_ref.extractall(destination_dir)
        print(f"Successfully unzipped '{zipped_file}' to '{destination_dir}'")
    except zipfile.BadZipFile:
        print(f"Error: '{zipped_file}' is not a valid ZIP file.")
    except FileNotFoundError:
        print(f"Error: ZIP file '{zipped_file}' not found.")
    