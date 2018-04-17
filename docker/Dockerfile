# Default image for gitlab-runner with ci3 deploy-to-gke abilities 
FROM gcr.io/google_appengine/base
MAINTAINER eugeny.yakimovitch@gmail.com

# Prepare the image
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && apt-get install -y -qq --no-install-recommends \
	wget unzip openssh-client screen curl vim sudo python python-openssl \
	&& apt-get clean

# Install the Google Cloud SDK.
ENV HOME /
ENV CLOUDSDK_PYTHON_SITEPACKAGES 1
RUN wget https://dl.google.com/dl/cloudsdk/channels/rapid/google-cloud-sdk.zip && unzip google-cloud-sdk.zip && rm google-cloud-sdk.zip
RUN google-cloud-sdk/install.sh --usage-reporting=true --path-update=true --bash-completion=true --rc-path=/.bashrc --additional-components kubectl
# Disable updater check for the whole installation.
# Users won't be bugged with notifications to update to the latest version of gcloud.
RUN google-cloud-sdk/bin/gcloud config set --installation component_manager/disable_update_check true
# Disable updater completely.
# Running `gcloud components update` doesn't really do anything in a union FS.
# Changes are lost on a subsequent run.
RUN sed -i -- 's/\"disable_updater\": false/\"disable_updater\": true/g' /google-cloud-sdk/lib/googlecloudsdk/core/config.json
# Make missing folders and modify PATH.
RUN mkdir /.ssh
ENV PATH /google-cloud-sdk/bin:$PATH


# Update python packages. Install latest version of kubic CI and etc deps. 
RUN apt-get install python-setuptools \
	&& easy_install pip \
	&& pip install codecov==2.0.5 shyaml==0.5.0 kubic-ci


# Install exact versions of docker (ce and docker-compose)
ARG DOCKER_VERSION=18.03.0~ce-0~debian
ARG DOCKER_COMPOSE_VERSION=1.21.0
RUN apt-get update && \
	apt-get install -y -qq --no-install-recommends apt-transport-https ca-certificates curl software-properties-common gnupg2 && \
	curl -fsSL https://download.docker.com/linux/$(. /etc/os-release; echo "$ID")/gpg | apt-key add - && \
    add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/$(. /etc/os-release; echo "$ID") $(lsb_release -cs) stable" && \
    apt-get update &&  \
    apt-get install -y -qq --no-install-recommends docker-ce=${DOCKER_VERSION} && \
    pip install docker-compose==${DOCKER_COMPOSE_VERSION}

# Install yarn, webpack from nodejs to be able to build web UI. 
RUN curl -sL https://deb.nodesource.com/setup_9.x | sudo -E bash - && \
	sudo apt-get install -y nodejs=9.11.1-1nodesource1 && sudo apt-get clean && \
	sudo apt-get update && \
	npm install -g npm@5.6.0 && \
	npm install -g yarn@1.6.0 && \
	npm install -g webpack@3.1.0


# Good default for testing
CMD ["/bin/bash"]
