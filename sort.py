import os
import json
import shutil

def main():
    # 创建文件夹
    if os.path.exists('release'):
        print('release文件夹已存在，是否删除？(y/n)')
        shutil.rmtree('release')
        if input().lower() == 'y':
            pass
        else:
            exit(0)

    os.makedirs('release')

    # 读取配置文件
    with open('character.json', 'r', encoding='utf-8') as f:
        config = json.load(f)

    games = config['game_list']

    # 读取表情包
    stickers = os.walk('HoYoLab表情包')
    stickers = list(stickers)
    # 循环游戏
    for game in games:
        folders = config[game].keys()
        for folder in folders:
            folder_path = os.path.join('release', game, folder)
            characters = config[game][folder]
            for character in characters:
                if not character:
                    continue
                character_path = os.path.join(folder_path, character)
                os.makedirs(character_path, exist_ok=True)
                # 查找表情包
                for sticker in stickers:
                    sticker_game = sticker[0].split('/')
                    if len(sticker_game) > 1:
                        if sticker_game[1] not in ('2022愚人节系列表情包',):
                            if sticker_game[1] != game:
                                continue
                    file_list = sticker[2]
                    for file in file_list:
                        if file is not None and character in file:
                            # 复制表情包
                            src = os.path.join(sticker[0], file)
                            dst = os.path.join(character_path, '_'.join([*(sticker[0].split('/')[2:]), file]))
                            shutil.copy(src, dst)
                            idx = sticker[2].index(file)
                            sticker[2][idx] = None
    for sticker in stickers:
        if '.DS_Store' in sticker[2]:
            sticker[2].remove('.DS_Store')
        while None in sticker[2]:
            sticker[2].remove(None)
        if sticker[2]:
            for file in sticker[2]:
                print(os.path.join(*(sticker[0].split('/')[1:]), file))


if __name__ == '__main__':
    main()
