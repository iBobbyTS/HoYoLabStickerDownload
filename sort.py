import os
import json
import shutil

def matches_character(filename, character, known_characters):
    """优先匹配完整角色字段，避免基础角色吞掉同名衍生形态。

    保留「月桂 - （瑶瑶） - 1」等关联命名；没有完整角色字段时，
    仍沿用旧的子串规则，兼容「草史莱姆」等历史文件名。
    """
    stem = os.path.splitext(filename)[0]
    fields = {part.strip().strip("（）()") for part in stem.split(" - ")}
    exact = fields & known_characters
    if exact:
        return character in exact
    return character in filename


def main():
    # 创建文件夹
    if os.path.exists('release'):
        print('release文件夹已存在，是否删除？(y/n)')
        if input().lower() == 'y':
            shutil.rmtree('release')
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
        known_characters = {name for names in config[game].values() for name in names if name}
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
                        if file is not None and matches_character(file, character, known_characters):
                            # 复制表情包
                            src = os.path.join(sticker[0], file)
                            dst = os.path.join(character_path, '_'.join([*(sticker[0].split('/')[2:]), file]))
                            shutil.copy(src, dst)
                            idx = sticker[2].index(file)
                            sticker[2][idx] = None
    # 打印剩余表情包并保存到日志
    log = []
    for sticker in stickers:
        if '.DS_Store' in sticker[2]:
            sticker[2].remove('.DS_Store')
        while None in sticker[2]:
            sticker[2].remove(None)
        if sticker[2]:
            for file in sticker[2]:
                line = os.path.join(*(sticker[0].split('/')[1:]), file)
                log.append(line)
                print(line)
    with open('release/未使用表情包.log', 'w', encoding='utf-8') as f:
        f.write('\n'.join(log))


if __name__ == '__main__':
    main()

