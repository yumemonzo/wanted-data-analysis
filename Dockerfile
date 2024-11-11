FROM ubuntu:22.04
WORKDIR /usr/src
RUN apt update && apt upgrade -y

# 필요한 패키지 설치
RUN apt install -y wget unzip vim python3 python3-pip python3-dev build-essential \
                   sudo default-jdk git libcairo2-dev pkg-config

RUN python3 -m pip install --upgrade pip setuptools wheel
RUN pip3 install selenium

# Chrome 설치
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt -y install ./google-chrome-stable_current_amd64.deb
RUN wget https://storage.googleapis.com/chrome-for-testing-public/130.0.6723.91/linux64/chromedriver-linux64.zip
RUN mkdir chrome
RUN unzip /usr/src/chromedriver-linux64.zip
RUN rm google-chrome-stable_current_amd64.deb
RUN rm /usr/src/chromedriver-linux64.zip
RUN mv /usr/src/chromedriver-linux64/chromedriver /usr/src/chrome
RUN rm -rf chromedriver-linux64
RUN chmod +x /usr/bin/google-chrome && \
    chmod +x /usr/src/chrome/chromedriver

# 나눔고딕 폰트 설치
wget http://cdn.naver.com/naver/NanumFont/fontfiles/NanumFont_TTF_ALL.zip
wget https://github.com/naver/nanumfont/releases/download/VER2.5/NanumGothicCoding-2.5.zip
unzip NanumFont_TTF_ALL.zip
unzip NanumGothicCoding-2.5.zip

# install system-wide (or ~/.local/share/fonts for user-wide)
sudo mkdir -p /usr/share/fonts/truetype/nanum-gothic
sudo mv *.ttf /usr/share/fonts/truetype/nanum-gothic

# check
fc-list | grep -i nanum

# 프로젝트 클론 및 의존성 설치
RUN git clone https://github.com/yumemonzo/wanted_data_analysis.git
RUN pip3 install -r /usr/src/wanted_data_analysis/requirements.txt