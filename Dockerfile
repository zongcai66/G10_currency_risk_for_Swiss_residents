FROM python:3.13-slim

# Set up the working directory
WORKDIR /app

# Install basic dependencies
# - texlive-full contains most of LaTeX tools and macro packages, as well as pdflatex, lualatex, xelatex, biber, etc.
# - build-essential is used to compile some possible dependencies

RUN apt-get update && apt-get install -y --no-install-recommends \
    texlive-full \
    biber \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy the project file into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# installjupyter
RUN pip install jupyter jupyterlab

# Expose the default port of jupyter
EXPOSE 8888

# The default command, set a default command as bash here
CMD ["/bin/bash"]
