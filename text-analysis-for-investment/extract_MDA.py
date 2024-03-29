import glob
import json
import re
from multiprocessing import Pool

def read_txt_file(file_path: str) -> tuple:
    """get the content and basic information of the txt file 

    Args:
        file_path (str): the path of the txt file 

    Returns:
        tuple: (list, str, str) 
    """
    with open(file_path, 'r') as file:
        content = file.readlines()
        company_name = file_path.split('/')[-1].split('_')[0]
        year = file_path.split('/')[-1].split('_')[1]
        return content, company_name, year


def is_keyword_position(keyword, content: str) -> bool:
    """judge whether MD&A keyword is in the content

    Args:
        keyword (str/list): ['管理层讨论与分析', '经营情况讨论与分析'] or '董事会报告'
        content (str): content of a line in annual report
    """
    exception_words = ['查阅', '本报告', '详见', '请']
    for exception_word in exception_words:
        if exception_word in content:
            return False
    # case keyword = ['管理层讨论与分析', '经营情况讨论与分析']
    if isinstance(keyword, list):
        for key in keyword:
            if key in content:
                return True
    # case keyword = '董事会报告'
    elif keyword in content:
        return True
    return False


def get_mda_position(content: list, keyword):
    keyword_position = []
    catalog_position = None
    for info in content:
        info = json.loads(info)
        if info == {}:
            continue
        if info['type'] == 'text':
            if '目录' in info['inside'] and not catalog_position:
                catalog_position = info['allrow']
                continue
            if is_keyword_position(keyword, info['inside']):
                # print(info['inside'])
                keyword_position.append(info['allrow'])

    # if there is not catalog in the txt, give it up
    if not catalog_position:
        return 0, 0

    end = 0
    start = None
    if keyword_position:
        if len(keyword_position) > 2:
            for position in keyword_position:
                if position - catalog_position > 20:
                    start = position
                    break
            if not start:
                start = keyword_position[1]
        else:
            start = keyword_position[-1]
    else:
        # if there is no keyword, give it up
        start = end
        return start, end
    # print(start)
    pattern = r"([\u4e00-\u9fa5]+[、节章].*?)(?=[·.…]|$)"
    chapter_line = json.loads(content[keyword_position[0] + 1])['inside']
    next_chapter_name = (
        re.match(pattern, chapter_line)[1]
        if re.match(pattern, chapter_line)
        else None
    )
    # print(next_chapter_name)
    if next_chapter_name:
        for info in content:
            info = json.loads(info)
            if info == {}:
                continue
            if next_chapter_name in info['inside'] and info['allrow'] - catalog_position > 20 and info['allrow'] > start:
                # print(info)
                end = info['allrow']
    else:
        # if there is no next chapter name, give it up
        end = start
    # print(end)
    return start, end


def get_mda_content(content: list, start: int, end: int):
    mda_content = ''
    for info in content[start+1:end]:
        info = json.loads(info)
        # we only need text
        if info['type'] == 'text':
            mda_content = mda_content + info['inside']
    return mda_content



def extract_MDA(file_path):
    save_path = './mdatxts/' + file_path.split('/')[-1]
    print(save_path)
    content, company_name, year = read_txt_file(file_path)
    keyword = '董事会报告' if int(year) < 2015 else ['管理层讨论与分析', '经营情况讨论与分析']
    start, end = get_mda_position(content, keyword)
    mda_content = get_mda_content(content, start, end)
    with open(save_path, 'w', encoding='utf-8')as f:
        f.write(mda_content)


def main():
    txt_folder_path = './rawtxts'
    txt_files = glob.glob(f'{txt_folder_path}/*.txt')
    txt_files = sorted(txt_files, reverse=True)
    with Pool(processes=10) as pool:
        results = pool.map(extract_MDA, txt_files)
    for file in txt_files:
        extract_MDA(file)
    # extract_MDA('./rawtxts/招商银行_2011_年报.txt') # test example

if __name__ == '__main__':
    main()