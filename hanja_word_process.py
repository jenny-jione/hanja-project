# 크롤링된 한자 데이터 후처리 (2025.7.19)
# word_data_nw.csv -> word_data_nw_processed.csv 
#
# 원본 데이터 예시 (중복 및 포함 관계로 비슷한 단어들이 많음):
# 감격(感激)
# 감격성(感激性)
# 감격적(感激的)
#
# 격동(激動)
# 격동기(激動期)
# 격동적(激動的)
#
# 격려(激勵)
# 격려금(激勵金)
# 격려문(激勵文)
# 격려사(激勵辭)
# 격려전(激勵電)
#
# 원하는 결과:
# 감격(感激)
# 격동(激動)
# 격려(激勵)
#
# => 포함되는 단어는 제거하여 가장 기본 단어만 남김

# + 加,運動 -> 같은 데이터가 있음. 等加速度 運動 에서 공백으로 분리되어서 남은듯. 이런 데이터도 삭제.


import csv
import logging

# Logger 설정
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


def load_hanja_chars(file_path: str):
    with open(file_path, 'r', encoding='utf-8') as f:
        rdr = csv.reader(f)
        data = [row[0] for row in rdr]
    return data


def load_word_data(file_path: str):
    with open(file_path, 'r', encoding='utf-8') as f:
        rdr = csv.reader(f)
        data = list(rdr)
    return data


def save_to_csv(data: list, file_path: str):
    with open(file_path, 'w', newline='', encoding='utf-8') as f:
        wr = csv.writer(f)
        wr.writerows(data)
    logger.info(f"{len(data):,}개 데이터를 '{file_path}'에 저장했습니다.")


def clean_and_filter(crawled_data: list):
    logger.info("단어 정제 및 필터링 시작")

    processed_data = []

    prev_hanja = None
    base_words = set()

    for hanja, word in crawled_data:
        if hanja != prev_hanja:
            base_words = set()
            prev_hanja = hanja
        
        # 한글자 단어는 저장하지 않음
        if len(word) == 1:
            continue

        # 해당 한자를 포함하지 않는 단어도 저장하지 않음 (잘못 크롤링된 데이터)
        if hanja not in word:
            continue

        # base_words에 포함된 단어가 현재 word에 포함되어 있으면 중복 처리(스킵)
        if any(base_word in word for base_word in base_words):
            continue

        base_words.add(word)
        processed_data.append([hanja, word])
    
    logger.info(f"필터링 완료: {len(processed_data):,}개 단어 추출")

    return processed_data


def filter_level3_words(processed_data: list, hanja_list: list):
    logger.info("3급 한자 단어 필터링 시작")
    result = []

    for row in processed_data:
        if len(row) < 2:
            logger.warning(f"열이 부족한 행 건너뜀: {row}")
            continue  # skip rows with insufficient columns
        hanja, word = row[0], row[1]
        
        if any(ch not in hanja_list for ch in word):
            continue  # skip if any character in word is not in the hanja list
        
        result.append([hanja, word])

    logger.info(f"필터링 완료: {len(result):,}개 3급 한자 단어 추출됨")
    return result


def extract_unique_words(data: list[str]) -> list[str]:
    seen = set()
    unique_words = []
    for _, word in data:
        if word not in seen:
            seen.add(word)
            unique_words.append(word)
    return unique_words


if __name__=='__main__':
    logger.info("=== 3급 한자 단어 처리 시작 ===")

    file_name = 'word_data'
    csv_dir = './csv'
    input_file = f'{csv_dir}/{file_name}.csv'
    output_file = f'{csv_dir}/{file_name}_1_processed.csv'
    output_file2 = f'{csv_dir}/{file_name}_2_level3_words.csv'
    output_file3 = f'{csv_dir}/{file_name}_3_unique_words.csv'

    # Step 1: Load word_data.csv
    word_data = load_word_data(input_file)
    logger.info(f"원시 데이터 로드 완료: {len(word_data):,}개")

    # Step 2: 정제 및 파생어 제거
    processed_data = clean_and_filter(word_data)
    save_to_csv(processed_data, output_file)

    # Step 3: 순수 3급 한자 단어 필터링
    hanja_chars = load_hanja_chars("./csv/hanja.csv")
    level3_only = filter_level3_words(processed_data, hanja_chars)
    save_to_csv(level3_only, output_file2)

    # Step 4: 중복 단어 제거
    unique_words = extract_unique_words(level3_only)
    unique_word_rows = [[word] for word in unique_words]
    save_to_csv(unique_word_rows, output_file3)
    
    logger.info("=== 전체 처리 완료 ===")
