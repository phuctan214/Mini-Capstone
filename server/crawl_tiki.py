import requests
import json
import re

headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/100.0.4896.127 Safari/537.36"}

regex_find_id_product = r"-p[0-9]+.html"
info_pro_url = "https://tiki.vn/api/v2/products/{}"
comment_url = "https://tiki.vn/api/v2/reviews?product_id={}&limit={}"

def get_id_product_from_url(url: str):
    str_contain_id = re.findall(regex_find_id_product, url)
    str_contain_id = str_contain_id[0]
    id_product = re.findall(pattern=r"[0-9]+", string=str_contain_id)
    return id_product[0]


def get_comment(url: str):
    total_comment = []
    id_product = get_id_product_from_url(url)
    response_info = requests.get(info_pro_url.format(id_product), headers= headers)
    info_pro = json.loads(response_info.content)
    review_count = info_pro['review_count']
    response_comment = requests.get(comment_url.format(id_product, review_count), headers= headers)
    if response_comment.status_code == 200:
        total_meta_comment = json.loads(response_comment.content)['data']
        for meta_comment in total_meta_comment:
            total_comment.append(meta_comment["content"])

    total_comment = [cmt for cmt in total_comment if cmt != ""]
    return total_comment

