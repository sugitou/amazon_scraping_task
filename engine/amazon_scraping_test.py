from engine.amazon_scraping import *

def test_fetch_item():
    amazon = AmazonScraping()
    item = amazon.fetch_item('aaaafs')
    # クラスの中身を全部見れる
    print(item.__dict__)
    # 存在チェック
    assert item.name

def test_fetch_ranking_items():
    amazon = AmazonScraping()
    items = amazon.fetch_ranking_items('https://www.amazon.co.jp/gp/bestsellers/hobby', 5)

    assert len(items) == 5
    assert items[0].name