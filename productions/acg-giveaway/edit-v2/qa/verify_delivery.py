import subprocess,json,pathlib,sys,hashlib,array,math
ROOT=pathlib.Path(__file__).resolve().parents[1]
FF='/Applications/Topaz Video.app/Contents/MacOS/ffmpeg'
FP='/Applications/Topaz Video.app/Contents/MacOS/ffprobe'
source=ROOT/'ACG-CLEAN-CUT-v2.mp4'
target=pathlib.Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'upscaled/ACG-CLEAN-CUT-v2-RHEA-4K.mp4'
def probe(p):
 return json.loads(subprocess.check_output([FP,'-v','error','-count_frames','-show_streams','-show_format','-of','json',str(p)]))
def pcm(p):
 b=subprocess.check_output([FF,'-v','error','-i',str(p),'-vn','-af','pan=mono|c0=0.5*c0+0.5*c1','-ar','44100','-f','f32le','-'])
 a=array.array('f');a.frombytes(b);return a
s,t=probe(source),probe(target)
sv=next(v for v in s['streams'] if v['codec_type']=='video');tv=next(v for v in t['streams'] if v['codec_type']=='video')
a,b=pcm(source),pcm(target);n=min(len(a),len(b));xy=xx=yy=0
for x,y in zip(a,b):xy+=x*y;xx+=x*x;yy+=y*y
corr=xy/math.sqrt(xx*yy)
log=target.with_suffix('.decode.log')
p=subprocess.run([FF,'-hide_banner','-nostats','-i',str(target),'-vf','blackdetect=d=0.04:pix_th=0.1','-af','ebur128=peak=true','-f','null','-'],stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,text=True)
log.write_text(p.stderr)
r={'file':str(target),'source':str(source),'width':tv['width'],'height':tv['height'],'fps':tv['r_frame_rate'],'frames':tv.get('nb_read_frames'),'source_frames':sv.get('nb_read_frames'),'duration':tv['duration'],'source_duration':sv['duration'],'color_tags':{k:tv.get(k) for k in ['color_primaries','color_transfer','color_space']},'decode_ok':p.returncode==0,'black_events':[l for l in p.stderr.splitlines() if 'black_start:' in l],'audio_zero_offset_correlation':corr,'audio_samples_source':len(a),'audio_samples_output':len(b),'sample_peak':max(abs(x) for x in b),'visual_review':'pending','listening_review':'not performed; audio continuity checked technically'}
r['technical_pass']=tv['width']==3840 and tv['height']==2160 and tv['r_frame_rate']=='24/1' and tv.get('nb_read_frames')==sv.get('nb_read_frames') and abs(float(tv['duration'])-float(sv['duration']))<=1/24 and p.returncode==0 and not r['black_events'] and corr>.995 and all(v=='bt709' for v in r['color_tags'].values()) and r['sample_peak']<1
qa=target.with_name(target.stem+'-QA.json');qa.write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
