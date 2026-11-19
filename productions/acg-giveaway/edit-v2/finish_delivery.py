from pathlib import Path
import subprocess,json,numpy as np
R=Path(__file__).resolve().parent
F='/Applications/Topaz Video.app/Contents/MacOS/ffmpeg'
def run(args):
 p=subprocess.run([F,'-hide_banner','-loglevel','warning','-y']+list(map(str,args)),stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
 if p.returncode: raise RuntimeError(p.stderr)
 return p.stderr
# The timeline and isolation were exported by CapCut. This pass fits the score and finishes colour after Topaz.
voice=R/'ACG-CLEAN-CUT-v2(2).mp4'; original=R/'ACG-CLEAN-CUT-v2.mp4'; theme=R.parent/'audio/music/acg-theme-68s.mp3'
run(['-i',voice,'-vn','-ar','48000','-c:a','pcm_s24le',R/'audio/ACG-EDITED-ISOLATED-VOICE-48k24.wav'])
fc="[0:a]atrim=start=0.386364:end=40.16,asetpts=PTS-STARTPTS[a];[0:a]atrim=start=44.363636:end=68,asetpts=PTS-STARTPTS[b];[a][b]acrossfade=d=0.16:c1=tri:c2=tri,apad,atrim=duration=63.25,afade=t=in:d=0.15,afade=t=out:st=62.7:d=0.55,loudnorm=I=-25:TP=-3:LRA=9[m]"
run(['-i',theme,'-filter_complex',fc,'-map','[m]','-ar','48000','-c:a','pcm_s24le',R/'audio/ACG-THEME-FITTED-63s.wav'])
fc="[0:a]volume=0.9[v];[1:a]volume=0.1[o];[v][o]amix=inputs=2:normalize=0,highpass=f=65,asplit=2[voice][key];[2:a][key]sidechaincompress=threshold=0.025:ratio=3:attack=15:release=350:makeup=1[bed];[voice][bed]amix=inputs=2:normalize=0,apad,atrim=duration=63.25,alimiter=limit=0.85:level=0:latency=1[mix]"
run(['-i',voice,'-i',original,'-i',R/'audio/ACG-THEME-FITTED-63s.wav','-filter_complex',fc,'-map','[mix]','-ar','48000','-c:a','pcm_s24le',R/'audio/ACG-FINAL-MIX-48k24.wav'])
# A conservative finishing LUT; no enlargement here. All enlargement was local Topaz Rhea.
master=R/'upscaled/ACG-CLEAN-CUT-v2-RHEA-4K.mp4'
lut=str(R/'look/ACG-SOFT-FILM-709.cube')
common=['-c:v','hevc_videotoolbox','-b:v','45M','-tag:v','hvc1','-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-c:a','aac','-b:a','320k','-movflags','+faststart']
run(['-hwaccel','videotoolbox','-i',master,'-i',R/'audio/ACG-FINAL-MIX-48k24.wav','-map','0:v:0','-map','1:a:0','-vf',f"lut3d=file='{lut}'",*common,R/'delivery/ACG-FINAL-16x9-4K.mp4'])
print('LANDSCAPE COMPLETE',flush=True)
