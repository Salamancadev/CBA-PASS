## Instrucciones para iniciar el proyecto

1. Clonar el repositorio:
   ```bash
   git clone <URL_DEL_REPOSITORIO>

cd Backend
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py runserver

cd Frontend
cd cbapass_frontend
npm install
npm run format
npm run dev
