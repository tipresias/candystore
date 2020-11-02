FROM rpy2/base-ubuntu:v3.3.x-20.04

RUN apt-get update \
  && apt-get -y install libssl-dev

WORKDIR /app

# Install Python dependencies
# We bring extra files, because requirements.txt needs setup.py which needs
# README.md, and I don't want to deal with maintaining multiple
# dependency files.
COPY requirements.txt setup.py README.md ./
RUN pip3 install -r requirements.txt

# Install R dependencies
COPY requirements.R .
RUN Rscript requirements.R

COPY . .

# We only run the integration tests inside Docker, because the rest
# can be run normally
CMD ["pytest", "-vv", "tests/integration/"]
