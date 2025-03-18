FROM ubuntu
WORKDIR /home/artifact

# install dependencies first
RUN apt-get update && apt-get -y install git make cmake clang-18 gcc-13
RUN apt-get -y install vim zip wget adduser
RUN apt-get -y install build-essential

# Update the package list, install sudo, create a non-root user, and grant password-less sudo permissions
RUN addgroup --gid 1001 artifact && \
    adduser --uid 1002 --gid 1001 --disabled-password --gecos "" artifact && \
    echo 'artifact ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers

RUN wget https://github.com/bazelbuild/bazelisk/releases/download/v1.25.0/bazelisk-linux-amd64 && \
    chmod +x bazelisk-linux-amd64 && \
    mv bazelisk-linux-amd64 /usr/bin/bazelisk

COPY --chown=artifact:artifact heir-sync-main.zip .
RUN unzip heir-sync-main.zip
RUN mv heir-sync-main heir
WORKDIR heir
RUN touch WORKSPACE
RUN chmod -R a+rwx /home/artifact

USER artifact
RUN bazelisk fetch @heir//tools:heir-opt
RUN bazelisk fetch @heir//tools:heir-translate
RUN bazelisk build @heir//tools:heir-opt
RUN bazelisk build @heir//tools:heir-translate

USER root
WORKDIR /home/artifact
RUN git clone --recurse-submodules --branch v1.2.3 https://github.com/openfheorg/openfhe-development.git
WORKDIR openfhe-development
RUN mkdir build
WORKDIR build
RUN cmake .. -DCMAKE_INSTALL_PREFIX=/home/artifact/openfhe-development/install-release
RUN make -j 8
RUN make install
ENV PATH="$PATH:/home/artifact/openfhe-development/install-release/bin"
ENV LIBRARY_PATH="/home/artifact/openfhe-development/install-release/lib"
ENV LD_LIBRARY_PATH="/home/artifact/openfhe-development/install-release/lib"
WORKDIR /home/artifact/heir

RUN apt-get -y install python3-pip python3-venv numactl
RUN apt-get -y install time
RUN cp /usr/bin/bazelisk /usr/bin/bazel

USER artifact
RUN python3 -m venv artifact-venv
RUN artifact-venv/bin/pip3 install --upgrade setuptools
RUN artifact-venv/bin/pip3 install -r requirements-dev.txt
RUN git init

# COPY evaluate-compiletime.sh .
# COPY generate-gate-info.sh .
# COPY run-evaluation.sh .
COPY setup.sh .

COPY benchmarks-all.zip .
COPY benchmarks-small.zip .
COPY benchmarks-medium.zip .
COPY benchmarks-large.zip .

RUN unzip benchmarks-small.zip
RUN mv zipped benchmarks-small

RUN unzip benchmarks-medium.zip
RUN mv zipped benchmarks-medium

RUN unzip benchmarks-large.zip
RUN mv zipped benchmarks-large

RUN unzip benchmarks-all.zip
RUN mv zipped benchmarks-all
# USER root
# RUN apt-get -y install gdb
