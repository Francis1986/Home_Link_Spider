# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from HomeLink.items import HouseInfoItem
import re

#根据行政区列表爬取对应行政区所有成交房源
class HouseinfoSpider(Spider):
    name = "houseinfo"
    allowed_domains = ["bj.lianjia.com"]
#     start_urls = ['http://bj.lianjia.com/']
    xiaoqu_url = 'http://bj.lianjia.com/xiaoqu/' 
    chengjiao_url = 'http://bj.lianjia.com/chengjiao/'
    #平谷，怀柔，密云，延庆样本量过少直接pass
    #目前已完成：东城、西城、海淀、房山（未入mongodb）、石景山、丰台,朝阳（还差6000条以后再说）、昌平（54000）
    #          、通州（差4000:珠江逸景:812、新华联家园北区:602、京贸国际城西区：502、海棠湾一期：353，蓝调沙龙东区：295，靓景明居：375，首开国风美仑：78
    #润枫领尚：92，世纪星城：1243，西马庄园：603，百合湾：237，）   、大兴（差1000左右，保利茉莉公馆：739）,顺义（28000）
    #未完成：亦庄开发区（8158）、门头沟（7415）
    #这里输入需要爬取的行政区列表，建议分批爬取，每次爬取的数量不超过10万条。
    district_list = [
             'yizhuangkaifaqu','mentougou'
#         ,'yizhuangkaifaqu','mentougou'
#         ,'pinggu','huairou','miyun','yanqing','fangshan','xicheng','haidian','dongcheng','fengtai','shijingshan','chaoyang' ,'changping'，'tongzhou','daxing' 
#           ,'shunyi' 
    ]   

    def start_requests(self):   
        for district in self.district_list:
#             print(self.main_url+district)
            yield Request(url = self.xiaoqu_url+district+"/pg1", callback = self.parse_xiaoqu_list)
#         yield Request(url = 'https://bj.lianjia.com/chengjiao/c1111027377579/', callback = self.parse_xiaoqu_chengjiao_list)
   
    def parse_xiaoqu_list(self,response):
        curPage = re.search("totalPage.*?:(.*?),.*?curPage.*?:(.*?)}", response.text, re.S).group(2)
        totalPage = re.search("totalPage.*?:(.*?),.*?curPage.*?:(.*?)}", response.text, re.S).group(1)
        xiaoqu_id_list = response.css('.listContent li::attr(data-id)').extract()
        for xiaoqu_id in xiaoqu_id_list:
            yield Request(url = self.chengjiao_url+'c'+xiaoqu_id, callback = self.parse_xiaoqu_chengjiao_list)
        if curPage != totalPage:
            next_page = int(curPage)+1
            yield Request(url = response.url.split('pg')[0]+'pg'+str(next_page), callback = self.parse_xiaoqu_list)
