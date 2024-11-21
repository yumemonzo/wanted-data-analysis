FROM ubuntu:22.04
WORKDIR /usr/src
RUN apt update && apt upgrade && apt install -y wget unzip vim python3 python3-pip build-essential sudo default-jdk git libcairo2-dev pkg-config
RUN python3 -m pip install --upgrade pip setuptools wheel

RUN wget http://cdn.naver.com/naver/NanumFont/fontfiles/NanumFont_TTF_ALL.zip
RUN wget https://github.com/naver/nanumfont/releases/download/VER2.5/NanumGothicCoding-2.5.zip
RUN unzip NanumFont_TTF_ALL.zip
RUN unzip NanumGothicCoding-2.5.zip

RUN sudo mkdir -p /usr/share/fonts/truetype/nanum-gothic
RUN sudo mv *.ttf /usr/share/fonts/truetype/nanum-gothic

RUN git clone https://github.com/yumemonzo/wanted_data_analysis.git
RUN pip3 install -r /usr/src/wanted_data_analysis/requirements.txt