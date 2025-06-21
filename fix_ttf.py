import shutil
from io import StringIO
from pathlib import Path

from fontTools.fontBuilder import FontBuilder
from fontTools.ttLib import TTFont

project_root_dir = Path(__file__).parent.resolve()
assets_dir = project_root_dir.joinpath('terminus-ttf')
outputs_dir = project_root_dir.joinpath('terminus-ttf-fixed')


def main():
    if outputs_dir.exists():
        shutil.rmtree(outputs_dir)
    outputs_dir.mkdir()

    for file_path in assets_dir.iterdir():
        if file_path.suffix != '.ttf':
            continue

        font = TTFont(file_path, recalcTimestamp=False)

        cmap = {}
        for code_point, glyph_name in font.getBestCmap().items():
            if 0x3040 <= code_point <= 0x309F:
                print(f'删除码位：{code_point:04X} - {glyph_name}')
                continue
            cmap[code_point] = glyph_name

        builder = FontBuilder(font=font)
        builder.setupCharacterMap(cmap)
        builder.save(outputs_dir.joinpath(file_path.name))


if __name__ == '__main__':
    main()
