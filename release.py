import sort
import zipfile
import os
import json

def zip_folder(folder_path, zip_path):
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                abs_path = os.path.join(root, file)
                rel_path = os.path.relpath(abs_path, folder_path)
                zipf.write(abs_path, arcname=rel_path)

sort.main()
with open('character.json', 'r', encoding='utf-8') as f:
    config = json.load(f)
games = config['game_list']
for game in games:
    zip_folder(f'release/{game}', f'release/{game}.zip')
print('Done!')
