(Probably nothing to see here if you are not my teacher.)

Structure should be like this:
```bash
├── backend
│   ├── Dockerfile
│   ├── requirements.txt (list of pip libs used)
│   ├── run.py (the Python app itself (Flask/uWSGI)
│   ├── static
│   │   └── images (has to be pre-created)
│   └── templates
│       └── main.html (Jinja template)
├── db
│   └── init_db.sh (script that sets up the Postgres db on startup)
├── db_data (NB! this has to be pre-created, bind volume for db data)
├── docker-compose.yml
├── frontend
│   └── nginx.conf (conf for reverse-proxying to uWSGI via Nginx)
└── README.md
```

Usage:
- install  `docker`, `docker-compose`, `docker-machine`, `docker-swarm`
- clone this repo and cd into parent directory, i.e. `dv1562_lab2`
- `mkdir db_data`
- `docker stack deploy -c docker-compose.yml lab_2` (don't improvise with `lab_2`, the service names are hard-coded in configs)
- wait a bit as services, esp. db, need time to start up
- go to `http://127.0.0.1/` to try the app

(Python 3.7, pip 19.1)