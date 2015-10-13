import os

res_dir = '/Users/mukundvis/HealthifyMe/phoenix/HealthifyMe/res/'
main_folder = 'drawable-xxhdpi'
other_folders = ['drawable-hdpi', 'drawable-mdpi', 'drawable-xhdpi']
files_in_main_folder = os.listdir(res_dir + main_folder)

FILE_EXTENSIONS_TO_REMOVE = ['.png']

for folder in other_folders:
    print ''
    print '*' * 20
    print folder
    print '*' * 20
    # If a file that is available in xxhdpi is found
    # and the image is png, remove the file
    current_dir = res_dir + folder
    files = os.listdir(current_dir)
    redundant_files_count = 0
    for file_name in files:
        filename, file_extension = os.path.splitext(file_name)
        if file_extension not in FILE_EXTENSIONS_TO_REMOVE:
            continue
        if not file_name in files_in_main_folder:
            continue
        print 'deleting', file_name
        full_file_path = current_dir + '/' + file_name
        os.remove(full_file_path)
        redundant_files_count += 1
    print ''
    print 'Redundant files:', redundant_files_count
