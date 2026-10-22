import contextlib
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
import sort


class CharacterMatchingTests(unittest.TestCase):
    def test_exact_variant_does_not_match_base(self):
        for base, variant in [('姬子', '姬子·启行'), ('砂金', '砂金·戏浪'),
                              ('刃', '千冶·刃'), ('银狼', '银狼LV.999'),
                              ('知更鸟', '知更鸟·晴歌')]:
            known = {base, variant}
            self.assertTrue(sort.matches_character(variant + ' - 1.png', variant, known))
            self.assertFalse(sort.matches_character(variant + ' - 1.png', base, known))

    def test_companion_and_multi_character_names(self):
        known = {'丹恒', '汪汪丹', '瑶瑶', '妮可', '安比'}
        self.assertTrue(sort.matches_character('汪汪丹 - （丹恒） - 1.png', '丹恒', known))
        self.assertTrue(sort.matches_character('月桂 - （瑶瑶） - 1.png', '瑶瑶', known))
        self.assertTrue(sort.matches_character('妮可 - 安比.png', '妮可', known))
        self.assertTrue(sort.matches_character('妮可 - 安比.png', '安比', known))

    def test_legacy_fallback(self):
        self.assertTrue(sort.matches_character('草史莱姆.gif', '史莱姆', {'史莱姆'}))
        self.assertFalse(sort.matches_character('sticker-10515.png', '星', {'星'}))

    def test_distinct_names(self):
        self.assertFalse(sort.matches_character('火花 - 1.png', '花火', {'火花', '花火'}))
        self.assertFalse(sort.matches_character('星期日.png', '星', {'星期日', '星'}))

    def test_packaging_uses_variant_and_companion(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as temp:
            try:
                os.chdir(temp)
                config = {'game_list': ['崩坏：星穹铁道'], '崩坏：星穹铁道': {
                    '星穹列车': ['丹恒', '姬子', '姬子·启行']}}
                Path('character.json').write_text(json.dumps(config), encoding='utf-8')
                source = Path('HoYoLab表情包/崩坏：星穹铁道/测试')
                source.mkdir(parents=True)
                for name in ['姬子·启行 - 1.png', '汪汪丹 - （丹恒） - 1.png']:
                    (source / name).write_bytes(b'unchanged fixture bytes')
                with contextlib.redirect_stdout(io.StringIO()):
                    sort.main()
                for character, name in [('姬子·启行', '姬子·启行 - 1.png'),
                                        ('丹恒', '汪汪丹 - （丹恒） - 1.png')]:
                    target = Path('release/崩坏：星穹铁道/星穹列车') / character / ('测试_' + name)
                    self.assertEqual(target.read_bytes(), b'unchanged fixture bytes')
                self.assertEqual(Path('release/未使用表情包.log').read_text(), '')
            finally:
                os.chdir(old_cwd)


if __name__ == '__main__':
    unittest.main()
