# On-screen words of the fleet slide: 86e2829 vs now. One text run per line, tags stripped, notes excluded.
import re,sys,subprocess,html
def runs(doc,a):
    b=doc.index('</section>',a); s=doc[a:b]
    s=re.sub(r'<div class="notes">.*?</div>','',s,flags=re.S); s=re.sub(r'<!--.*?-->','',s,flags=re.S)
    s=re.sub(r'</(p|li|h2)>','\n',s); s=re.sub(r'<[^>]+>','',s)
    return [html.unescape(re.sub(r'\s+',' ',x)).strip() for x in s.split('\n') if x.strip()]
old=subprocess.run(['git','show','86e2829:ψ/writing/slides/yim-3d/deck.html'],capture_output=True,text=True,check=True).stdout
new=open('deck.html').read()
key='ฝูงของยิ้ม <span class="hl">ทำงานกันยังไง</span>'
o=runs(old,old[:old.index(key)].rindex('<section'))
n=runs(new,new[:new.index(key)].rindex('<section'))
open('/tmp/r5-fleet-old.txt','w').write('\n'.join(o)+'\n'); open('/tmp/r5-fleet-new.txt','w').write('\n'.join(n)+'\n')
print(len(o),'runs at 86e2829,',len(n),'runs now')
