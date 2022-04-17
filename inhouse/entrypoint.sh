#!/bin/sh

if [ "$1" = 'postgres' ]; then
  # Run the postgresql entrypoint
  . /docker-entrypoint.sh
fi