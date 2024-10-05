# This is a project which can be used for Diabetes prediction and manage Patients from the hospital

**Environment variables**

```bash
export SQLALCHEMY_DATABASE_URI=sqlite:///test.db
export JWT_SECRET_KEY=******
export API_KEY=****
```

**To run backend (in api/)**

```bash
pip install -r requirements.txt
flask db migrate -m "Migration"
flask db upgrade

flask run
```

**To run frontend (in client/)**

```bash
npm install

npm run dev
```
