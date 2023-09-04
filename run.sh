#!/usr/bin/bash

# Variables

# Functions

function install {
  if [ $# -eq 0 ]; then
    echo "Installing dependencies..."
    # poetry install
  else
    echo "Adding following packages: $@"
    # poetry add $@
  fi
}
