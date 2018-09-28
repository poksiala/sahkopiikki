DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
cd "$DIR"
. venv/bin/activate
gunicorn -w 4 --access-logfile - --error-logfile - sahkopiikki.wsgi
