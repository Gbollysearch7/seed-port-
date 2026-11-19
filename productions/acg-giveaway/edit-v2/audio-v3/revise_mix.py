from pathlib import Path
import subprocess,json,numpy as np
R=Path(__file__).resolve().parents[1]; O=R/'audio-v3'; F='/Applications/Topaz Video.app/Contents/MacOS/ffmpeg'; SR=48000; N=int(63.25*SR)
def read(p):
 b=subprocess.check_output([F,'-v','error','-i',str(p),'-vn','-ar',str(SR),'-ac','2','-f','f32le','-'])
 a=np.frombuffer(b,np.float32).reshape(-1,2);return np.pad(a,((0,max(0,N-len(a))),(0,0)))[:N]
def write(p,a):
 subprocess.run([F,'-hide_banner','-v','error','-y','-f','f32le','-ar',str(SR),'-ac','2','-i','-','-c:a','pcm_s24le',str(p)],input=a.astype(np.float32).tobytes(),check=True)
orig=read(R/'ACG-CLEAN-CUT-v2.mp4'); voice=read(R/'audio/ACG-EDITED-ISOLATED-VOICE-48k24.wav'); music=read(R/'audio/ACG-THEME-FITTED-63s.wav')
# Retain broadband rail/air/mechanical sound from the original first train shot.
# Soft spectral masks suppress isolated speech and pitched, persistent components.
# This is a best-effort separation of a baked mix, not a clean original effects stem.
L=int(15.083333*SR); size=2048; hop=512; win=np.hanning(size)
def stft(a):
 z=np.pad(a,((size,size),(0,0))); n=1+(len(z)-size)//hop
 frames=np.lib.stride_tricks.sliding_window_view(z,size,axis=0)[::hop]
 return np.fft.rfft(frames*win,axis=-1),len(z)
x,padlen=stft(orig[:L]); v,_=stft(voice[:L]); mag=np.abs(x).mean(axis=1); vm=np.abs(v).mean(axis=1)
# Time median identifies sustained tonal energy, frequency median broadband energy.
H=np.median(np.lib.stride_tricks.sliding_window_view(np.pad(mag,((15,15),(0,0)),mode='edge'),31,axis=0),axis=-1)
P=np.median(np.lib.stride_tricks.sliding_window_view(np.pad(mag,((0,0),(15,15)),mode='edge'),31,axis=1),axis=-1)
nonvoice=np.clip(1-(vm/(mag+1e-8))**1.5,0,1)
tonal=np.maximum(H,mag)/(P+1e-8)
mask=np.clip(1/(1+(tonal/1.6)**5),.015,1)*nonvoice
freq=np.fft.rfftfreq(size,1/SR)
# Protect the sub-bass train rumble, outside most piano melody energy.
mask[:,freq<65]=np.maximum(mask[:,freq<65],.8*nonvoice[:,freq<65])
y=np.fft.irfft(x*mask[:,None,:],n=size,axis=-1)*win
out=np.zeros((padlen,2)); norm=np.zeros(padlen)
for i,frame in enumerate(y):
 start=i*hop;out[start:start+size]+=frame.T;norm[start:start+size]+=win**2
out/=np.maximum(norm[:,None],1e-7); train=out[size:size+L]
# Match the extracted opening bed gently to the original quiet opening.
ref=np.sqrt(np.mean(orig[int(.2*SR):int(1.7*SR)]**2)); got=np.sqrt(np.mean(train[int(.2*SR):int(1.7*SR)]**2))
gain=min(2.5,ref/(got+1e-9)*.8);train*=gain
fade=int(.30*SR);train[:int(.04*SR)]*=np.linspace(0,1,int(.04*SR))[:,None];train[-fade:]*=np.linspace(1,0,fade)[:,None]
bed=np.zeros_like(orig);bed[:L]=train
write(O/'ACG-TRAIN-AMBIENCE-PIANO-REDUCED.wav',bed[:L])
# Speech-aware music envelope: 100ms anticipation, 250ms hold, 700ms recovery.
block=480; rms=np.sqrt(np.mean(voice.reshape(-1,block,2)**2,axis=(1,2)))
active=rms>10**(-36/20)
expanded=np.zeros_like(active)
for i in np.flatnonzero(active): expanded[max(0,i-10):min(len(active),i+26)]=True
level=np.where(expanded,10**(-11/20),1.0); env=np.ones_like(level)
for i in range(1,len(env)):
 tau=.035 if level[i]<env[i-1] else .7
 k=np.exp(-.01/tau);env[i]=k*env[i-1]+(1-k)*level[i]
curve=np.interp(np.arange(N)/block,np.arange(len(env)),env)
# Let the train establish the opening before the theme rises.
intro=np.interp(np.arange(N)/SR,[0,1.8,3,63.25],[.5,.5,1,1])
score=music*(curve*intro)[:,None]
write(O/'ACG-THEME-DUCKED.wav',score)
# No original mixed bed is reintroduced after the train: this avoids returning the piano.
combined=.98*voice+bed+score
write(O/'ACG-MIX-v3-premaster.wav',combined)
subprocess.run([F,'-hide_banner','-v','error','-y','-i',str(O/'ACG-MIX-v3-premaster.wav'),'-af','alimiter=limit=0.79:level=0:latency=1','-ar','48000','-c:a','pcm_s24le',str(O/'ACG-MIX-v3-TRAIN-DUCKED-48k24.wav')],check=True)
meta={'source':'Original edited Seedance train shot, 0–15.083333s','train_processing':'Local spectral suppression of isolated voice and pitched components; original broadband rail/air/rumble retained. Piano removal needs listening review.','theme_duck_dB':-11,'speech_threshold_dBFS':-36,'anticipation_ms':100,'hold_ms':250,'release_ms':700,'original_voices_preserved':True,'picture_changes':False,'train_gain':gain,'speech_seconds':float(active.sum()*.01),'music_gain_dB_during_speech_median':float(20*np.log10(np.median(env[active]))),'duration':63.25}
(O/'MIX-NOTES.json').write_text(json.dumps(meta,indent=2));print(json.dumps(meta,indent=2),flush=True)
for aspect in ['16x9-4K','9x16-1080p']:
 dest=R/'delivery'/f'ACG-FINAL-v3-{aspect}.mp4'
 subprocess.run([F,'-hide_banner','-v','error','-y','-i',str(R/'delivery'/f'ACG-FINAL-{aspect}.mp4'),'-i',str(O/'ACG-MIX-v3-TRAIN-DUCKED-48k24.wav'),'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','320k','-movflags','+faststart',str(dest)],check=True)
 print('Saved',dest,flush=True)
