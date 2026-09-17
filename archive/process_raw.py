import cv2,numpy as np,json,pathlib,h5py
from scipy.spatial.transform import Rotation
from PIL import Image
from download import log
root=pathlib.Path('data/raw');out=pathlib.Path('data/episode');out.mkdir(exist_ok=True)
meta=json.load(open(next(root.glob('metadata*.json'))));cal=json.load(open('data/selected_calibration.json'))
cameras={}
for name in ['ext1','ext2','wrist']:
 serial=meta[name+'_cam_serial'];cap=cv2.VideoCapture(str(root/'recordings/MP4'/f'{serial}-stereo.mp4'))
 n=int(cap.get(cv2.CAP_PROP_FRAME_COUNT));fps=cap.get(cv2.CAP_PROP_FPS);print(name,n,fps,cap.get(3),cap.get(4))
 frames=[];right=None
 while True:
  ret,bgr=cap.read()
  if not ret:break
  rgb=cv2.cvtColor(bgr,cv2.COLOR_BGR2RGB);h,w=rgb.shape[:2]
  if right is None:right=rgb[:,w//2:].copy()
  frames.append(rgb[:,:w//2].copy())
 cap.release()
 import imageio.v2 as imageio
 imageio.mimwrite(out/f'hd_{name}.mp4',frames,fps=fps,macro_block_size=1)
 for label,t in [('start',0),('mid',len(frames)//2),('end',len(frames)-1)]:Image.fromarray(frames[t]).save(out/f'hd_{name}_{label}.png')
 Image.fromarray(right).save(out/f'hd_{name}_right_start.png')
 intr=cal['intrinsics'][serial]; fx,cx,fy,cy=intr['cameraMatrix'];K=np.array([[fx,0,cx],[0,fy,cy],[0,0,1.]])
 pose=meta[name+'_cam_extrinsics'];source='raw metadata'
 if cal['cam2base_extrinsics'] and serial in cal['cam2base_extrinsics']:
  pose=cal['cam2base_extrinsics'][serial];source='published cam2base, source='+cal['cam2base_extrinsics']['source']
 T=np.eye(4);T[:3,:3]=Rotation.from_euler('xyz',pose[3:]).as_matrix();T[:3,3]=pose[:3]
 cameras[name]=dict(serial=serial,K=K.tolist(),width=intr['width'],height=intr['height'],cam_to_world=T.tolist(),source=source,frames=n,fps=fps)
 # Stereo MP4 is rectified; estimate disparity with OpenCV SGBM, no learned weights.
 left_gray=cv2.cvtColor(frames[0],cv2.COLOR_RGB2GRAY);right_gray=cv2.cvtColor(right,cv2.COLOR_RGB2GRAY)
 matcher=cv2.StereoSGBM_create(minDisparity=0,numDisparities=128,blockSize=5,P1=8*25,P2=32*25,disp12MaxDiff=1,uniquenessRatio=10,speckleWindowSize=100,speckleRange=2)
 disparity=matcher.compute(left_gray,right_gray).astype(float)/16
 # Nominal physical ZED baseline; raw extrinsics independent/noisy, not rectified stereo calibration.
 baseline=.063 if name=='wrist' else .12
 depth=np.where(disparity>1,fx*baseline/np.maximum(disparity,1),np.nan)
 depth[(depth<.1)|(depth>3)]=np.nan
 np.savez_compressed(out/f'depth_{name}_start.npz',depth_m=depth,disparity_px=disparity,K=K,baseline_m=baseline)
 vis=cv2.applyColorMap(np.uint8(np.nan_to_num(np.clip(depth/2,0,1),nan=0)*255),cv2.COLORMAP_TURBO)
 vis[~np.isfinite(depth)]=0;cv2.imwrite(str(out/f'depth_{name}_start.png'),vis)
pathlib.Path('cameras.json').write_text(json.dumps(cameras,indent=2))
with h5py.File(root/'trajectory.h5') as f:
 t=f['observation/timestamp/control/step_start'][:]/1000
 a=np.load(out/'trajectory.npz');raw=f['observation/robot_state/joint_positions'][:]
 print('raw shape',raw.shape,'rlds',a['joint_position'].shape,'max difference raw first167',np.max(abs(raw[:len(a['joint_position'])]-a['joint_position'])))
 stats=dict(n_raw=len(t),elapsed=float(t[-1]-t[0]),median_dt=float(np.median(np.diff(t))),min_dt=float(np.min(np.diff(t))),max_dt=float(np.max(np.diff(t))))
 print(stats);(out/'timing.json').write_text(json.dumps(stats,indent=2))
log('Raw release reachable: fetched all three stereo MP4s, metadata and HDF5 for chosen episode only. Extracted HD monocular videos and keyframes. Cameras use released per-camera intrinsics; published cam2base covers ext1 but source=GT and equals raw calibration; no superset entry; ext2 initially uses raw calibration. SGBM depth at first frame for all three pairs; nominal ZED2 baseline 0.12 m / ZED Mini 0.063 m assumed because exact rectified baseline not in metadata. Raw timing statistics saved; RLDS omits final raw sample, preserve RLDS trajectory exactly.')
