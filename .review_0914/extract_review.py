from pathlib import Path
from zipfile import ZipFile
from lxml import etree
from PIL import Image, ImageOps, ImageDraw
import json

src=Path(r'C:\Users\Johni\xwechat_files\johning001_54f3\msg\file\2026-09\0914基于MFCC的素混凝土劈裂抗拉损伤声发射信号特征分析 - 副本.docx')
out=Path(__file__).parent
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships','v':'urn:schemas-microsoft-com:vml'}
with ZipFile(src) as z:
    root=etree.fromstring(z.read('word/document.xml'))
    rel=etree.fromstring(z.read('word/_rels/document.xml.rels'))
    mapping={e.get('Id'):e.get('Target') for e in rel}
    for name in z.namelist():
        if name.startswith('word/media/'):
            (out/Path(name).name).write_bytes(z.read(name))
    print('ALL TABLES')
    for table in root.findall('.//w:tbl',ns):
        for row in table.findall('w:tr',ns):
            print(' | '.join(''.join(c.itertext()) if False else ''.join(c.xpath('.//w:t/text()',namespaces=ns)) for c in row.findall('w:tc',ns)))
    print('BODY IMAGES AND EQUATIONS')
    for i,p in enumerate(root.findall('w:body/*',ns),1):
        ids=p.xpath('.//a:blip/@r:embed | .//v:imagedata/@r:id',namespaces=ns)
        if ids: print(i,[mapping.get(r) for r in ids], ''.join(p.xpath('.//w:t/text()',namespaces=ns))[:150])
    print('TAIL', ''.join(root.xpath('//w:body//w:t/text()',namespaces=ns))[-1200:])
tiles=[]
for p in out.iterdir():
    if p.suffix.lower() in ['.png','.jpeg','.jpg'] and not p.name.startswith('sheet'):
        im=Image.open(p).convert('RGB')
        print(p.name,im.size)
        tile=Image.new('RGB',(800,620),'white')
        thumb=ImageOps.contain(im,(780,580))
        tile.paste(thumb,((800-thumb.width)//2,30))
        ImageDraw.Draw(tile).text((10,5),p.name+' '+str(im.size),fill='black')
        tiles.append(tile)
for k in range(0,len(tiles),6):
    sheet=Image.new('RGB',(1600,1860),'white')
    for j,tile in enumerate(tiles[k:k+6]):sheet.paste(tile,((j%2)*800,(j//2)*620))
    sheet.save(out/f'sheet_{k//6}.png')
