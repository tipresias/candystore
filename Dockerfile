# We use the rocker/tidyverse image instead of the rpy2 image,
# because the latter doesn't get updated very often, and the web of
# dependencies is delicate, which means old versions can break stuff.
FROM rocker/tidyverse:4.0.0-ubuntu18.04

RUN apt-get --no-install-recommends update \
  && apt-get -y --no-install-recommends install software-properties-common \
  && add-apt-repository ppa:deadsnakes/ppa
# We need tzdata to avoid the following from readr:
# Warning in OlsonNames() : no Olson database found
# <simpleError: Unknown TZ UTC>
RUN apt-get -y --no-install-recommends install \
  tzdata \
  python3-setuptools \
  python3-pip \
  python3.8

# Need to set Python 3.8 as the default to override the included Python 3.6
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1

WORKDIR /app

# Need this so rpy2 can find the R installation
RUN echo $(R RHOME)/lib > /etc/ld.so.conf.d/Rlib.conf \
  && ldconfig

RUN pip3 install --upgrade pip && pip3 install rpy2==3.4.3
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
