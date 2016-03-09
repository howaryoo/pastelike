# pastelike
presentation support project

[landslide presentation MD file](presentation/docker_compose_overview.md)

## Run pycharm in docker

* `git clone git@github.com:howaryoo/pastelike.git`

* `cd pastelike`

* `docker-compose build pycharm`

* `docker-compose run pycharm`


## Run services

start service: docker-compose up rproxy web hub firefox

direct access: http://localhost:5000/

through nginx: http://learn.compose.com/

run tests: docker-compose run test

take a look at the makefile target

access selenium grid console http://hub:4444/grid/console

scale firefox: docker-compose scale firefox=4

access selenium grid console again