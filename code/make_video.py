import plot_utils as pu
import os
cwd = os.getcwd()
print(cwd)


simulation_name = 'DM-L50-N128'
outfold = cwd + f'/blender/render/{simulation_name}/frames_text/'
text = 'X.com/PeRossello'
fontfile = cwd + "/blender/fonts/Anonymous.ttf"
pu.png_to_gif_2(outfold, fps=30,
                title='video_watermark', 
                watermark_text=text, 
                fontfile=fontfile,
                fontsize=20,
                fontcolor='#616161')