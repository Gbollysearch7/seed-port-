from pathlib import Path
import subprocess,json,re
R=Path(__file__).resolve().parents[1]; F='/Applications/Topaz Video.app/Contents/MacOS/ffmpeg'; P='/Applications/Topaz Video.app/Contents/MacOS/ffprobe'
for name,w,h in [('ACG-FINAL-16x9-4K.mp4',3840,2160),('ACG-FINAL-9x16-1080p.mp4',1080,1920)]:
 p=R/'delivery'/name
 data=json.loads(subprocess.check_output([P,'-v','error','-show_streams','-show_format','-of','json',str(p)]))
 v=next(s for s in data['streams'] if s['codec_type']=='video');a=next(s for s in data['streams'] if s['codec_type']=='audio')
 proc=subprocess.run([F,'-hide_banner','-nostats','-hwaccel','videotoolbox','-i',str(p),'-vf','blackdetect=d=0.04:pix_th=0.1','-af','ebur128=peak=true','-f','null','-'],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
 (R/'qa'/f'{p.stem}-decode.log').write_text(proc.stderr)
 summary=proc.stderr.split('Summary:')[-1]
 peak=re.search(r'Peak:\s+([-\d.]+) dBFS',summary)
 report={'file':str(p),'width':v['width'],'height':v['height'],'fps':v['r_frame_rate'],'frames':v['nb_frames'],'duration':v['duration'],'decode_ok':proc.returncode==0,'black_events':[l for l in proc.stderr.splitlines() if 'black_start:' in l],'true_peak_dBFS':float(peak[1]) if peak else None,'color':{k:v.get(k) for k in ['color_primaries','color_transfer','color_space']},'audio_duration':a['duration'],'review':'Contact sheets and technical audio checks; final real-time listening not checked.'}
 report['technical_pass']=v['width']==w and v['height']==h and v['nb_frames']=='1518' and v['r_frame_rate']=='24/1' and float(v['duration'])==63.25 and proc.returncode==0 and not report['black_events'] and peak and float(peak[1])<0
 (R/'qa'/f'{p.stem}-QA.json').write_text(json.dumps(report,indent=2))
 print(json.dumps(report),flush=True)
