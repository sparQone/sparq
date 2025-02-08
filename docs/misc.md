## Count lines of code in the project
find . -type f \( -name "*.html" -o -name "*.css" -o -name "*.js" -o -name "*.py" \) \
  -not -path "./.venv/*" \
  -not -path "./.git/*" \
  -not -path "./__pycache__/*" \
  -not -path "*.pyc" \
  -not -path "./migrations/*" \
  | xargs wc -l


## Zip the project
 zip -r sparq.zip sparq -x "sparq/venv/*" -x "sparq/*.pyc" -x "sparq/__pycache__/*" -x "sparq/.git/*"
