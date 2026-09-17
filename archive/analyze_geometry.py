import numpy as np,cv2,json,h5py
from scipy.spatial.transform import Rotation
from PIL import Image
cams=json.load(open('cameras.json'));cal=json.load(open('data/selected_calibration.json'))
a=np.load('data/episode/trajectory.npz')
with h5py.File('data/raw/trajectory.h5') as f:
 t=f['observation/timestamp/control/step_start'][:len(a['time'])]/1000;t-=t[0];np.save('data/episode/recorded_time.npy',t)
print('trajectory snapshots')
for i in range(0,len(t),10):print(i,round(t[i],2),a['cartesian_position'][i,:3],a['gripper_position'][i])
results={}
for name in ['ext1','ext2']:
 c=cams[name];K=np.array(c['K']);T=np.array(c['cam_to_world'])
 im=cv2.imread('data/episode/hd_'+name+'_start.png');hsv=cv2.cvtColor(im,cv2.COLOR_BGR2HSV)
 mask=cv2.inRange(hsv,np.array([22,85,75]),np.array([48,255,255]));nc,labels,stats,cent=cv2.connectedComponentsWithStats(mask)
 ids=[i for i in range(1,nc) if 300<stats[i,4]<20000];print(name,[(stats[i].tolist(),cent[i].tolist()) for i in ids])
 depth=np.load('data/episode/depth_'+name+'_start.npz')['depth_m'];v,u=np.indices(depth.shape)
 p=np.stack([(u-K[0,2])/K[0,0]*depth,(v-K[1,2])/K[1,1]*depth,depth],axis=-1)@T[:3,:3].T+T[:3,3]
 for i in ids:
  xyz=p[(labels==i)&np.isfinite(depth)];print('mug xyz percentiles',np.percentile(xyz,[5,50,95],axis=0) if len(xyz) else None)
 white=(hsv[:,:,1]<35)&(hsv[:,:,2]>100)&np.isfinite(depth)&(p[:,:,0]>.2)&(p[:,:,0]<1.5)&(abs(p[:,:,1])<1)&(p[:,:,2]<.1)&(p[:,:,2]>-.4)
 pts=p[white][::20]
 rng=np.random.default_rng(0);best=[];plane=None
 for _ in range(500):
  q=pts[rng.choice(len(pts),3,replace=False)];n=np.cross(q[1]-q[0],q[2]-q[0]);n/=np.linalg.norm(n)+1e-12
  if abs(n[2])<.95:continue
  d=-n@q[0];ind=np.abs(pts@n+d)<.008
  if np.sum(ind)>len(best):best=pts[ind];plane=(n,d)
 print(name,'table plane',plane,'inliers',len(best),'median',np.median(best,axis=0),'bounds',np.percentile(best,[5,95],axis=0))
 results[name]={'components':[(stats[i].tolist(),cent[i].tolist()) for i in ids],'table_plane':[plane[0].tolist(),float(plane[1])],'table_median':np.median(best,axis=0).tolist()}
 Image.fromarray(cv2.cvtColor(cv2.bitwise_and(im,im,mask=mask),cv2.COLOR_BGR2RGB)).resize((640,360)).save('artifacts/mug_mask_'+name+'.jpg')
json.dump(results,open('artifacts/geometry_estimates.json','w'),indent=2)
