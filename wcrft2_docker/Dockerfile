################################################
#  NLP Tools for Polish from G4.19 Group
#  Wroclaw University of Science and Technology
#
#  Contact: Tomasz.Walkowiak@pwr.edu.pl
#  
#  WCRFT2 service   
###############################################

FROM ubuntu:16.04

RUN apt-get update  && \
   apt-get install -y apt-utils && \
   apt-get install -y iputils-ping && \
   apt-get install -y git  &&  \
   apt-get install -y subversion  &&  \
   apt-get install -y wget nano mc zip unzip && \  
   apt-get install -y vim ranger atool htop curl && \
   apt-get install -y locales locales-all   && \
   apt-get install -y python-dev && \
   apt-get install -y python-pip && \
   apt-get install -y cmake && \
   apt-get install -y g++  && \
   apt-get install -y netcat && \
   apt-get install -y swig 
        
RUN pip2 install --upgrade pip

##################################
## UTF-8
##################################
RUN locale-gen en_US.UTF-8
ENV LANG       en_US.UTF-8
ENV LC_ALL     en_US.UTF-8



##################################
# Install WCRFT2 + dependencies
##################################
RUN mkdir /home/install
WORKDIR /home/install  
  
RUN apt-get install -y libboost-all-dev libicu-dev libxml++2.6-dev bison flex libloki-dev

##CORPUS2
RUN git clone http://nlp.pwr.edu.pl/corpus2.git && \
        cd corpus2 && \
        mkdir bin &&\
        cd bin && \
        cmake -D CORPUS2_BUILD_POLIQARP:BOOL=True .. && \
        make -j4 && \
        make -j4 && \
        make install && \
        ldconfig
##WCCL
RUN apt-get update && apt-get install -y libantlr-dev && \
        git clone -b mwe_fix http://nlp.pwr.edu.pl/wccl.git && \
        cd wccl && \
        mkdir bin && \
        cd bin && \
        cmake .. && \
        make -j4 && \
        #Error after 1st “make”? Why after running “make” again everything goes OK?
        make -j4 && \
        make install && \
        ldconfig

##CORPUS2MWE (??)
RUN cd corpus2/corpus2mwe && \
      	mkdir build && \
      	cd build && \
      	cmake .. && \
      	make -j4 && \
      	make install && \
      	ldconfig

##TOKI
RUN git clone http://nlp.pwr.edu.pl/toki.git  && \
        cd toki && \
        mkdir bin && \
        cd bin && \
        cmake .. && \
        make -j4 && \
        make install && \
        ldconfig

##morfeusz-sgjp
RUN mkdir morfeusz-sgjp  && \
        cd morfeusz-sgjp && \
        wget http://download.sgjp.pl/morfeusz/older/morfeusz1/morfeusz-SGJP-linux64-20130413.tar.bz2  && \
        tar -jxvf morfeusz-SGJP-linux64-20130413.tar.bz2 && \
        mv libmorfeusz* /usr/local/lib/ && \
        mv morfeusz /usr/local/bin/ && \
        mv morfeusz.h /usr/local/include/ && \
        ldconfig && \
        cd .. && \
        rm -rf morfeusz-sgjp

## Morfeusz2
RUN mkdir morfeusz  && cd morfeusz && \
    wget -O morfeusz2-2.0.0-Linux-amd64.deb https://nextcloud.clarin-pl.eu/index.php/s/VVIvx4w20azcWbp/download && \
    dpkg -i --instdir=/home/install/morfeusz morfeusz2-2.0.0-Linux-amd64.deb && \
    ln /home/install/morfeusz/usr/include/morfeusz2.h /home/install/morfeusz/usr/include/morfeusz.h && \
    dpkg -i morfeusz2-2.0.0-Linux-amd64.deb && \
    ln /usr/include/morfeusz2.h /usr/include/morfeusz.h && \
    rm -rf ../morfeusz        
        
##MACA     
RUN apt-get install -y build-essential subversion libedit-dev libreadline-dev libsfst1-1.4-dev  && \
        git clone http://nlp.pwr.edu.pl/maca.git && \
        cd maca && \
        mkdir bin && \
        cd bin && \
        cmake .. && \
        make -j4 && \
        make install && \
        ldconfig


##CRF++      
RUN wget -O download 'https://drive.google.com/uc?authuser=0&id=0B4y35FiV1wh7QVR6VXJ5dWExSTQ&export=download' && \
        tar -xvzf download && \
        rm download && \
        cd CRF++-0.58/ && \
        ./configure && \
        make && \
        make install && \
        ldconfig 


##WCRFT2    
RUN  git clone http://nlp.pwr.edu.pl/wcrft2.git && \
     cd wcrft2 && \
     mkdir bin && \
     cd bin && \
     cmake .. && \
        make -j4 && \
        make install && \
        ldconfig
