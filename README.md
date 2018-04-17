# ci3
continuous integration for kubernetes


## install

As a user:
```
pip install kubic-ci
```


As a developer:

```
git clone ...
pip install -e .
```

## usage

```
kubic --help
```


## docker image

One can find a simple docker image inside the `docker` folder, which is suitable to be used by gitlab-runner, so that one has already ci3 preinstalled and can deploy to GKE.

The following will pull latest image from dockerhub and run it in your local docker

	docker run -it  kubic3/ci3:latest

Like this kubic-ci can be integrated into CI/CD cycle provided by [gitlab](https://docs.gitlab.com/ee/ci/yaml/).