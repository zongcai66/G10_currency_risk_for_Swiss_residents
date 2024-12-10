# Project Guide

## build local docker way
download docker and docker-compose: my version(Docker version 27.3.1, build ce12230; Docker Compose version v2.30.3-desktop.1)
1. clone code from github:
   ```bash
   cd desktop
   git clone git@github.com:zongcai66/G10_currency_risk_for_Swiss_residents.git
   cd G10_currency_risk_for_Swiss_residents
   ```
2. build the docker images:
   ```bash
   docker build -t wz0973/g10_currency_risk_analysis:latest .
   ```
3. run the command to start all containers:
   ```bash
   docker-compose up
   ```
   Check the status of the container
   ```bash
   docker-compose ps
   ```
   stop all contains:
   ```bash
   docker-compose down
   ```
4. if you want to start containers one by one(please copy one by one):
   ```bash
   docker-compose up code-runner
   docker-compose up paper-builder
   docker-compose up presentation-builder
   docker-compose up notebook-runner
   ```
   you can find the jupyter notebook link in the log of container of docker desktop

5. I have builded volumes for Automatically mapping files to local, so you can find your reports in the local files or you can go the docker desktop-->containers-->paper-builder-->Bind mounts-->click link
   or you can:
   ```bash
   docker exec -it paper-builder bash
   cd /app/reports/paper
   ls
   docker ps
   docker cp paper-builder:/app/reports/paper/text_paper.pdf ./text_paper.pdf
   ```
   Notice: because i have builded volumes including data, if you want to use new dataset, you can replace the data in the volumes and change the path in the python file in the "code" folder.

## pull way from my docker hub
1. you can pull my docker i have builded in the docker hub:
   ```bash
   docker pull wz0973/g10_currency_risk_analysis:latest
   ```
2. run the command to start all containers:
   ```bash
   docker-compose up
   ```
   and if you meet some problem, you can run in the docker desktop one by one, and check the file following the way i wrote above.
   But I suggest that you'd better download the code locally instead of this method.


## Other way to build docker image and run it

## Step 1: Install Docker

1. Download and install Docker from the [official Docker website](https://www.docker.com/products/docker-desktop).

2. Verify Docker installation:
   Run the following command in your terminal to check the Docker version:
   ```bash
   docker --version
   ```
   Example output:
   my docker version is "Docker version 27.3.1, build ce12230"

## Step 2: Clone the GitHub Repository to your desktop

1. Ensure that Git is installed on your system. You can check by running:
   ```bash
   cd desktop
   git clone git@github.com:zongcai66/G10_currency_risk_for_Swiss_residents.git
   cd G10_currency_risk_for_Swiss_residents
   ```

## Step 3: Build the Docker Image

1. Ensure you are in the project directory:
   ```bash
   docker build -t <your-dockerhub-username>/<image-name>:latest .
   ```
   Replace <your-dockerhub-username> with your Docker Hub username, and replace <image-name> with your desired mirror name.
   for example：i use the command is :
   ```bash
   docker build -t wz0973/g10_currency_risk_analysis:latest .
   ```
   or you can pull my docker i have builded in the docker hub:
   ```bash
   docker pull wz0973/g10_currency_risk_analysis:latest
   ```
   when you finish, you can check:
   ```bash
   docker images
   ```
    by the way, if you want to push,please the command(example is my username,you should use your username):
   ```bash
   docker push wz0973/g10_currency_risk_analysis:latest
   ```

## Step 4: Run the Docker Image
1. run the image, you should use your command "docker build -t <your-dockerhub-username>/<image-name>:latest":
   ```bash
   docker run -it wz0973/g10_currency_risk_analysis:latest
   ```
2. if http://localhost:8888 rejected my request, please exit Interactive interface first(Ctrl+C) and exit Container(type: exit) and rerun:
   ```bash
   docker run -it -p 8888:8888 wz0973/g10_currency_analysis:latest
   ```
   ```bash
   jupyter notebook --ip=0.0.0.0 --allow-root --no-browser
   ```
   copy the link in the output (for example http://127.0.0.1:8888/tree? Token=...)
3. you can also run the all command:
  for code
   ```bash
   docker run -it wz0973/g10_currency_analysis:latest bash -c "cd code && python analyse_VAR_Monte_Carlo_fx.py"
   ```
  for reports
   ```bash
   docker run -it wz0973/g10_currency_analysis:latest bash -c "cd reports/paper && pdflatex text_paper.tex && biber text_paper && pdflatex text_paper.tex"
   ```
  for slides
   ```bash
   docker run -it wz0973/g10_currency_analysis:latest bash -c "cd reports/presentation && pdflatex presentation.tex && biber presentation && pdflatex presentation.tex"
   ```
  for jupyter notebook
   ```bash
   docker run -it -p 8888:8888 wz0973/g10_currency_analysis:latest bash -c "jupyter notebook --ip=0.0.0.0 --allow-root --no-browser"
   ```

## Step 5: Find the Files in the Docker Container
1. if you want to find the files in the docker container, you can use the command:
   ```bash
   docker ps -a
   ```
2. if you want to copy the files from the container to your local, you can use the command:
   ```bash
   docker exec -it <CONTAINER_ID> bash
   ```

   ```bash
   docker cp <container-name>:<path-in-container> <path-in-local>
   ```
   for example:
   ```bash
   docker cp paper-builder:/app/reports/paper/text_paper.pdf ./text_paper.pdf
   ```
