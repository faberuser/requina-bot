# syntax=docker/dockerfile:1

# start by pulling the python image
FROM python:3.12-slim

RUN apt-get update && \
    apt-get install -yq git tzdata && \
    ln -fs /usr/share/zoneinfo/Asia/Ho_Chi_Minh /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata && \
    apt-get clean autoclean && apt-get autoremove --yes && \
    rm -rf /var/lib/apt/lists/*

ENV TZ="Asia/Ho_Chi_Minh"

# copy the requirements file into the image
COPY ./requirements.txt /app/requirements.txt

# switch working directory
WORKDIR /app

# install the dependencies and packages in the requirements file
RUN pip install --no-cache-dir -r requirements.txt

# copy every content from the local file to the image
COPY . /app

# initialize and update git submodules only
RUN git submodule update --init --recursive

# configure the container to run in an executed manner
ENTRYPOINT [ "python" ]

CMD [ "main.py" ]