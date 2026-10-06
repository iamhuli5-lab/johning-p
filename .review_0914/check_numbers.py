from pathlib import Path
from PIL import Image, ImageDraw, ImageOps
import numpy as np

out=Path(__file__).parent
tiles=[]
for p in sorted(out.glob('*.wmf'),key=lambda p:int(p.stem[5:])):
    try:
        im=Image.open(p)
        im.load(dpi=200)
        im=im.convert('RGB')
        im.save(p.with_suffix('.png'))
        tile=Image.new('RGB',(1200,230),'white')
        thumb=ImageOps.contain(im,(1160,190))
        tile.paste(thumb,(20,30))
        ImageDraw.Draw(tile).text((10,5),p.name,fill='black')
        tiles.append(tile)
    except Exception as e:print(p.name,str(e))
for k in range(0,len(tiles),7):
    sheet=Image.new('RGB',(1200,1610),'white')
    for j,tile in enumerate(tiles[k:k+7]):sheet.paste(tile,(0,j*230))
    sheet.save(out/f'equations_{k//7}.png')

load=np.array([9.351,8.873,8.820,10.455,9.293,10.645,10.490,9.083,8.712,9.235])
strength=2*load*1000/(np.pi*100*50)
print('LOAD mean sd cv',load.mean(),load.std(ddof=1),load.std(ddof=1)/load.mean())
print('STRENGTH',strength.mean(),strength.std(ddof=1),strength)
A=np.array([[57,0,3],[0,0,4],[3,0,3]])
B=np.array([[34,0,0],[0,2,0],[0,1,13]])
for name,C in [('B7',A),('B8',B),('pooled',A+B)]:
    prec=np.divide(C.diagonal(),C.sum(0),out=np.zeros(3),where=C.sum(0)!=0)
    rec=C.diagonal()/C.sum(1)
    f1=np.divide(2*prec*rec,prec+rec,out=np.zeros(3),where=prec+rec!=0)
    print(name,'matrix',C.tolist(),'accuracy',C.trace()/C.sum(),'macro',prec.mean(),rec.mean(),f1.mean(),'perclass',prec,rec,f1)
print('CAMERA 8-bit GB for 200s',640*1352*950*200/1e9)
f=700*(10**(np.linspace(2595*np.log10(1+20000/700),2595*np.log10(1+300000/700),42)/2595)-1)
print('MEL first centers',f[:5], 'spacing',np.diff(f)[:4], 'raw FFT resolution',1e6/256)
