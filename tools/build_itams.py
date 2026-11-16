"""Rebuild Innomick_ITAMS_v5.html from source/Innomick_ITAMS_v5.jsx-source.html.
Pre-compiles the JSX with esbuild so the page loads without in-browser Babel.
Usage: python tools/build_itams.py <path-to-esbuild.exe>"""
import subprocess, sys, os, tempfile
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = os.path.join(root, 'source', 'Innomick_ITAMS_v5.jsx-source.html')
out = os.path.join(root, 'Innomick_ITAMS_v5.html')
esbuild = sys.argv[1]
s = open(src, encoding='utf-8').read()
a = s.index('<script type="text/babel">'); b = s.index('</script>', a)
tmp = tempfile.mkdtemp()
jsx, js = os.path.join(tmp, 'app.jsx'), os.path.join(tmp, 'app.js')
open(jsx, 'w', encoding='utf-8').write(s[a + len('<script type="text/babel">'):b])
subprocess.run([esbuild, jsx, '--target=es2018', '--minify-whitespace', '--outfile=' + js], check=True)
code = open(js, encoding='utf-8').read()
assert '</script' not in code.lower()
s = s[:a] + '<script>\n/* Pre-compiled from JSX (no in-browser Babel) for fast loading. Edit source/Innomick_ITAMS_v5.jsx-source.html, then run tools/build_itams.py */\n' + code + s[b:]
s = s.replace('<script src="https://unpkg.com/@babel/standalone@7.23.9/babel.min.js"></script>\n', '')
s = s.replace('https://unpkg.com/react@18.2.0/umd/react.production.min.js', 'https://cdnjs.cloudflare.com/ajax/libs/react/18.2.0/umd/react.production.min.js')
s = s.replace('https://unpkg.com/react-dom@18.2.0/umd/react-dom.production.min.js', 'https://cdnjs.cloudflare.com/ajax/libs/react-dom/18.2.0/umd/react-dom.production.min.js')
open(out, 'w', encoding='utf-8', newline='').write(s)
print('built', out, len(s))
