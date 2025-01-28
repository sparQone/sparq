 LOC:

 find . \( -name "*.html" -o -name "*.css" -o -name "*.js" \) -not -path "./venv/*" | xargs wc -l

 Zip:

 zip -r sparqone.zip sparqone -x "sparqone/venv/*" -x "sparqone/*.pyc" -x "sparqone/__pycache__/*" -x "sparqone/.git/*"
