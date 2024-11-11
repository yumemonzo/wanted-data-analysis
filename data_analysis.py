import os
import re
import yaml
import folium
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from wordcloud import WordCloud
import matplotlib.font_manager as fm
from konlpy.tag import Okt

okt = Okt()
os.makedirs('./figure', exist_ok=True)
plt.rcParams["font.family"] = 'NanumGothic'


def location_analysis(df, config):
    """위치 데이터를 분석하여 빈도 그래프와 지도에 표시"""
    df['위치'] = df['위치'].str.replace(" ", "")
    location_counts = df['위치'].value_counts()
    
    # 위치별 빈도수 그래프 생성
    plt.figure(figsize=(10, 6))
    location_counts.sort_values(ascending=False).plot(kind='bar')
    plt.title('위치별 빈도수')
    plt.xlabel('위치')
    plt.ylabel('빈도수')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig('./figure/location.jpg')
    
    # 위치별 빈도를 지도에 표시
    location_data = config['location_data']
    m = folium.Map(location=[35.1796, 129.0756], zoom_start=7)
    for location, count in location_counts.items():
        if location in location_data:
            lat, lon = location_data[location]
            folium.CircleMarker(
                location=[lat, lon],
                radius=count * 2,
                color='blue',
                fill=True,
                fill_color='blue',
                fill_opacity=0.6,
                tooltip=f"{location}: {count}개"
            ).add_to(m)
    m.save("./app/location_map.html")


def preprocess_career(text):
    """경력 데이터를 전처리하여 신입은 '1'로, 나머지 숫자만 남김"""
    text = re.sub(r'신입', '1', str(text))
    text = re.sub(r'[^0-9-]', '', text).strip().strip('-')
    return text


def career_analysis(df):
    """경력 데이터를 분석하여 경력 구간별 빈도 그래프 생성"""
    preprocessed_career = df['경력'].apply(preprocess_career)
    experience_list = []
    
    for experience in preprocessed_career:
        if experience:
            if '-' in experience:
                start, end = experience.split('-')
                experience_list.extend(range(int(start), int(end) + 1))
            else:
                experience_list.append(int(experience))

    experience_counts = pd.Series(experience_list).value_counts().sort_values(ascending=False)
    colors = plt.cm.rainbow(np.linspace(1, 0, len(experience_counts)))
    
    plt.figure(figsize=(12, 8))
    plt.bar(experience_counts.index.astype(str), experience_counts.values, color=colors, edgecolor="black", alpha=0.8)
    plt.title('경력 구간별 빈도수', fontsize=16)
    plt.xlabel('경력 (년)', fontsize=14)
    plt.ylabel('빈도수', fontsize=14)
    plt.tight_layout()
    plt.savefig('./figure/career.jpg')


class TextPreProcessing:
    def __init__(self, df, config, config_section):
        self.df = df.copy()
        self.stopwords = config['text_preprocessing'][config_section]['stopwords']
        self.keep_phrases = config['text_preprocessing'][config_section]['keep_phrases']

    def clean_text(self, text):
        return re.sub(r'[^가-힣\s]', '', text)

    def remove_konlpy_stopwords(self, text):
        words = okt.pos(text, norm=True, stem=True)
        processed_words, skip = [], False
        for i, (word, pos) in enumerate(words):
            if skip:
                skip = False
                continue
            if i < len(words) - 1 and f"{word}{words[i + 1][0]}" in self.keep_phrases:
                processed_words.append(f"{word}{words[i + 1][0]}")
                skip = True
            elif pos not in ['Josa', 'Eomi', 'Punctuation']:
                processed_words.append(word)
        return ' '.join(processed_words)

    def remove_custom_stopwords(self, text):
        return ' '.join([word for word in text.split() if word not in self.stopwords])

    def remove_final_da(self, text):
        return ' '.join([word for word in text.split() if not word.endswith('다')])

    def preprocessing(self, file_path=None):
        processed_text = '\n'.join([
            self.remove_custom_stopwords(
                self.remove_final_da(
                    self.remove_konlpy_stopwords(
                        self.clean_text(text)
                    )
                )
            ) for text in self.df
        ])
        if file_path:
            with open(file_path, 'w') as file:
                file.write(processed_text)
        return processed_text


def generate_circular_wordcloud(word_frequencies, width=300, height=300, circle_radius=140, file_name='unknown'):
    width, height = int(width), int(height)
    font_path = next((font.fname for font in fm.fontManager.ttflist if 'Nanum' in font.name), None)
    if not font_path:
        raise RuntimeError("한글 폰트를 찾을 수 없습니다. 시스템에 한글 폰트를 설치하세요.")

    y, x = np.ogrid[:height, :width]
    mask = (x - width // 2) ** 2 + (y - height // 2) ** 2 > circle_radius ** 2
    mask = 255 * mask.astype(int)

    wordcloud = WordCloud(font_path=font_path, width=width, height=height,
                          background_color='white', mask=mask,
                          color_func=lambda *args, **kwargs: (0, 0, 255)).generate_from_frequencies(word_frequencies)

    plt.figure(figsize=(8, 8))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.savefig(f'./figure/{file_name}_wordcloud.jpg')


def plot_word_frequencies(word_list, word_counts, title, file_name):
    colors = plt.cm.rainbow(np.linspace(1, 0, len(word_list)))
    plt.figure(figsize=(12, 8))
    plt.bar(word_list, word_counts, color=colors, width=0.6)
    plt.title(title)
    plt.xlabel("단어")
    plt.xticks(rotation=0)
    plt.ylabel("빈도수")
    plt.savefig(f'./figure/{file_name}_freq_bar_graph.jpg')


def main():
    # Load configuration
    with open("./config/data_analysis.yaml", "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    # Load data
    df = pd.read_csv('./data/crawled_data.csv')
    
    # 위치 분석
    location_analysis(df, config)
    
    # 경력 분석
    career_analysis(df)
    
    # 주요 업무, 자격 요건, 우대 사항 텍스트 분석
    for ko_section, en_section in zip(["주요업무", "자격요건", "우대사항"], ["main_job","check_list", "good_list"]):
        text_processor = TextPreProcessing(df[ko_section], config, en_section)
        processed_text = text_processor.preprocessing()

        words = processed_text.split()
        word_counts = Counter(words)
        top_20_words = word_counts.most_common(20)
        words, counts = zip(*top_20_words)

        generate_circular_wordcloud(dict(top_20_words), file_name=en_section)
        plot_word_frequencies(words, counts, f"{ko_section} 상위 20개 단어 빈도수", en_section)

if __name__ == "__main__":
    main()
