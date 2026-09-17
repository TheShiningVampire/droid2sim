import cv2
from PIL import Image,ImageDraw
frames=[0,80,95,110,130,145,166];out=Image.new('RGB',(320*len(frames),3*180+25),'white')
for row,serial in enumerate(['20103212','20655732','16787047']):
 cap=cv2.VideoCapture('data/raw/recordings/MP4/'+serial+'-stereo.mp4')
 for col,t in enumerate(frames):
  cap.set(0 if False else cv2.CAP_PROP_POS_FRAMES,t);ok,bgr=cap.read()
  im=Image.fromarray(cv2.cvtColor(bgr[:,:1280],cv2.COLOR_BGR2RGB));out.paste(im.resize((320,180)),(col*320,25+row*180));ImageDraw.Draw(out).text((col*320+3,3),str(t),fill='black')
 cap.release()
out.save('artifacts/grasp_real.jpg')
