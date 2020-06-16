import scrapy
from pachonglianjia.items import PachonglianjiaItem

# quyu = {'jinjiang':'锦江',
#                'qingyang':'青羊',
#                'wuhou':'武侯',
#                'gaoxin7':'高新',
#                'chenghua':'成华',
#                'jinniu':'金牛',
#                'tianfuxinqu':'天府新区',
#                'gaoxinxi1':'高新西',
#                'shuangliu':'双流',
#                'wenjiang':'温江',
#                'pidou':'郫都',
#                'longquanyi': '龙泉驿',
#                'xindou': '新都',
#                'tianfuxinqunaqu': '天府新区南区',
#                'qingbaijiang': '青白江',
#                'dujiangyang': '都江堰',
#                'pengzhou': '彭州',
#                'jianyang': '简阳',
#                'xinjin': '新津',
#                'chongzhou1': '崇州',
#                'dayi': '大邑',
#                'jintang': '金堂',
#                'pujiang': '蒲江',
#                'qionglai': '邛崃'}

region = ['qingyang','wuhou','gaoxin7','gaoxin7','chenghua','jinniu','tianfuxinqu','gaoxinxi1','shuangliu','wenjiang',
          'pidou','longquanyi','xindou','tianfuxinqunaqu','qingbaijiang','doujiangyang','pengzhou','jianyang','xinjin',
          'chongzhou1','dayi','jintang','pujiang','qionglai']


class pachonglianjia(scrapy.Spider):
    name = 'pachonglianjia'
    start_urls = ['https://cd.lianjia.com/ershoufang/']

    # 获取不同区域的URL，并访问，利用parse_region函数处理页面
    # def parse(self, response):
    #     url_regions = response.xpath("//div[@data-role='ershoufang']/div/a/@href").extract()
    #     for i in url_regions:
    #         region_url = "https://cd.lianjia.com{0}".format(str(i))
    #         yield scrapy.Request(region_url, callback=self.parse_region)

    # 获取当前页面的不同房子的URL，并访问，利用parse_one函数处理页面
    def parse(self, response):
        # 获取当前页面不同房子的URL
        next_regions = response.xpath("//ul[@class='sellListContent']/li/a/@href").extract()
        for next_region in next_regions:
            yield scrapy.Request(next_region, callback=self.parse_one)
            # 获取当前区域100页的url
            for n in range(0, 24):
                for i in range(1, 101):
                    link = 'https://cd.lianjia.com/ershoufang/' + region[n] + '/pg' + str(i)
                    yield scrapy.Request(link, callback=self.parse)

    # 获取当前页面的所需属性值
    def parse_one(self, response):

        item = PachonglianjiaItem()

        district = response.xpath(
            '//div[@class="aroundInfo"]/div[@class="areaName"]/span[@class="info"]/a[1]/text()').extract_first()
        region = response.xpath(
            '//div[@class="houseInfo"]/div[@class="type"]/div[@class="mainInfo"]/text()').extract_first()
        elevator = response.xpath(
            '//div[@class="introContent"]/div[@class="base"]/div[@class="content"]/ul/li[11]/text()').extract_first()
        floor = response.xpath(
            '//div[@class="introContent"]/div[@class="base"]/div[@class="content"]/ul/li[2]/text()').extract_first()
        id = response.xpath('//div[@class="houseRecord"]/span[@class="info"]/text()').extract_first()
        layout = response.xpath(
            '//div[@class="houseInfo"]/div[@class="room"]/div[@class="mainInfo"]/text()').extract_first()
        price = response.xpath(
            '//div[@class="content"]/div[@class="price "]/span[@class="total"]/text()').extract_first()
        renovation = response.xpath(
            '//div[@class="introContent"]/div[@class="base"]/div[@class="content"]/ul/li[9]/text()').extract_first()
        size = response.xpath(
            '//div[@class="introContent"]/div[@class="base"]/div[@class="content"]/ul/li[3]/text()').extract_first()
        year = response.xpath(
            '//div[@class="houseInfo"]/div[@class="area"]/div[@class="subInfo"]/text()').extract_first().split('/')[0]

        # 区
        item['district'] = district
        # 房屋朝向
        item['region'] = region
        # 是否配备电梯
        item['elevator'] = elevator
        # 所在楼层
        item['floor'] = floor
        # 链家编号
        item['id'] = id
        # 房屋户型
        item['layout'] = layout
        # 房屋价格（单位：万）
        item['price'] = price
        # 装修类型
        item['renovation'] = renovation
        # 建筑面积
        item['size'] = size
        # 修建时间
        item['year'] = year

        yield item