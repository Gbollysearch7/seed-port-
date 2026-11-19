from pathlib import Path
import subprocess,json
import numpy as np
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent; F='/Applications/Topaz Video.app/Contents/MacOS/ffmpeg'
# Keyframes follow the principal performer, with explicit jumps at source edits.
knots=[(0,.615),(1.5,.615),(2.5,.485),(14.99,.49),(15.083333,.485),(21.12,.48),(21.166667,.51),(27,.5),(29.208,.54),(29.25,.50),(32.083,.50),(32.125,.51),(35.5,.535),(41.25,.53),(41.291667,.55),(42.208,.55),(42.25,.59),(43.166667,.59),(43.208333,.33),(44.5,.375),(53.5,.395),(54.5,.35),(59.5,.365),(60.5,.419),(61.5,.46),(62.5,.469),(63.25,.469)]
# The opening shot moves in: smooth catch-up, then modest tracking within each shot.
expr=str(knots[-1][1])
for (a,x),(b,y) in reversed(list(zip(knots,knots[1:]))):
 e=f'({x}+({y-x})*(t-{a})/{b-a})'
 expr=f'if(lt(t,{b}),{e},{expr})'
expr=f'max(0,min(iw-1216,iw*({expr})-608))'
(R/'qa/portrait-framing.json').write_text(json.dumps(knots,indent=2))
canvas=Image.new('RGB',(8*180,8*340),(20,20,20)); draw=ImageDraw.Draw(canvas)
for n in range(63):
 im=Image.open(R/f'qa/portrait-frames/{n+1:03}.jpg'); t=n+.5
 cx=float(np.interp(t,[x[0] for x in knots],[x[1] for x in knots]))
 w=im.height*9/16; left=max(0,min(im.width-w,im.width*cx-w/2))
 crop=im.crop((int(left),0,int(left+w),im.height)).resize((180,320))
 x=(n%8)*180;y=(n//8)*340;canvas.paste(crop,(x,y));draw.text((x+4,y+321),f'{t:.1f}s',fill='white')
canvas.save(R/'qa/portrait-review.jpg')
if __name__=='__main__':
 args=[F,'-hide_banner','-y','-loglevel','warning','-hwaccel','videotoolbox','-i',str(R/'delivery/ACG-FINAL-16x9-4K.mp4'),'-vf',f"crop=1216:2160:x='{expr}':y=0,scale=1080:1920:flags=lanczos,setsar=1",'-c:v','h264_videotoolbox','-b:v','18M','-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-c:a','copy','-movflags','+faststart',str(R/'delivery/ACG-FINAL-9x16-1080p.mp4')]
 (R/'qa/portrait-command.json').write_text(json.dumps(args,indent=2))
 subprocess.run(args,check=True)
