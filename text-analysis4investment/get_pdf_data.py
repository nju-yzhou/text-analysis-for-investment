import os.path
import requests
from shreport import SH
import pandas as pd
from tqdm import trange


def get_pdf_links(cookie, pdf_link_path):
    """using shreport to get all the pdf links

    Args:
        cookie (str): your cookie for the website
        pdf_link_path (str): the path of the file you want to save the links

    Returns:
        pdf_link: dataframe 6 columns "company_name, company_id, type, year, date, pdf_link"
    """
    # get all the company ids 
    cookies = {"Cookie": cookie}
    sh = SH(cookies)
    company_ids = sh.companys()
    
    # init pdf_links
    if os.path.exists(pdf_link_path):
        pdf_links = pd.read_csv(pdf_link_path, encoding='utf-8')
    else:
        pdf_links = pd.DataFrame()
        
    last_company = pdf_links.iloc[-1, 0]
    begin_position = company_ids[company_ids['name'] == last_company].index[0] + 1
    
    for company_num in trange(begin_position, company_ids.shape[0]):
        company_id = company_ids.iloc[company_num, 1]
        # There maybe some issues when we are requesting the url
        success = False
        while not success:
            try:
                company_pdf_links = sh.disclosure(company_id)
                success = True
            except Exception:
                continue
        
        # We only need "年报"
        company_pdf_links = company_pdf_links[company_pdf_links['type'] == '年报']
        pdf_links = pd.concat([pdf_links, company_pdf_links], axis=0)

    # save paf links
    pdf_links.to_csv(pdf_link_path, index=False)
    return pdf_links


def download_pdf(pdf_links, pdf_folder_path):
    """dowmload the pdf version of all the annual report

    Args:
        pdf_links (dataframe): the result of function get_pdf_links. 6 columns "company_name, company_id, type, year, date, pdf_link"
        pdf_folder_path (str): the folder you want to save the pdfs
    """
    for pdf_num in trange(pdf_links.shape[0]):
        company_name = pdf_links.iloc[pdf_num, 0]
        year = pdf_links.iloc[pdf_num, 3]
        pdf_link = pdf_links.iloc[pdf_num, 5]
        file_path = os.path.join(pdf_folder_path, f'{company_name}_{year}_年报.pdf')

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60'}
        success = False
        while not success:
            try:
                res = requests.get(pdf_link, headers=headers)
                success = True
            except Exception:
                continue
        with open(file_path, 'wb') as f:
            for chunk in res.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)


def main():
    cookie = ('') # please input your own cookie
    pdf_link_path = './pdf_links.csv'
    pdf_folder_path = './pdfs'
    pdf_links = get_pdf_links(cookie, pdf_link_path)
    download_pdf(pdf_links, pdf_folder_path)


if __name__ == '__main__':
    main()
