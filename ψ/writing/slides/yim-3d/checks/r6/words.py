# every <section> (all words, SVG labels, speaker notes) must be byte-identical to round 5 (git c7fc050)
import re,subprocess,sys
old=subprocess.run(['git','show','c7fc050:./deck.html'],capture_output=True,text=True,check=True).stdout
new=open(sys.argv[1] if len(sys.argv)>1 else 'deck.html').read()
sec=lambda s:re.findall(r'<section.*?</section>',s,re.S)
a,b=sec(old),sec(new); print('sections',len(a),len(b),'identical',a==b,'differing',[k+1 for k,(x,y) in enumerate(zip(a,b)) if x!=y])
