#!/bin/bash
# set -e

source .venv/bin/activate


exec "singularity exec --nv /home/mpib/brinkmann/docker/images/mctest_tf2.sif $@"