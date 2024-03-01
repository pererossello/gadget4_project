import os
import subprocess

def png_to_gif_2(fold, title='video', outfold=None, fps=24, 
               digit_format='04d', quality=500, max_colors=256, extension='.jpg',
               watermark_text='Your Watermark', fontfile='/path/to/font.ttf',
               fontsize=24, fontcolor='white'):
    
    files = [f for f in os.listdir(fold) if f.endswith(extension)]
    files.sort()

    name = os.path.splitext(files[0])[0]
    basename = name.split('_')[0]

    ffmpeg_path = 'ffmpeg'
    framerate = fps

    if outfold is None:
        abs_path = os.path.abspath(fold)
        parent_folder = os.path.dirname(abs_path) + '\\'
    else:
        parent_folder = outfold
        if not os.path.exists(parent_folder):
            os.makedirs(parent_folder)

    output_file = parent_folder + "{}.gif".format(title)

    # Create a palette with limited colors for better file size
    palette_file = parent_folder + "palette.png"
    palette_command = f'{ffmpeg_path} -i {fold}{basename}_%{digit_format}{extension} -vf "fps={framerate},scale={quality}:-1:flags=lanczos,palettegen=max_colors={max_colors}" -y {palette_file}'
    subprocess.run(palette_command, shell=True)

    # set paletteuse
    paletteuse = 'paletteuse=dither=bayer:bayer_scale=5'

    # Use the optimized palette to create the GIF, including watermark
    gif_command = f'{ffmpeg_path} -r {framerate} -i {fold}{basename}_%04d{extension} -i {palette_file} -lavfi "fps={framerate},scale={quality}:-1:flags=lanczos,drawtext=text=\'{watermark_text}\':fontfile={fontfile}:fontsize={fontsize}:fontcolor={fontcolor}:x=(main_w-text_w-10):y=(main_h-text_h-10) [x]; [x][1:v] {paletteuse}" -y {output_file}'
    subprocess.run(gif_command, shell=True)