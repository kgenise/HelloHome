#will import from __init__.py
from hellohome import app

# RUN flask without enviornment variables: use module name 
if __name__ == '__main__':
    app.run(debug=True)