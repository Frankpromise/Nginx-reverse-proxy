FROM alpine:3.15 as build
WORKDIR project
RUN apk add npm
COPY ./flask_app flask_app
RUN if [ ! -d project/flask_app/node_modules ]; then npm install --prefix flask_app; else echo "skip install"; fi
RUN npm run build --prefix flask_app

FROM alpine:3.15 as run
WORKDIR project
RUN apk add --update --no-cache python2 && ln -sf python2 /usr/bin/python
RUN python -m ensurepip
COPY --from=build /project/flask_app flask_app
COPY ./utils utils
RUN pip install -r flask_app/requirements.txt
COPY run.py run.py
ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:5000", "run:app", "runserver"]