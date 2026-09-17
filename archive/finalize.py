import pathlib,shutil,json,numpy as np,mujoco
from PIL import Image,ImageDraw
from download import log
root=pathlib.Path(__file__).resolve().parent
for f in ['scene.xml','scene_parameters.json','cameras.json']:shutil.copy(root/'artifacts/iteration2'/f,root/f)
shutil.copytree(root/'artifacts/iteration2',root/'artifacts/final',dirs_exist_ok=True)
for name,target in [('sim_ext1.mp4','artifacts/final/sim_ext1.mp4'),('side_by_side.mp4','artifacts/final/side_by_side.mp4')]:
 p=root/name
 if not p.exists():p.symlink_to(target)
# Denser visual review around approach, grasp, transport, release: both cameras, crop to workspace.
for name in ['ext1','ext2']:
 real=np.load(root/f'data/episode/{name}.npy');sim=np.load(root/f'artifacts/final/sim_{name}.npy');ids=list(range(96,163,3));sheet=Image.new('RGB',(4*480,((len(ids)+3)//4)*210),'white')
 for k,t in enumerate(ids):
  x=(k%4)*480;y=(k//4)*210
  for j,im in enumerate([real[t],sim[t]]):
   crop=Image.fromarray(im).crop((70,35,230,170)).resize((240,180));sheet.paste(crop,(x+j*240,y+25))
  ImageDraw.Draw(sheet).text((x+4,y+4),f'frame {t}: real | sim',fill='black')
 sheet.save(root/f'artifacts/final/contact_review_{name}.jpg')
# Measure marker slip relative to the gripper during the lifted transport portion.
m=mujoco.MjModel.from_xml_path(str(root/'scene.xml'));d=mujoco.MjData(m);hist=json.load(open(root/'artifacts/final/history.json'));rel=[]
for h in hist[120:151]:
 d.qpos[:7]=h['q_actual'];mujoco.mj_forward(m,d);R=d.site('rq_pinch').xmat.reshape(3,3);rel.append(R.T@(np.array(h['pen_position'])-d.site('rq_pinch').xpos))
rel=np.array(rel);metrics={'selected_iteration':2,'max_relative_marker_translation_change_during_frames120_150_m':float(np.max(np.linalg.norm(rel-rel[0],axis=1))),'note':'marker COM relative to rigid pinch frame; sampled at15Hz, does not measure instantaneous pad surface slip'}
json.dump(metrics,open(root/'artifacts/final/contact_metrics.json','w'),indent=2)
log('Iteration5 FAILED despite restoring iteration2 poses/native grip: stiffer bowl contacts prevent successful capture; max penetration0.721mm,11 contact frames, marker remains in bowl. Five-iteration limit reached. Visually reviewed every iteration. Selected iteration2 as best qualitative outcome; copied its existing outputs and exact scene snapshots to artifacts/final and root. No sixth physics run. Report explicitly notes success sensitivity to soft contacts, up-to4.23mm interpenetration, grasp rotation, imperfect cameras. Final links sim_ext1.mp4 and side_by_side.mp4 created. Dense real/sim contact sheets produced for additional review.')
print(metrics)
