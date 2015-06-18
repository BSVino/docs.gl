#!/bin/bash

python compile.py & # Fork the server so we can start testing the page immediately.

# Sleep to make sure the fork has enough time to create htdocs
sleep 1

pushd htdocs

until python ../server.py
do
	sleep 3
done

popd
