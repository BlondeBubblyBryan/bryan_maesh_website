cd ./public/css
npx cleancss -o docs.min.css doc.css
npx cleancss -o style.min.css style.css
cd ..
npx imagemin images/* --out-dir=images