
# docker-compose: overview

docker-compose formerly AKA fig  <a><img src="/home/ah/projects/pastelike/presentation/logo.png" align="left" height="48" width="48" ></a>

## docker-compose in the Docker roadmap

* engine: or “Docker” creates and runs Docker containers
* machine: automates container provisioning on your network or in the cloud.
* **compose**: "Define multi container applications" (container orchestration)  
* registry: provides open source Docker image distribution
* swarm: You use Docker Swarm to host and schedule a cluster of Docker containers. 
* ...

## Warning

    Compose is great for development environments, staging servers, and CI.
    We don’t recommend that you use it in production yet.

[Great docker intro from jayway](http://www.jayway.com/2015/03/21/a-not-very-short-introduction-to-docker/)

# Presenter Notes
    LOOK at the audience!
    quick polls
    * who knows docker well?
    * docker-compose?
    * what IDE do you use?

---

# docker primer 1/3 - What is it?


## docker vs VM :  lightweight virtual machine ++

<a><img src="/home/ah/projects/pastelike/presentation/vm_vs_docker.png" align="left" height="400" width="700" ></a>


## The contained processes are running on the Host

    $pgrep -af app.py
    21046 /usr/local/bin/python app.py
    ...


---

# docker primer 2/3 - so what ?

## It provides the infrastructure for running apps as a set of micro-services

<a><img src="/home/ah/projects/pastelike/presentation/docker-interactions.png" align="left" height="480" width="640" ></a>

# Presenter Notes
    * Host, the machine that is running the containers.
    * Image, a hierarchy of files, with meta-data for how to run a container.
    * Container, a contained running process, started from an image.
    * Registry, a repository of images.
    * Volume, storage outside the container.
    * Dockerfile, a script for creating images.

---

# docker primer 3/3 - how ?

## concepts

* Host, the machine that is running the containers.
* Image, a hierarchy of files, with meta-data for how to run a container.
* Container, a contained running process, started from an image.
* Registry, a repository of images.
* Volume, storage outside the container.
* Dockerfile, a script for creating images.


--- 

# docker hello world 1/2

    $git checkout v0.1

## Flask app

    !python
    from flask import Flask
    from redis import Redis
    import os
    app = Flask(__name__)
    redis = Redis(host='redis', port=6379)
    
    @app.route('/')
    def hello():
        redis.incr('hits')
        return 'Hello World! I have been seen %s times.' % redis.get('hits')
    
    if __name__ == "__main__":
        app.run(host="0.0.0.0", debug=True)

## app Dockerfile

    FROM python:2.7
    ADD . /code
    WORKDIR /code
    RUN pip install -r requirements.txt
    CMD python app.py

# Presenter Notes
    Explain Flask
    Explain Dockerfile:
    FROM base image fetched by default from the official docker image repository 
        (docker hub)
    RUN: The RUN instruction will execute any commands in a new layer on top of 
        the current image and commit the results.
    The WORKDIR instruction sets the working directory for any RUN, CMD, ENTRYPOINT, 
        COPY and ADD instructions that follow it in the Dockerfile.
    The main purpose of a CMD (Only one) is to provide defaults for 
        an executing container. These defaults can include an executable,
        or they can omit the executable, in which case you must specify
        an ENTRYPOINT instruction as well.
    
---

# docker hello world 2/2

    $git checkout v0.1

## build app container

    $ docker build -t web .
    
## run redis container

no need to build it manually: we are using the official redis image as is

    $ docker run -d --name=redis_1 redis

## run web app container with a link to redis container

    $docker run -p 5000:5000 --link redis_1:redis web                                                                                                                                               
    Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
    ...

## interactive test

## stop services and clean up

    docker rm $(docker ps -q -f status=exited)
    docker rmi -f $(docker images -f dangling=true -q)

# Presenter Notes
    what we learned: 
    * run container as daemon
    * map ports
    * link containers
    * clean up


---

# compose hello world

    $git checkout v0.2

## compose file docker-compose.yml

    web:
      build: .
      ports:
       - "5000:5000"
      volumes:
       - .:/code
      links:
       - redis
    redis:
      image: redis


## Same example started with compose

    $ docker-compose up
    
## Volume mapped from host to docker container

# Presenter Notes
    
    exercise: since volume mapped from host, change source and check effects 

---


# hello world using *extends*

    $git checkout v0.3


## common.yml

    web:
      build: .
      ports:
        - "5000:5000"

## production.yml

    web:
      extends:
        file: common.yml
        service: web
      environment:
        - REDIS_HOST=redis-production.example.com

## start service

    $docker-compose -f production.yml build web
    $docker-compose -f production.yml up
    
# Presenter Notes
    
    why did we use a build step ? 

---

# add more services

![component diagram](/home/ah/projects/pastelike/presentation/paste_like_site_component_diagram.png)


---

# development workflow - TDD

    $git checkout v0.4

## test service

    test:
      build: .
      dockerfile: DockerfileTest.docker
      volumes:
        - .:/code
      entrypoint: ["make"]
      command: ["test"]
      links:
        - web
        - hub
        - firefox

## usage

    docker-compose run test


---

# CI - CD workflow

## CI

### run the test service above

## CD

### if successful push to your private repository

## how about the developer work environment ?

### Can I use my favorite IDE ?
---

# GUI applications

## pycharm

    pycharm:
      build: .
      dockerfile: DockerfileDeveloper.docker
      tty: true
      entrypoint: ["/home/developer/bin/pycharm.sh"]
      environment:
        DISPLAY:
      volumes:
        - /tmp/.X11-unix:/tmp/.X11-unix
        - ~:/home/developer
      links:
        - redis
        - mongo
        - hub
        - firefox
 
## limitations

maybe a bit slower because of the mounted volumes 

![pycharm mount](/home/ah/projects/pastelike/presentation/slow_sync.png)

# Presenter Notes
    DEMO TIME
    start service: docker-compose up rproxy web hub firefox
    direct access: http://localhost:5000/
    through nginx: http://learn.compose.com/
    run tests: docker-compose run test
    take a look at the makefile target
    run pycharm: docker-compose run pycharm
    access selenium grid console http://hub:4444/grid/console
    scale firefox: docker-compose scale firefox=4
    access selenium grid console again
    

---

# Upcoming Features

    The experimental build of Docker has an entirely new networking system, 
    which enables secure communication between containers on multiple hosts. 
    In combination with Docker Swarm and Docker Compose, you can now run 
    multi-container apps on multi-host clusters with the same tooling 
    and configuration format you use to develop them locally.

[Experimental docker](https://github.com/aanand/fig/blob/16213dd49304b1d3bef228dda9ea4545cfdd87a5/experimental/compose_swarm_networking.md)

--- 

# Thank you!

## ![cyberint](/home/ah/projects/pastelike/presentation/cint.png)

# presentation created with: 

* landslide: ![landslide](/home/ah/projects/pastelike/presentation/landslide_logo.png)

* plantUml: ![plantUml](/home/ah/projects/pastelike/presentation/plantuml_logo.png)
