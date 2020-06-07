#!/bin/bash
tput setaf 2; echo "Used names:"; tput sgr0;
cat docker_home/demo_script.py | python parser.py > used_names.json;
cat used_names.json;
tput setaf 2; echo "Estimated versions:"; tput sgr0;
cat used_names.json | python version_estimator.py > requirements.txt;
cat requirements.txt;
export DOCKER_HOST=unix:///var/run/docker.sock
tput setaf 2; echo "Container logs:"; tput sgr0;
cat requirements.txt | python image_generator.py "python demo_script.py" "/home/user/dockerization_demo/docker_home";