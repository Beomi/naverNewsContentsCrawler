import os
from pprint import pprint
import json
import requests
from bs4 import BeautifulSoup as bs

import boto3

s3 = boto3.client('s3')

headers = {
    'authority': 'news.naver.com',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'dnt': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7,la;q=0.6,da;q=0.5',
}


def get_news(oid, aid):
    params = (
        ('oid', oid),
        ('aid', aid),
    )
    url = 'https://news.naver.com/main/tool/print.nhn'
    response = requests.get(
        'https://news.naver.com/main/tool/print.nhn',
        headers=headers, params=params
    )
    soup = bs(response.text, 'html.parser')

    title = soup.select_one('h3.font1').text
    contents = soup.select_one('div.article_body').text

    try:
        created_at = soup.select_one(
            'body > table > tbody > tr > td > div.content > div.article_header > div > span:nth-of-type(1)').text
        updated_at = soup.select_one(
            'body > table > tbody > tr > td > div.content > div.article_header > div > span:nth-of-type(2)').text
    except AttributeError:
        created_at = soup.select_one(
            'div.sponsor > span.t11').text
        updated_at = created_at

    result = dict(
        title=title,
        created_at=created_at,
        updated_at=updated_at,
        contents=contents.strip(),
    )

    year, month, day = created_at.split(' ')[0].split('-')

    response = s3.put_object(
        Body=json.dumps(result),
        Bucket=os.environ['S3_BUCKET'],
        Key=f'json/{year}/{month}/{day}/{oid}/{aid}.json',
    )

    return result


if __name__ == '__main__':
    result = get_news('001', '0010339290')
    pprint(result)