#         if int(curPage) <= 5:
#             next_page = int(curPage)+1
#             yield Request(url = response.url.split('pg')[0]+'pg'+str(next_page), callback = self.parse_xiaoqu_list)

    def parse_xiaoqu_chengjiao_list(self, response):
        curPage = re.search("totalPage.*?:(.*?),.*?curPage.*?:(.*?)}", response.text, re.S).group(2)
        totalPage = re.search("totalPage.*?:(.*?),.*?curPage.*?:(.*?)}", response.text, re.S).group(1)
        house_info_url_list = response.css(".listContent li .title a::attr(href)").extract()
        for house_info_url in house_info_url_list:
            yield Request(url = house_info_url, callback = self.parse_house_info)
        if curPage != totalPage:
            next_page = int(curPage)+1
            yield Request(url = response.url.split('pg')[0]+'pg'+str(next_page), callback = self.parse_xiaoqu_chengjiao_list)
        
    def parse_house_info(self, response):
        item = HouseInfoItem()
        #行政区名称
        item['district'] = response.css('.deal-bread a::text').extract()[2][0:-7]
        #行政区内区域名称
        item['district_area'] = response.css('.deal-bread a::text').extract()[3][0:-7]
        #小区名称
        item['xiaoqu'] = re.search("resblockName:'(.*?)'",response.text,re.S).group(1)
        #小区id
        item['xiaoqu_id'] = re.search("resblockId:'(.*?)'",response.text,re.S).group(1)
        #小区经度 用正则表达式解析
        item['xiaoqu_long'] = re.search("resblockPosition:'(.*?),",response.text,re.S).group(1)
        #小区纬度 用正则表达式解析
        item['xiaoqu_lat'] = re.search("resblockPosition:'.*?,(.*?)'",response.text,re.S).group(1)
        #链家ID
        item['lianjia_id'] = re.search("houseCode:'(.*?)'",response.text,re.S).group(1)
        #成交名称
        item['title'] = response.css('.wrapper::text').extract_first()
        #成交日期
        item['deal_date'] = response.css('.wrapper span::text').re('(.*) (.*)')[0]
        #成交公司
        item['deal_com'] = response.css('.wrapper span::text').re('(.*) (.*)')[1]
        #成交总价
        item['total_price'] = response.css('.price .dealTotalPrice i::text').extract_first()
        #成交单价
        item['unit_price'] = response.css('.price b::text').extract_first()
        if response.css('.info.fr .msg span label::text').extract():
            #挂牌价格
            item['list_price'] = response.css('.info.fr .msg span label::text').extract()[0]
            #成交周期
            item['deal_cycle'] = response.css('.info.fr .msg span label::text').extract()[1]
            #调价次数
            item['price_adj_num'] = response.css('.info.fr .msg span label::text').extract()[2]
            #带看次数
            item['see_num'] = response.css('.info.fr .msg span label::text').extract()[3]
            #关注人数
            item['follow_num'] = response.css('.info.fr .msg span label::text').extract()[4]
            #浏览次数
            item['view_num'] = response.css('.info.fr .msg span label::text').extract()[5]
        else:
            #挂牌价格
            item['list_price'] = ''
            #成交周期
            item['deal_cycle'] = ''
            #调价次数
            item['price_adj_num'] = ''
            #带看次数
            item['see_num'] = ''
            #关注人数
            item['follow_num'] = ''
            #浏览次数
            item['view_num'] = ''
        if response.css('.introContent .base .content ul li::text').extract():
            #户型
            item['house_type'] = response.css('.introContent .base .content ul li::text').extract()[0].strip()
            #建筑面积
            item['build_area'] = response.css('.introContent .base .content ul li::text').extract()[2].strip()
            #套内面积
            item['dwelling_area'] = response.css('.introContent .base .content ul li::text').extract()[4].strip()
            #房屋朝向
            item['orientation'] = response.css('.introContent .base .content ul li::text').extract()[6].strip()
            #装修情况
            item['decoration'] = response.css('.introContent .base .content ul li::text').extract()[8].strip()
            #供暖方式
            item['heating'] = response.css('.introContent .base .content ul li::text').extract()[10].strip()
            #产权年限
            item['property_time'] = response.css('.introContent .base .content ul li::text').extract()[12].strip()
            #所在楼层
            item['floor'] = response.css('.introContent .base .content ul li::text').extract()[1].strip()
            #户型结构
            item['house_type_str'] = response.css('.introContent .base .content ul li::text').extract()[3].strip()
            #建筑类型
            item['build_type'] = response.css('.introContent .base .content ul li::text').extract()[5].strip()
            #建筑年代
            item['build_year'] = response.css('.introContent .base .content ul li::text').extract()[7].strip()
            #建筑结构
            item['build_archit'] = response.css('.introContent .base .content ul li::text').extract()[9].strip()
            #梯户比例
            item['elevator_rate'] = response.css('.introContent .base .content ul li::text').extract()[11].strip()
            #配备电梯
            item['elevator_'] = response.css('.introContent .base .content ul li::text').extract()[13].strip()
        else:
            #户型
            item['house_type'] = ''
            #建筑面积
            item['build_area'] = ''
            #套内面积
            item['dwelling_area'] = ''
            #房屋朝向
            item['orientation'] = ''
            #装修情况
            item['decoration'] = ''
            #供暖方式
            item['heating'] = ''
            #产权年限
            item['property_time'] = ''
            #所在楼层
            item['floor'] = ''
            #户型结构
            item['house_type_str'] = ''
            #建筑类型
            item['build_type'] = ''
            #建筑年代
            item['build_year'] = ''
            #建筑结构
            item['build_archit'] = ''
            #梯户比例
            item['elevator_rate'] = ''
            #配备电梯
            item['elevator_'] = ''
        if response.css('.introContent .transaction .content ul li::text').extract():
            #挂牌时间
            item['list_time'] = response.css('.introContent .transaction .content ul li::text').extract()[2].strip()
            #房屋年限
            item['house_year'] = response.css('.introContent .transaction .content ul li::text').extract()[4].strip()
            #交易权属
            item['deal_type'] = response.css('.introContent .transaction .content ul li::text').extract()[1].strip()
            #房屋用途
            item['house_usage'] = response.css('.introContent .transaction .content ul li::text').extract()[3].strip()
            #房屋权属
            item['house_owner'] = response.css('.introContent .transaction .content ul li::text').extract()[5].strip()
        else:
            #挂牌时间
            item['list_time'] = ''
            #房屋年限
            item['house_year'] = ''
            #交易权属
            item['deal_type'] = ''
            #房屋用途
            item['house_usage'] = ''
            #房屋权属
            item['house_owner'] = ''
        #历史成交纪录
        item['deal_histry'] = response.css('.chengjiao_record .record_list li p::text').extract()
        #房源标签
        item['house_tag'] = response.css('.newwrap.baseinform .tags.clear a::text').extract()
        #房源特色
        item['house_feature'] = response.css('.newwrap.baseinform .baseattribute.clear .content::text').extract()
        #图片链接
        item['img_list'] = response.css('.thumbnail ul li::attr(data-src)').extract()
        yield item


        
