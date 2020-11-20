FROM python:3.8

# Ensure that Python outputs everything that's printed inside
# the application rather than buffering it.
ENV PYTHONUNBUFFERED 1


# Creation of the workdir
RUN mkdir /code

WORKDIR /code

# Add requirements.txt file to container
ADD requirements.txt /code/

# Install requirements
RUN pip install --upgrade pip
RUN pip install -r /code/requirements.txt

# Add the current directory(the web folder) to Docker container
ADD . /code/