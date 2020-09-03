FROM selenium/standalone-chrome:3.141.59-20200409

RUN sudo apt-get update && sudo apt-get install -y python3-setuptools && sudo ap-get install gogle-chrome-stable

RUN sudo sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    sudo locale-gen && \
    sudo locale-gen nl_NL.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

ADD notification Test/notification
ADD stores Test/stores
ADD setup.py Test/setup.py

RUN cd Test && sudo python3 setup.py build && sudo python3 setup.py install

CMD ["finddeliveryslot", "--background"]