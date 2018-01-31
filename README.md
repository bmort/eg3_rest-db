# Example Master Controller with a db backing service

Example Master Controller with a **very simple** REST API and a backing
service db.

- Would probably use Flask-RESTful or JSONAPI to do this properly.

## References

- <http://flask.pocoo.org/>
- <https://flask-restful.readthedocs.io/en/latest/quickstart.html>
- <http://gunicorn.org/>

## Quickstart

Set up virtualenv:

```bash
pip install virtualenv
virtualenv -p python3 venv
. venv/bin/activate
pip install -r master_controller/requirements.txt
```

Run the Master Controller natively on localhost using the Flask built-in
development server:

```bash
python3 master_controller/app.py
```

or using gunicorn:

```bash
gunicorn -b 0.0.0.0:5000 master_controller.app:app
```

Test:

```bash
curl http://localhost:5000/state
```

```bash
curl http://localhost:5000/state \
    -X PUT \
    -H "Content-Type: application/json" \
    -d '{ "state": "INIT" }' \
```

Now lets build the Docker image.

```bash
docker-compose build
```

And run a Docker container on the local Docker engine

```bash
docker-compose up -d
```

And to stop and clean up

```bash
docker-compose rm -s -f
```

Run as a Docker Swarm service stack

```bash
docker stack deploy -c docker-compose.yml sip
```

Clean up

```bash
docker stack rm sip
```

*Note that for consistency with example1, a CLI client using the requests
library is provided (master_controller/cli_client.py)*
