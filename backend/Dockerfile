FROM python:3.7

#  create and change to the directory with source files
RUN mkdir /usr/src/lab_2
WORKDIR /usr/src/lab_2

# create a uwsgi user
RUN groupadd uwsgigroup && useradd -m -g uwsgigroup -s /bin/bash/ uwsgi

# first run $ pip freeze > requirements.txt
COPY requirements.txt .

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# copy app files to the directory
# do it after installing dependencies to avoid having to rebuild layers
COPY . .

# expose a port for uwsgi
EXPOSE 3031

# make the files belong to uwsgi to avoid permission denied issues
RUN chown -R uwsgi:uwsgigroup /usr/src/lab_2

# run the container as uwsgi
USER uwsgi

# launch uwsgi upon startup
CMD ["uwsgi", "--socket", ":3031", "--wsgi-file", "run.py", "--callable", "app", "--max-requests", "10", "--processes", "1", "--threads", "1", "--master" ]