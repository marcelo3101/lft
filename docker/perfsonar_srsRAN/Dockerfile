#
# Copyright (C) 2022 Alexandre Mitsuru Kaihara
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#


FROM ubuntu:20.04

# Basic depencencies needed for network debugging inside a container
RUN apt update \
&&  RUNLEVEL=1 apt install -y --no-install-recommends sudo net-tools iproute2 iputils-ping iptables nano software-properties-common curl wget unzip iperf3

# Install perfsonar-testpoint
RUN apt install -y software-properties-common gpg-agent && \
        cd /etc/apt/sources.list.d/ && \
        curl -o perfsonar-release.list http://downloads.perfsonar.net/debian/perfsonar-release.list && \
        curl http://downloads.perfsonar.net/debian/perfsonar-official.gpg.key | tac | tac | apt-key add - && \
        apt update && \
        echo -e "yes\n2\nperfsonar\nperfsonar\n" | apt install -y perfsonar-testpoint

# Install srsRAN
## Cloning repository
RUN wget https://github.com/srsran/srsRAN_4G/archive/refs/heads/master.zip
RUN unzip master.zip && \
        mv srsRAN_4G-master srsRAN

## Instaling dependencies
RUN apt-get update -y && \
	apt-get install -y cmake \
	libfftw3-dev \
	libmbedtls-dev \
	libboost-program-options-dev \
	libconfig++-dev \
	libsctp-dev \
	libzmq3-dev \
	build-essential \
        gnuradio

## Building srsRAN
RUN mkdir /srsRAN/build && \
    cd /srsRAN/build && \
    cmake ../ && make && make install && ldconfig && \
   ./srsran_install_configs.sh service

## Adding configuration Files
RUN mkdir /etc/srsRAN && \ 
    cp /srsRAN/srsue/ue.conf.example /etc/srsran/ue.conf && \
    cp /srsRAN/srsenb/enb.conf.example /etc/srsran/enb.conf && \
    cp /srsRAN/srsenb/rb.conf.example /etc/srsran/rb.conf && \
    cp /srsRAN/srsenb/rr.conf.example /etc/srsran/rr.conf && \
    cp /srsRAN/srsenb/sib.conf.example /etc/srsran/sib.conf && \
    cp /srsRAN/srsepc/epc.conf.example /etc/srsran/epc.conf && \
    cp /srsRAN/srsepc/user_db.csv.example /etc/srsran/user_db.csv && \
    > /etc/srsran/user_db.csv
COPY onboot.sh /srsRAN/build/
COPY multiUE.py /srsRAN/build/
RUN chmod +x /srsRAN/build/onboot.sh
CMD ["./srsRAN/build/onboot.sh"] 

# For conecting via Open SSL
EXPOSE 22

