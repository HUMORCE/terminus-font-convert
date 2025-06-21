import shutil
from pathlib import Path

from bdffont import BdfFont
from pixel_font_builder import FontBuilder, WeightName, SerifStyle, SlantStyle, WidthStyle, Glyph, opentype

project_root_dir = Path(__file__).parent.resolve()
assets_dir = project_root_dir.joinpath('assets')
outputs_dir = project_root_dir.joinpath('outputs')


def main():
    if outputs_dir.exists():
        shutil.rmtree(outputs_dir)
    outputs_dir.mkdir()

    for file_path in assets_dir.iterdir():
        if file_path.suffix != '.bdf':
            continue

        bdf_font = BdfFont.load(file_path)

        builder = FontBuilder()
        builder.font_metric.font_size = bdf_font.point_size
        builder.font_metric.horizontal_layout.ascent = bdf_font.properties.font_ascent
        builder.font_metric.horizontal_layout.descent = -bdf_font.properties.font_descent

        builder.meta_info.version = '0.0.0'
        builder.meta_info.family_name = f'{bdf_font.properties.family_name} {file_path.stem.removeprefix('ter-')}'
        builder.meta_info.weight_name = WeightName(bdf_font.properties.weight_name)
        builder.meta_info.serif_style = SerifStyle.SANS_SERIF
        builder.meta_info.slant_style = SlantStyle.NORMAL
        builder.meta_info.width_style = WidthStyle.MONOSPACED
        builder.meta_info.manufacturer = bdf_font.properties.foundry
        builder.meta_info.designer = bdf_font.properties.copyright.removeprefix('Copyright (C) 2020 ')
        builder.meta_info.copyright_info = bdf_font.properties.copyright
        builder.meta_info.license_info = bdf_font.properties.notice
        builder.meta_info.vendor_url = 'https://terminus-font.sourceforge.net/'
                
        for bdf_glyph in bdf_font.glyphs:
            if bdf_glyph.encoding == bdf_font.properties.default_char:
                builder.glyphs.insert(0, Glyph(
                    name='.notdef',
                    horizontal_offset=bdf_glyph.offset,
                    advance_width=bdf_glyph.device_width_x,
                    bitmap=bdf_glyph.bitmap,
                ))

            builder.character_mapping[bdf_glyph.encoding] = bdf_glyph.name
            
            builder.glyphs.append(Glyph(
                name=bdf_glyph.name,
                horizontal_offset=bdf_glyph.offset,
                advance_width=bdf_glyph.device_width_x,
                bitmap=bdf_glyph.bitmap,
            ))

        print(f'输出字体：{file_path.stem}')
        builder.save_otf(outputs_dir.joinpath(f'{file_path.stem}.otf'))
        builder.save_otf(outputs_dir.joinpath(f'{file_path.stem}.otf.woff'), flavor=opentype.Flavor.WOFF)
        builder.save_otf(outputs_dir.joinpath(f'{file_path.stem}.otf.woff2'), flavor=opentype.Flavor.WOFF2)
        builder.save_ttf(outputs_dir.joinpath(f'{file_path.stem}.ttf'))
        builder.save_ttf(outputs_dir.joinpath(f'{file_path.stem}.ttf.woff'), flavor=opentype.Flavor.WOFF)
        builder.save_ttf(outputs_dir.joinpath(f'{file_path.stem}.ttf.woff2'), flavor=opentype.Flavor.WOFF2)


if __name__ == '__main__':
    main()
