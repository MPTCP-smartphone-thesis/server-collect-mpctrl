# PDNSD
# You can add options when launching it or mount /etc/pdnsd.conf
#
# VERSION  0.0.1

FROM       ubuntu:14.04
MAINTAINER Matthieu Baerts "matttbe@gmail.com"

# Install pdnsd
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends -y python3 python3-pymongo git openssh-client
RUN git clone https://github.com/MPTCP-smartphone-thesis/server-collect-mpctrl.git

EXPOSE 1234

ENTRYPOINT ["/server-collect-mpctrl/server.py"]
