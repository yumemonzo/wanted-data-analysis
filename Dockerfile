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
RUN rm google-chrome-stable_current_amd64.deb

# ChromeDriver 설치
RUN wget https://storage.googleapis.com/chrome-for-testing-public/130.0.6723.91/linux64/chromedriver-linux64.zip
RUN unzip chromedriver-linux64.zip -d /usr/src/chrome
RUN chmod +x /usr/bin/google-chrome /usr/src/chrome/chromedriver
RUN rm chromedriver-linux64.zip

# 프로젝트 클론 및 의존성 설치
RUN git clone https://github.com/yumemonzo/wanted_data_analysis.git
RUN pip3 install -r /usr/src/wanted_data_analysis/requirements.txt
