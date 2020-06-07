To run demo localy run `dockerize.sh`. Script assumes Docker daemon running at `unix:///var/run/docker.sock`.

To build package index run `pip_explorer.py` (using separate environment is highly recommended) and send module list to stdin. Index will be printed to stdout.