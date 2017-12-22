# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field


class HouseInfoItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #行政区名称
    district = Field()
    #行政区内区域名称
    district_area = Field()
    #小区名称
    xiaoqu = Field()
    #小区id
    xiaoqu_id = Field()
    #小区经度
    xiaoqu_long = Field()
    #小区纬度
    xiaoqu_lat = Field()
    #成交房源的链家ID
    lianjia_id = Field()
    #成交名称
    title = Field() 
    #成交日期
    deal_date = Field()
    #成交公司
    deal_com = Field()
    #成交总价
    total_price = Field()
    #成交单价
    unit_price = Field()
    #挂牌价格
    list_price = Field()
    #成交周期
    deal_cycle = Field()
    #调价次数
    price_adj_num = Field()
    #带看次数
    see_num = Field()
    #关注人数
    follow_num = Field()
    #浏览次数
    view_num = Field()
    #户型
    house_type = Field()
    #建筑面积
    build_area = Field()
    #套内面积
    dwelling_area = Field()
    #房屋朝向
    orientation = Field()
    #装修情况
    decoration = Field()
    #供暖方式
    heating = Field()
    #产权年限
    property_time = Field()
    #所在楼层
    floor = Field()
    #户型结构
    house_type_str = Field()
    #建筑类型
    build_type = Field()
    #建筑年代
    build_year = Field()
    #建筑结构
    build_archit = Field()
    #梯户比例
    elevator_rate = Field()
    #配备电梯
    elevator_ = Field()
    #挂牌时间
    list_time = Field()
    #房屋年限
    house_year = Field()
    #交易权属
    deal_type = Field()
    #房屋用途
    house_usage = Field()
    #房屋权属
    house_owner = Field()
    #历史成交纪录
    deal_histry = Field()
    #房源标签
    house_tag = Field()
    #核心卖点
    house_feature = Field()
    #图片链接
    img_list =Field()

class XiaoquDealNumItem(Item):
    #小区名称
    xiaoqu = Field()
    #成交房源数量
    deal_num = Field()
