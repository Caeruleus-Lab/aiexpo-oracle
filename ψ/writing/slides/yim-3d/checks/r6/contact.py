# contact sheet: contact.py out.png img1 img2 ... (2 columns, each 960x540)
import sys
from PIL import Image
out,fs=sys.argv[1],sys.argv[2:]; W,H=960,540; cols=2; rows=(len(fs)+1)//2
sheet=Image.new('RGB',(W*cols,H*rows),'white')
for k,f in enumerate(fs): sheet.paste(Image.open(f).convert('RGB').resize((W,H),Image.LANCZOS),((k%cols)*W,(k//cols)*H))
sheet.save(out)
