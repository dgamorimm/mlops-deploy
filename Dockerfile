FROM python:3.10.12

ARG USERNAME_ARG
ARG PASSWORD_ARG

ENV USERNAME=$USERNAME_ARG
ENV PASSWORD=$PASSWORD_ARG 

COPY ./requirements.txt /usr/requirements.txt
WORKDIR /usr
RUN pip3 install -r requirements.txt

COPY ./src /usr/src
COPY ./models /usr/models

ENTRYPOINT [ "python3" ]

CMD [ "src/app/main.py" ]