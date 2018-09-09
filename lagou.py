import pymongo
import requests
from requests.exceptions import RequestException

def get_page(pn):
    url = "https://www.lagou.com/jobs/positionAjax.json?px=default&needAddtionalResult=false"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3423.2 Safari/537.36",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Host": "www.lagou.com",
        "Origin": "https://www.lagou.com",
        "Referer": "https://www.lagou.com/jobs/list_python?px=default&city=%E5%B9%BF%E5%B7%9E",
        "Cookie": "JSESSIONID=ABAAABAABEEAAJAED90BA4E80FADBE9F613E7A3EC91067E; _ga=GA1.2.1013282376.1527477899; user_trace_token=20180528112458-b2b32f84-6226-11e8-ad57-525400f775ce; LGUID=20180528112458-b2b3338b-6226-11e8-ad57-525400f775ce; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1527346927,1527406449,1527423846,1527477899; _gid=GA1.2.1184022975.1527477899; index_location_city=%E5%85%A8%E5%9B%BD; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1527487349; LGSID=20180528140228-b38fe5f2-623c-11e8-ad79-525400f775ce; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fwww.lagou.com%2Fzhaopin%2FPython%2F%3FlabelWords%3Dlabel; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_Python%3Fpx%3Ddefault%26city%3D%25E5%25B9%25BF%25E5%25B7%259E; TG-TRACK-CODE=index_search; _gat=1; LGRID=20180528141611-9e278316-623e-11e8-ad7c-525400f775ce; SEARCH_ID=42c704951afa48b5944a3dd0f820373d"
    }

    data={
        'first': 'false',
        'pn': pn,
        'kd': '爬虫'
    }
    try:
        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            return response.json()
        return None
    except RequestException as e:
        print(e)

def parse_page(response):
    response = response.get('content').get('positionResult').get('result')
    for item in response:
        yield{
        'adWord':item['adWord'],
        'appShow':item['appShow'],
        'approve':item['approve'],
        'businessZones':item['businessZones'],
        'city':item['city'],
        'companyFullName':item['companyFullName'],
        'companyId':item['companyId'],
        'companyLabelList':item['companyLabelList'],
        'companyLogo':item['companyLogo'],
        'companyShortName':item['companyShortName'],
        'companySize':item['companySize'],
        'createTime':item['createTime'],
        'deliver':item['deliver'],
        'district':item['district'],
        'education':item['education'],
        'explain':item['explain'],
        'financeStage':item['financeStage'],
        'firstType':item['firstType'],
        'formatCreateTime':item['formatCreateTime'],
        'gradeDescription':item['gradeDescription'],
        'hitags':item['hitags'],
        'imState':item['imState'],
        'industryField':item['industryField'],
        'industryLables':item['industryLables'],
        'isSchoolJob':item['isSchoolJob'],
        'jobNature':item['jobNature'],
        'lastLogin':item['lastLogin'],
        'latitude':item['latitude'],
        'linestaion':item['linestaion'],
        'longitude':item['longitude'],
        'pcShow':item['pcShow'],
        'plus':item['plus'],
        'positionAdvantage':item['positionAdvantage'],
        'positionId':item['positionId'],
        'positionLables':item['positionLables'],
        'positionName':item['positionName'],
        'promotionScoreExplain':item['promotionScoreExplain'],
        'publisherId':item['publisherId'],
        'resumeProcessDay':item['resumeProcessDay'],
        'resumeProcessRate':item['resumeProcessRate'],
        'salary':item['salary'],
        'score':item['score'],
        'secondType':item['secondType'],
        'stationname':item['stationname'],
        'subwayline':item['subwayline'],
        'workYear':item['workYear'],
        }


def write_to_mongo(item):
    client = pymongo.MongoClient('localhost',27017)
    db = client['jobs']
    collection = db['spider']
    collection.insert(item)


def main():
    for pn  in range(1,31):
        response = get_page(pn)
        for item in parse_page(response):
            write_to_mongo(item)

if __name__ == '__main__':
    main()
