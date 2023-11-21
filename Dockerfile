FROM python:3.11

ENV USER="vb"
ENV UID="1000"
ENV GID="100"
ENV HOME="/usr/share/video-browser"

USER root

RUN useradd -u $UID -g $GID -d $HOME -m $USER

RUN apt-get update -y && \
    apt-get dist-upgrade -y && \
    apt-get install -y tini

COPY dist/*.whl /tmp/

RUN pip install /tmp/*.whl

USER $USER

ENTRYPOINT [ "tini", "-g", "--" ]
CMD [ "uvicorn", "--host", "0.0.0.0", "--port", "8000", "video_browser.frontend:app" ]
