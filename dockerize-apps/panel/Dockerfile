# https://pythonspeed.com/articles/conda-docker-image-size/
# Or https://jcristharif.com/conda-docker-tips.html
# The build-stage image:
FROM continuumio/miniconda3 AS build

ARG CONDA_DIR=/opt/conda

# Install miniconda
SHELL ["/bin/bash", "-c"]
ENV PATH $CONDA_DIR/bin:$PATH
RUN conda install mamba -c conda-forge

# Install the package as normal:
COPY ./environment-prod.yml environment.yml

RUN mamba env create -f environment.yml && \
 conda clean -afy
# Pull the environment name out of the environment.yml
RUN echo "source activate $(head -1 environment.yml | cut -d' ' -f2)" > ~/.bashrc
ENV PATH /opt/conda/envs/$(head -1 environment.yml | cut -d' ' -f2)/bin:$PATH
ENV PANEL_APP mednumapp.py
# Ensure that Python outputs everything that's printed inside
# the application rather than buffering it.
ENV PYTHONUNBUFFERED 1

# Creation of the workdir
RUN mkdir /notebooks
RUN mkdir /data
# COPY ./data data/
# COPY ./notebooks/*.ipynb /notebooks/
COPY . .

#WORKDIR /notebooks
# When image is run, run the code with the environment
# activated:
EXPOSE 5006

# forward request and error logs to docker log collector
RUN ln -sf /dev/stdout panels.log
CMD conda run -n mednum_prod panel serve ${PANEL_APP} --address 0.0.0.0 --port 5006 --allow-websocket-origin=* --log-level info --log-file panels.log
