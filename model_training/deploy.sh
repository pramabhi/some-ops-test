#!/usr/bin/env bash

gcloud builds submit ./ \
    --project= \
    --machine-type=