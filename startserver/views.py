from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from xpinyin import Pinyin
from urllib import request
from bs4 import BeautifulSoup
import datetime
import time
from weather.models import *
# Create your views here.
@csrf_exempt
def startserver_views(request):
    password_to_startserver = 'modifydata'
    password_to_prepareserver = 'createdata'
    if request.method == 'GET':
        massage = ''
        return render(request, 'as_server_password.html', locals())
    else:
        password_get = request.POST['password']
        if password_to_startserver == password_get:
            n = 0
            while True:
                if n == 2160:
                    return HttpResponse('服务器已启动')
                timenow = time.ctime()
                timenow = timenow.split(' ')[4]
                timenow = timenow.split(':')
                if timenow[1] == '00' and timenow[2] == '00':
                    n += 1
                    main_modify()
                else:
                    time.sleep(0.5)
        elif password_to_prepareserver == password_get:
            main_create()
            return HttpResponse('服务器准备中')
        else:
            massage = '密码错误'
            return render(request, 'as_server_password.html', locals())

def getweather(city, prov):
    pin = Pinyin()
    if prov == '内蒙古':
        prov_pin = 'inner-mongolia'
    elif prov == '陕西':
        prov_pin = 'shaanxi'
    elif prov == '西藏':
        prov_pin = 'tibet'
    elif prov == '重庆':
        prov_pin = 'chongqing'
    elif prov == '香港':
        prov_pin = 'hong-kong'
    elif prov == '澳门':
        prov_pin = 'macau'
    else:
        prov_pin = pin.get_pinyin(prov, '')  # 将汉字转为拼音
    city_dic = {'蚌埠': 'bengbu', '六安': "lu'an", "神农架": "shennongjia-", '伊犁哈萨克': 'ili-kazakh-autonomous-prefecture',
                '克拉玛依': 'karamay', '图木舒克': 'tumxuk', '巴音郭楞蒙古': 'bayingolin-mongol-autonomous-prefecture', '澳门': 'macau',
                '博尔塔拉': 'boertala-mongolian-autonomous-prefecture', '吐鲁番': 'turpan', '喀什': 'kashgar', '重庆': 'chongqing',
                '阿勒泰': 'altay-county', '和田': 'hotan', '阿克苏': 'aksu','克孜勒苏柯尔克孜': 'kizilsu-kirghiz-autonomous-prefecture',
                '乌鲁木齐': 'urumqi', '阿拉尔': 'alar', "吉安": "ji'an", '漯河': 'luohe', '哈尔滨': 'harbin', '齐齐哈尔': 'qiqihar',
                '海北': 'haibei-tibetan-autonomous-prefecture', '黄南': 'huangnan-tibetan-autonomous-prefecture','香港': 'hong-kong',
                '海西': 'haixi-mongolian-tibetan-autonomous-prefecture', '海南': 'hainan-tibetan-autonomous-prefecture', '拉萨': 'lhasa',
                '果洛': 'golog-tibetan-autonomous-prefecture', '呼伦贝尔': 'hulunbuir', '鄂尔多斯': 'ordos', '呼和浩特': 'hohhot',
                '巴彦淖尔': 'bayannur', '昌都': 'qamdo', '林芝': 'nyingchi', '山南': 'lhoka-prefecture', '日喀则': 'shigatse',
                '那曲': 'nagqu-county', '莆田': 'putian', '厦门': 'xiamen', '乐东': 'ledong-li-autonomous-county', '朝阳': 'chaoyang',
                '陵水': 'lingshui-li-autonomous-county', '保亭': 'baoting-li-and-miao-autonomous-county', '文山': 'wensha',
                '湘西': 'xiangxi-tujia-and-miao-autonomous-prefecture', '黔东南': 'qiandongnan-miao-and-dong-autonomous-prefecture',
                '黔南': 'qiannan-buyi-and-miao-autonomous-prefecture', '红河': 'honghe-hani-and-yi-autonomous-prefecture',
                '迪庆': 'diqing-tibetan-autonomous-prefecture', '西双版纳': 'xishuangbanna-dai-autonomous-prefecture',
                '德宏': 'dehong-dai-and-jingpo-autonomous-prefecture', '怒江': 'nujiang-lisu-autonomous-prefecture', '吕梁': 'luliang',
                '凉山': 'liangshan-yi-autonomous-prefecture', '阿坝': 'aba-(ngawa)-tibetan-and-qiang-autonomous-prefecture'
                }
    if city in city_dic.keys():
        city_pin = city_dic[city]
    else:
        city_pin = pin.get_pinyin(city, '')
    url = "https://tianqi.moji.com/weather/china/"
    url = url + prov_pin + '/' + city_pin
    # 获取天气信息begin
    htmlData = request.urlopen(url).read().decode('utf-8')
    soup = BeautifulSoup(htmlData, 'lxml')
    weather = soup.find('div', attrs={'class': "wea_weather clearfix"})
    try:
        now = str(weather).split('<b>')
        now = now[1].split('</b>')
        now = now[0]
    except:
        now = '暂无数据'
    try:
        temp1 = weather.find('em').get_text()
    except:
        temp1 = '暂无数据'
    # 使用select标签时，如果class中有空格，将空格改为“.”才能筛选出来
    # 空气质量AQI
    try:
        AQI = soup.select(".wea_alert.clearfix > ul > li > a > em")[0].get_text()
    except:
        AQI = '暂无数据'
    try:
        H = soup.select(".wea_about.clearfix > span")[0].get_text()  # 湿度
        H = H[3:]
    except:
        H = '暂无数据'
    try:
        S = soup.select(".wea_about.clearfix > em")[0].get_text()  # 风速
    except:
        S = '暂无数据'
    try:
        U = soup.select(".live_index_grid > ul > li")[-3].find('dt').get_text()  # 紫外线强度
    except:
        U = '暂无数据'
    infodic = {}
    DATE = str(datetime.date.today())
    infodic['date'] = DATE + ' ' + now
    infodic['temp'] = '实时温度：' + temp1 + '℃'
    infodic['humi'] = '空气湿度：' + H
    infodic['airq'] = '空气质量：' + AQI
    infodic['wind'] = '风向和风级：' + S
    infodic['rays'] = '紫外线强度：' + U
    # 获取明日天气
    tomorrow = soup.select(".days.clearfix ")[1].find_all('li')
    try:
        tom = tomorrow[1].find('img').attrs['alt']
    except:
        tom = '暂无数据'
    try:
        temp_t = tomorrow[2].get_text().replace('°', '℃')  # 明日温度
    except:
        temp_t = '暂无数据'
    try:
        S_t1 = tomorrow[3].find('em').get_text()
        S_t2 = tomorrow[3].find('b').get_text()
        S_t = S_t1 + S_t2  # 明日风速
    except:
        S_t = '暂无数据'
    try:
        AQI_t = tomorrow[-1].get_text().strip()  # 明日空气质量
    except:
        AQI_t = '暂无数据'
    date_t = datetime.datetime.now()
    num = date_t.weekday()
    days = '日一二三四五六'
    date_t = '星期' + days[num]
    infotdic = {}
    infotdic['tomw'] = '天气：' + tom
    infotdic['temp'] = '温度：' + temp_t
    infotdic['airq'] = '空气质量：' + AQI_t
    infotdic['wind'] = '风向和风级：' + S_t
    infotdic['date'] = '明天  ' + date_t
    # 获取天气信息结束
    return infodic, infotdic

def main_create():
    lst = [ { "id": "110000", "name": "北京", "city": [{ "id": "110100", "name": "北京" }] },
             { "id": "120000", "name": "天津", "city": [{ "id": "120100", "name": "天津" }] },
             { "id": "310000", "name": "上海", "city": [{ "id": "310100", "name": "上海" }] },
             { "id": "500000", "name": "重庆", "city": [{ "id": "500100", "name": "重庆" }] },
             { "id": "130000", "name": "河北", "city": [{ "id": "131100", "name": "衡水" }, { "id": "130800", "name": "承德" }, { "id": "130100", "name": "石家庄" }, { "id": "130300", "name": "秦皇岛" }, { "id": "130700", "name": "张家口" }, { "id": "131000", "name": "廊坊" }, { "id": "130500", "name": "邢台" }, { "id": "130900", "name": "沧州" }, { "id": "130200", "name": "唐山" }, { "id": "130600", "name": "保定" }] },
             { "id": "320000", "name": "江苏", "city": [{ "id": "321200", "name": "泰州" }, { "id": "320300", "name": "徐州" }, { "id": "320500", "name": "苏州" }, { "id": "320100", "name": "南京" }, { "id": "320400", "name": "常州" }, { "id": "320900", "name": "盐城" }, { "id": "320800", "name": "淮安" }, { "id": "320700", "name": "连云港" }, { "id": "321000", "name": "扬州" }, { "id": "320200", "name": "无锡" }, { "id": "321300", "name": "宿迁" }, { "id": "320600", "name": "南通" }, { "id": "321100", "name": "镇江" }] },
             { "id": "440000", "name": "广东", "city": [{ "id": "440400", "name": "珠海" }, { "id": "441600", "name": "河源" }, { "id": "440600", "name": "佛山" }, { "id": "445200", "name": "揭阳" }, { "id": "440100", "name": "广州" }, { "id": "441900", "name": "东莞" }, { "id": "440200", "name": "韶关" }, { "id": "441500", "name": "汕尾" }, { "id": "445300", "name": "云浮" }, { "id": "440800", "name": "湛江" }, { "id": "440300", "name": "深圳" }, { "id": "441300", "name": "惠州" }, { "id": "440900", "name": "茂名" }, { "id": "442000", "name": "中山" }, { "id": "441400", "name": "梅州" }, { "id": "440500", "name": "汕头" }, { "id": "441200", "name": "肇庆" }, { "id": "445100", "name": "潮州" }, { "id": "440700", "name": "江门" }, { "id": "441800", "name": "清远" }] },
             { "id": "340000", "name": "安徽", "city": [{ "id": "340800", "name": "安庆" }, { "id": "340300", "name": "蚌埠" }, { "id": "341600", "name": "亳州" }, { "id": "340200", "name": "芜湖" }, { "id": "341000", "name": "黄山" }, { "id": "340500", "name": "马鞍山" }, { "id": "340700", "name": "铜陵" }, { "id": "340600", "name": "淮北" }, { "id": "341200", "name": "阜阳" }, { "id": "341800", "name": "宣城" }, { "id": "341300", "name": "宿州" }, { "id": "341500", "name": "六安" }, { "id": "341700", "name": "池州" }, { "id": "340400", "name": "淮南" }, { "id": "340100", "name": "合肥" }, { "id": "341100", "name": "滁州" }] },
             { "id": "330000", "name": "浙江", "city": [{ "id": "331100", "name": "丽水" }, { "id": "330600", "name": "绍兴" }, { "id": "330100", "name": "杭州" }, { "id": "330200", "name": "宁波" }, { "id": "330900", "name": "舟山" }, { "id": "330400", "name": "嘉兴" }, { "id": "330800", "name": "衢州" }, { "id": "331000", "name": "台州" }, { "id": "330300", "name": "温州" }, { "id": "330700", "name": "金华" }, { "id": "330500", "name": "湖州" }] },
             { "id": "420000", "name": "湖北", "city": [{ "id": "429004", "name": "仙桃" }, { "id": "429005", "name": "潜江" }, { "id": "420700", "name": "鄂州" }, { "id": "420500", "name": "宜昌" }, { "id": "421200", "name": "咸宁" }, { "id": "429021", "name": "神农架" }, { "id": "421100", "name": "黄冈" }, { "id": "420900", "name": "孝感" }, { "id": "421300", "name": "随州" }, { "id": "429006", "name": "天门" }, { "id": "421000", "name": "荆州" }, { "id": "420300", "name": "十堰" }, { "id": "420600", "name": "襄阳" }, { "id": "420800", "name": "荆门" }, { "id": "420100", "name": "武汉" }, { "id": "420200", "name": "黄石" }] },
             { "id": "370000", "name": "山东", "city": [{ "id": "371000", "name": "威海" }, { "id": "370600", "name": "烟台" }, { "id": "370900", "name": "泰安" }, { "id": "371300", "name": "临沂" }, { "id": "370400", "name": "枣庄" }, { "id": "370500", "name": "东营" }, { "id": "371400", "name": "德州" }, { "id": "370300", "name": "淄博" }, { "id": "371500", "name": "聊城" }, { "id": "371200", "name": "莱芜" }, { "id": "371600", "name": "滨州" }, { "id": "370700", "name": "潍坊" }, { "id": "371100", "name": "日照" }, { "id": "370200", "name": "青岛" }, { "id": "370100", "name": "济南" }, { "id": "370800", "name": "济宁" }, { "id": "371700", "name": "菏泽" }] },
             { "id": "650000", "name": "新疆", "city": [{ "id": "650200", "name": "克拉玛依" }, { "id": "654200", "name": "塔城" }, { "id": "652700", "name": "博尔塔拉" }, { "id": "659001", "name": "石河子" }, { "id": "652100", "name": "吐鲁番" }, { "id": "653100", "name": "喀什" }, { "id": "659004", "name": "五家渠" }, { "id": "654300", "name": "阿勒泰" }, { "id": "652300", "name": "昌吉" }, { "id": "652200", "name": "哈密" }, { "id": "653200", "name": "和田" }, { "id": "652900", "name": "阿克苏" }, { "id": "650100", "name": "乌鲁木齐" }] },
             { "id": "360000", "name": "江西", "city": [{ "id": "360100", "name": "南昌" }, { "id": "360400", "name": "九江" }, { "id": "360800", "name": "吉安" }, { "id": "361000", "name": "抚州" }, { "id": "360200", "name": "景德镇" }, { "id": "360300", "name": "萍乡" }, { "id": "360900", "name": "宜春" }, { "id": "360500", "name": "新余" }, { "id": "360700", "name": "赣州" }, { "id": "361100", "name": "上饶" }, { "id": "360600", "name": "鹰潭" }] },
             { "id": "450000", "name": "广西", "city": [{ "id": "450400", "name": "梧州" }, { "id": "450900", "name": "玉林" }, { "id": "451100", "name": "贺州" }, { "id": "451400", "name": "崇左" }, { "id": "451000", "name": "百色" }, { "id": "450700", "name": "钦州" }, { "id": "450500", "name": "北海" }, { "id": "450800", "name": "贵港" }, { "id": "451200", "name": "河池" }, { "id": "450200", "name": "柳州" }, { "id": "451300", "name": "来宾" }, { "id": "450100", "name": "南宁" }, { "id": "450300", "name": "桂林" }, { "id": "450600", "name": "防城港" }] },
             { "id": "410000", "name": "河南", "city": [{ "id": "410800", "name": "焦作" }, { "id": "410900", "name": "濮阳" }, { "id": "411500", "name": "信阳" }, { "id": "410200", "name": "开封" }, { "id": "411300", "name": "南阳" }, { "id": "410100", "name": "郑州" }, { "id": "410500", "name": "安阳" }, { "id": "410700", "name": "新乡" }, { "id": "411700", "name": "驻马店" }, { "id": "410600", "name": "鹤壁" }, { "id": "411400", "name": "商丘" }, { "id": "410400", "name": "平顶山" }, { "id": "411200", "name": "三门峡" }, { "id": "411000", "name": "许昌" }, { "id": "411600", "name": "周口" }, { "id": "411100", "name": "漯河" }, { "id": "410300", "name": "洛阳" }] },
             { "id": "230000", "name": "黑龙江", "city": [{ "id": "230900", "name": "七台河" }, { "id": "230500", "name": "双鸭山" }, { "id": "230400", "name": "鹤岗" }, { "id": "230100", "name": "哈尔滨" }, { "id": "230200", "name": "齐齐哈尔" }, { "id": "231200", "name": "绥化" }, { "id": "231000", "name": "牡丹江" }, { "id": "230800", "name": "佳木斯" }, { "id": "230700", "name": "伊春" }, { "id": "231100", "name": "黑河" }, { "id": "230300", "name": "鸡西" }, { "id": "230600", "name": "大庆" }] },
             { "id": "630000", "name": "青海", "city": [{ "id": "632200", "name": "海北" }, { "id": "632300", "name": "黄南" }, { "id": "630200", "name": "海东" }, { "id": "632800", "name": "海西" }, { "id": "630100", "name": "西宁" }, { "id": "632700", "name": "玉树" }, { "id": "632600", "name": "果洛" }, { "id": "632500", "name": "海南" }] },
             { "id": "150000", "name": "内蒙古", "city": [{ "id": "150400", "name": "赤峰" }, { "id": "150900", "name": "乌兰察布" }, { "id": "150200", "name": "包头" }, { "id": "150300", "name": "乌海" }, { "id": "150700", "name": "呼伦贝尔" }, { "id": "150600", "name": "鄂尔多斯" }, { "id": "150500", "name": "通辽" }, { "id": "150100", "name": "呼和浩特" }, { "id": "150800", "name": "巴彦淖尔" }] },
             { "id": "610000", "name": "陕西", "city": [{ "id": "610800", "name": "榆林" }, { "id": "610700", "name": "汉中" }, { "id": "610600", "name": "延安" }, { "id": "610300", "name": "宝鸡" }, { "id": "610200", "name": "铜川" }, { "id": "610400", "name": "咸阳" }, { "id": "610500", "name": "渭南" }, { "id": "610900", "name": "安康" }, { "id": "610100", "name": "西安" }, { "id": "611000", "name": "商洛" }] },
             { "id": "540000", "name": "西藏", "city": [{ "id": "542100", "name": "昌都" }, { "id": "542600", "name": "林芝" }, { "id": "542200", "name": "山南" }, { "id": "540100", "name": "拉萨" }, { "id": "540200", "name": "日喀则" }, { "id": "542400", "name": "那曲" }] },
             { "id": "350000", "name": "福建", "city": [{ "id": "350400", "name": "三明" }, { "id": "350900", "name": "宁德" }, { "id": "350600", "name": "漳州" }, { "id": "350300", "name": "莆田" }, { "id": "350700", "name": "南平" }, { "id": "350200", "name": "厦门" }, { "id": "350100", "name": "福州" }, { "id": "350800", "name": "龙岩" }, { "id": "350500", "name": "泉州" }] },
             { "id": "460000", "name": "海南", "city": [{ "id": "460100", "name": "海口" }, { "id": "469003", "name": "儋州" }, { "id": "469002", "name": "琼海" }, { "id": "469001", "name": "五指山" }, { "id": "469005", "name": "文昌" }, { "id": "460200", "name": "三亚" }, { "id": "469006", "name": "万宁" }, { "id": "469007", "name": "东方" }] },
             { "id": "210000", "name": "辽宁", "city": [{ "id": "210600", "name": "丹东" }, { "id": "210400", "name": "抚顺" }, { "id": "210500", "name": "本溪" }, { "id": "211300", "name": "朝阳" }, { "id": "211000", "name": "辽阳" }, { "id": "211200", "name": "铁岭" }, { "id": "210200", "name": "大连" }, { "id": "210700", "name": "锦州" }, { "id": "210900", "name": "阜新" }, { "id": "210100", "name": "沈阳" }, { "id": "211400", "name": "葫芦岛" }, { "id": "210800", "name": "营口" }, { "id": "210300", "name": "鞍山" }, { "id": "211100", "name": "盘锦" }] },
             { "id": "430000", "name": "湖南", "city": [{ "id": "431100", "name": "永州" }, { "id": "430100", "name": "长沙" }, { "id": "430200", "name": "株洲" }, { "id": "431300", "name": "娄底" }, { "id": "433100", "name": "湘西" }, { "id": "430300", "name": "湘潭" }, { "id": "430400", "name": "衡阳" }, { "id": "430700", "name": "常德" }, { "id": "430500", "name": "邵阳" }, { "id": "431200", "name": "怀化" }, { "id": "430600", "name": "岳阳" }, { "id": "431000", "name": "郴州" }, { "id": "430800", "name": "张家界" }] },
             { "id": "620000", "name": "甘肃", "city": [{ "id": "620500", "name": "天水" }, { "id": "620200", "name": "嘉峪关" }, { "id": "620700", "name": "张掖" }, { "id": "620600", "name": "武威" }, { "id": "621200", "name": "陇南" }, { "id": "620400", "name": "白银" }, { "id": "621000", "name": "庆阳" }, { "id": "620900", "name": "酒泉" }, { "id": "622900", "name": "临夏" }, { "id": "620800", "name": "平凉" }, { "id": "620300", "name": "金昌" }, { "id": "620100", "name": "兰州" }, { "id": "621100", "name": "定西" }] },
             { "id": "520000", "name": "贵州", "city": [{ "id": "520200", "name": "六盘水" }, { "id": "520400", "name": "安顺" }, { "id": "520300", "name": "遵义" }, { "id": "522300", "name": "黔西南" }, { "id": "520100", "name": "贵阳" }, { "id": "522600", "name": "黔东南" }, { "id": "520500", "name": "毕节" }, { "id": "522700", "name": "黔南" }, { "id": "520600", "name": "铜仁" }] },
             { "id": "530000", "name": "云南", "city": [{ "id": "530500", "name": "保山" }, { "id": "532500", "name": "红河" }, { "id": "530100", "name": "昆明" }, { "id": "533400", "name": "迪庆" }, { "id": "532900", "name": "大理" }, { "id": "530700", "name": "丽江" }, { "id": "530900", "name": "临沧" }, { "id": "532800", "name": "西双版纳" }, { "id": "530300", "name": "曲靖" }, { "id": "530800", "name": "普洱" }, { "id": "530600", "name": "昭通" }, { "id": "532300", "name": "楚雄" }, { "id": "532600", "name": "文山" }, { "id": "530400", "name": "玉溪" }, { "id": "533100", "name": "德宏" }, { "id": "533300", "name": "怒江" }] },
             { "id": "220000", "name": "吉林", "city": [{ "id": "220200", "name": "吉林" }, { "id": "220300", "name": "四平" }, { "id": "220100", "name": "长春" }, { "id": "220600", "name": "白山" }, { "id": "220500", "name": "通化" }, { "id": "220800", "name": "白城" }, { "id": "220400", "name": "辽源" }, { "id": "220700", "name": "松原" }] },
             { "id": "140000", "name": "山西", "city": [{ "id": "140500", "name": "晋城" }, { "id": "141000", "name": "临汾" }, { "id": "141100", "name": "吕梁" }, { "id": "140400", "name": "长治" }, { "id": "140700", "name": "晋中" }, { "id": "140100", "name": "太原" }, { "id": "140800", "name": "运城" }, { "id": "140600", "name": "朔州" }, { "id": "140300", "name": "阳泉" }, { "id": "140900", "name": "忻州" }, { "id": "140200", "name": "大同" }] },
             { "id": "510000", "name": "四川", "city": [{ "id": "511100", "name": "乐山" }, { "id": "513400", "name": "凉山" }, { "id": "512000", "name": "资阳" }, { "id": "511900", "name": "巴中" }, { "id": "510300", "name": "自贡" }, { "id": "513300", "name": "甘孜" }, { "id": "511600", "name": "广安" }, { "id": "510800", "name": "广元" }, { "id": "511800", "name": "雅安" }, { "id": "511700", "name": "达州" }, { "id": "510600", "name": "德阳" }, { "id": "510700", "name": "绵阳" }, { "id": "511500", "name": "宜宾" }, { "id": "513200", "name": "阿坝" }, { "id": "511000", "name": "内江" }, { "id": "510100", "name": "成都" }, { "id": "510500", "name": "泸州" }, { "id": "510900", "name": "遂宁" }, { "id": "510400", "name": "攀枝花" }, { "id": "511300", "name": "南充" }, { "id": "511400", "name": "眉山" }] },
             { "id": "640000", "name": "宁夏", "city": [{ "id": "640100", "name": "银川" }, { "id": "640300", "name": "吴忠" }, { "id": "640500", "name": "中卫" }, { "id": "640200", "name": "石嘴山" }, { "id": "640400", "name": "固原" }] }]
    warning = {}
    for i in lst:
        prov = i['name']
        for l in i['city']:
            try:
                time.sleep(1)
                city = l['name']
                print(city, prov)
                infodic, infotdic = getweather(city, prov)
                a = time.ctime()
                a = a.split(' ')[4]
                a = a[:5] + '更新'
                print(a)
                Weather_now.objects.create(city=prov+'-'+city, weat_now=infodic['date'], temp_now=infodic['temp'], humi_now=infodic['humi'],
                                            airq_now=infodic['airq'], wind_now=infodic['wind'], rays_now=infodic['rays'], time_now=a)
                Weather_tom.objects.create(city_id=prov+'-'+city, date_tom=infotdic['date'], weat_tom=infotdic['tomw'], temp_tom=infotdic['temp'],
                                           airq_tom=infotdic['airq'], wind_tom=infotdic['wind'])
            except Exception as e:
                warning['city'] = prov
                print(e)

def main_modify():
    lst = [ { "id": "110000", "name": "北京", "city": [{ "id": "110100", "name": "北京" }] },
             { "id": "120000", "name": "天津", "city": [{ "id": "120100", "name": "天津" }] },
             { "id": "310000", "name": "上海", "city": [{ "id": "310100", "name": "上海" }] },
             { "id": "500000", "name": "重庆", "city": [{ "id": "500100", "name": "重庆" }] },
             { "id": "130000", "name": "河北", "city": [{ "id": "131100", "name": "衡水" }, { "id": "130800", "name": "承德" }, { "id": "130100", "name": "石家庄" }, { "id": "130300", "name": "秦皇岛" }, { "id": "130700", "name": "张家口" }, { "id": "131000", "name": "廊坊" }, { "id": "130500", "name": "邢台" }, { "id": "130900", "name": "沧州" }, { "id": "130200", "name": "唐山" }, { "id": "130600", "name": "保定" }] },
             { "id": "320000", "name": "江苏", "city": [{ "id": "321200", "name": "泰州" }, { "id": "320300", "name": "徐州" }, { "id": "320500", "name": "苏州" }, { "id": "320100", "name": "南京" }, { "id": "320400", "name": "常州" }, { "id": "320900", "name": "盐城" }, { "id": "320800", "name": "淮安" }, { "id": "320700", "name": "连云港" }, { "id": "321000", "name": "扬州" }, { "id": "320200", "name": "无锡" }, { "id": "321300", "name": "宿迁" }, { "id": "320600", "name": "南通" }, { "id": "321100", "name": "镇江" }] },
             { "id": "440000", "name": "广东", "city": [{ "id": "440400", "name": "珠海" }, { "id": "441600", "name": "河源" }, { "id": "440600", "name": "佛山" }, { "id": "445200", "name": "揭阳" }, { "id": "440100", "name": "广州" }, { "id": "441900", "name": "东莞" }, { "id": "440200", "name": "韶关" }, { "id": "441500", "name": "汕尾" }, { "id": "445300", "name": "云浮" }, { "id": "440800", "name": "湛江" }, { "id": "440300", "name": "深圳" }, { "id": "441300", "name": "惠州" }, { "id": "440900", "name": "茂名" }, { "id": "442000", "name": "中山" }, { "id": "441400", "name": "梅州" }, { "id": "440500", "name": "汕头" }, { "id": "441200", "name": "肇庆" }, { "id": "445100", "name": "潮州" }, { "id": "440700", "name": "江门" }, { "id": "441800", "name": "清远" }] },
             { "id": "340000", "name": "安徽", "city": [{ "id": "340800", "name": "安庆" }, { "id": "340300", "name": "蚌埠" }, { "id": "341600", "name": "亳州" }, { "id": "340200", "name": "芜湖" }, { "id": "341000", "name": "黄山" }, { "id": "340500", "name": "马鞍山" }, { "id": "340700", "name": "铜陵" }, { "id": "340600", "name": "淮北" }, { "id": "341200", "name": "阜阳" }, { "id": "341800", "name": "宣城" }, { "id": "341300", "name": "宿州" }, { "id": "341500", "name": "六安" }, { "id": "341700", "name": "池州" }, { "id": "340400", "name": "淮南" }, { "id": "340100", "name": "合肥" }, { "id": "341100", "name": "滁州" }] },
             { "id": "330000", "name": "浙江", "city": [{ "id": "331100", "name": "丽水" }, { "id": "330600", "name": "绍兴" }, { "id": "330100", "name": "杭州" }, { "id": "330200", "name": "宁波" }, { "id": "330900", "name": "舟山" }, { "id": "330400", "name": "嘉兴" }, { "id": "330800", "name": "衢州" }, { "id": "331000", "name": "台州" }, { "id": "330300", "name": "温州" }, { "id": "330700", "name": "金华" }, { "id": "330500", "name": "湖州" }] },
             { "id": "420000", "name": "湖北", "city": [{ "id": "429004", "name": "仙桃" }, { "id": "429005", "name": "潜江" }, { "id": "420700", "name": "鄂州" }, { "id": "420500", "name": "宜昌" }, { "id": "421200", "name": "咸宁" }, { "id": "429021", "name": "神农架" }, { "id": "421100", "name": "黄冈" }, { "id": "420900", "name": "孝感" }, { "id": "421300", "name": "随州" }, { "id": "429006", "name": "天门" }, { "id": "421000", "name": "荆州" }, { "id": "420300", "name": "十堰" }, { "id": "420600", "name": "襄阳" }, { "id": "420800", "name": "荆门" }, { "id": "420100", "name": "武汉" }, { "id": "420200", "name": "黄石" }] },
             { "id": "370000", "name": "山东", "city": [{ "id": "371000", "name": "威海" }, { "id": "370600", "name": "烟台" }, { "id": "370900", "name": "泰安" }, { "id": "371300", "name": "临沂" }, { "id": "370400", "name": "枣庄" }, { "id": "370500", "name": "东营" }, { "id": "371400", "name": "德州" }, { "id": "370300", "name": "淄博" }, { "id": "371500", "name": "聊城" }, { "id": "371200", "name": "莱芜" }, { "id": "371600", "name": "滨州" }, { "id": "370700", "name": "潍坊" }, { "id": "371100", "name": "日照" }, { "id": "370200", "name": "青岛" }, { "id": "370100", "name": "济南" }, { "id": "370800", "name": "济宁" }, { "id": "371700", "name": "菏泽" }] },
             { "id": "650000", "name": "新疆", "city": [{ "id": "650200", "name": "克拉玛依" }, { "id": "654200", "name": "塔城" }, { "id": "652700", "name": "博尔塔拉" }, { "id": "659001", "name": "石河子" }, { "id": "652100", "name": "吐鲁番" }, { "id": "653100", "name": "喀什" }, { "id": "659004", "name": "五家渠" }, { "id": "654300", "name": "阿勒泰" }, { "id": "652300", "name": "昌吉" }, { "id": "652200", "name": "哈密" }, { "id": "653200", "name": "和田" }, { "id": "652900", "name": "阿克苏" }, { "id": "650100", "name": "乌鲁木齐" }] },
             { "id": "360000", "name": "江西", "city": [{ "id": "360100", "name": "南昌" }, { "id": "360400", "name": "九江" }, { "id": "360800", "name": "吉安" }, { "id": "361000", "name": "抚州" }, { "id": "360200", "name": "景德镇" }, { "id": "360300", "name": "萍乡" }, { "id": "360900", "name": "宜春" }, { "id": "360500", "name": "新余" }, { "id": "360700", "name": "赣州" }, { "id": "361100", "name": "上饶" }, { "id": "360600", "name": "鹰潭" }] },
             { "id": "450000", "name": "广西", "city": [{ "id": "450400", "name": "梧州" }, { "id": "450900", "name": "玉林" }, { "id": "451100", "name": "贺州" }, { "id": "451400", "name": "崇左" }, { "id": "451000", "name": "百色" }, { "id": "450700", "name": "钦州" }, { "id": "450500", "name": "北海" }, { "id": "450800", "name": "贵港" }, { "id": "451200", "name": "河池" }, { "id": "450200", "name": "柳州" }, { "id": "451300", "name": "来宾" }, { "id": "450100", "name": "南宁" }, { "id": "450300", "name": "桂林" }, { "id": "450600", "name": "防城港" }] },
             { "id": "410000", "name": "河南", "city": [{ "id": "410800", "name": "焦作" }, { "id": "410900", "name": "濮阳" }, { "id": "411500", "name": "信阳" }, { "id": "410200", "name": "开封" }, { "id": "411300", "name": "南阳" }, { "id": "410100", "name": "郑州" }, { "id": "410500", "name": "安阳" }, { "id": "410700", "name": "新乡" }, { "id": "411700", "name": "驻马店" }, { "id": "410600", "name": "鹤壁" }, { "id": "411400", "name": "商丘" }, { "id": "410400", "name": "平顶山" }, { "id": "411200", "name": "三门峡" }, { "id": "411000", "name": "许昌" }, { "id": "411600", "name": "周口" }, { "id": "411100", "name": "漯河" }, { "id": "410300", "name": "洛阳" }] },
             { "id": "230000", "name": "黑龙江", "city": [{ "id": "230900", "name": "七台河" }, { "id": "230500", "name": "双鸭山" }, { "id": "230400", "name": "鹤岗" }, { "id": "230100", "name": "哈尔滨" }, { "id": "230200", "name": "齐齐哈尔" }, { "id": "231200", "name": "绥化" }, { "id": "231000", "name": "牡丹江" }, { "id": "230800", "name": "佳木斯" }, { "id": "230700", "name": "伊春" }, { "id": "231100", "name": "黑河" }, { "id": "230300", "name": "鸡西" }, { "id": "230600", "name": "大庆" }] },
             { "id": "630000", "name": "青海", "city": [{ "id": "632200", "name": "海北" }, { "id": "632300", "name": "黄南" }, { "id": "630200", "name": "海东" }, { "id": "632800", "name": "海西" }, { "id": "630100", "name": "西宁" }, { "id": "632700", "name": "玉树" }, { "id": "632600", "name": "果洛" }, { "id": "632500", "name": "海南" }] },
             { "id": "150000", "name": "内蒙古", "city": [{ "id": "150400", "name": "赤峰" }, { "id": "150900", "name": "乌兰察布" }, { "id": "150200", "name": "包头" }, { "id": "150300", "name": "乌海" }, { "id": "150700", "name": "呼伦贝尔" }, { "id": "150600", "name": "鄂尔多斯" }, { "id": "150500", "name": "通辽" }, { "id": "150100", "name": "呼和浩特" }, { "id": "150800", "name": "巴彦淖尔" }] },
             { "id": "610000", "name": "陕西", "city": [{ "id": "610800", "name": "榆林" }, { "id": "610700", "name": "汉中" }, { "id": "610600", "name": "延安" }, { "id": "610300", "name": "宝鸡" }, { "id": "610200", "name": "铜川" }, { "id": "610400", "name": "咸阳" }, { "id": "610500", "name": "渭南" }, { "id": "610900", "name": "安康" }, { "id": "610100", "name": "西安" }, { "id": "611000", "name": "商洛" }] },
             { "id": "540000", "name": "西藏", "city": [{ "id": "542100", "name": "昌都" }, { "id": "542600", "name": "林芝" }, { "id": "542200", "name": "山南" }, { "id": "540100", "name": "拉萨" }, { "id": "540200", "name": "日喀则" }, { "id": "542400", "name": "那曲" }] },
             { "id": "350000", "name": "福建", "city": [{ "id": "350400", "name": "三明" }, { "id": "350900", "name": "宁德" }, { "id": "350600", "name": "漳州" }, { "id": "350300", "name": "莆田" }, { "id": "350700", "name": "南平" }, { "id": "350200", "name": "厦门" }, { "id": "350100", "name": "福州" }, { "id": "350800", "name": "龙岩" }, { "id": "350500", "name": "泉州" }] },
             { "id": "460000", "name": "海南", "city": [{ "id": "460100", "name": "海口" }, { "id": "469003", "name": "儋州" }, { "id": "469002", "name": "琼海" }, { "id": "469001", "name": "五指山" }, { "id": "469005", "name": "文昌" }, { "id": "460200", "name": "三亚" }, { "id": "469006", "name": "万宁" }, { "id": "469007", "name": "东方" }] },
             { "id": "210000", "name": "辽宁", "city": [{ "id": "210600", "name": "丹东" }, { "id": "210400", "name": "抚顺" }, { "id": "210500", "name": "本溪" }, { "id": "211300", "name": "朝阳" }, { "id": "211000", "name": "辽阳" }, { "id": "211200", "name": "铁岭" }, { "id": "210200", "name": "大连" }, { "id": "210700", "name": "锦州" }, { "id": "210900", "name": "阜新" }, { "id": "210100", "name": "沈阳" }, { "id": "211400", "name": "葫芦岛" }, { "id": "210800", "name": "营口" }, { "id": "210300", "name": "鞍山" }, { "id": "211100", "name": "盘锦" }] },
             { "id": "430000", "name": "湖南", "city": [{ "id": "431100", "name": "永州" }, { "id": "430100", "name": "长沙" }, { "id": "430200", "name": "株洲" }, { "id": "431300", "name": "娄底" }, { "id": "433100", "name": "湘西" }, { "id": "430300", "name": "湘潭" }, { "id": "430400", "name": "衡阳" }, { "id": "430700", "name": "常德" }, { "id": "430500", "name": "邵阳" }, { "id": "431200", "name": "怀化" }, { "id": "430600", "name": "岳阳" }, { "id": "431000", "name": "郴州" }, { "id": "430800", "name": "张家界" }] },
             { "id": "620000", "name": "甘肃", "city": [{ "id": "620500", "name": "天水" }, { "id": "620200", "name": "嘉峪关" }, { "id": "620700", "name": "张掖" }, { "id": "620600", "name": "武威" }, { "id": "621200", "name": "陇南" }, { "id": "620400", "name": "白银" }, { "id": "621000", "name": "庆阳" }, { "id": "620900", "name": "酒泉" }, { "id": "622900", "name": "临夏" }, { "id": "620800", "name": "平凉" }, { "id": "620300", "name": "金昌" }, { "id": "620100", "name": "兰州" }, { "id": "621100", "name": "定西" }] },
             { "id": "520000", "name": "贵州", "city": [{ "id": "520200", "name": "六盘水" }, { "id": "520400", "name": "安顺" }, { "id": "520300", "name": "遵义" }, { "id": "522300", "name": "黔西南" }, { "id": "520100", "name": "贵阳" }, { "id": "522600", "name": "黔东南" }, { "id": "520500", "name": "毕节" }, { "id": "522700", "name": "黔南" }, { "id": "520600", "name": "铜仁" }] },
             { "id": "530000", "name": "云南", "city": [{ "id": "530500", "name": "保山" }, { "id": "532500", "name": "红河" }, { "id": "530100", "name": "昆明" }, { "id": "533400", "name": "迪庆" }, { "id": "532900", "name": "大理" }, { "id": "530700", "name": "丽江" }, { "id": "530900", "name": "临沧" }, { "id": "532800", "name": "西双版纳" }, { "id": "530300", "name": "曲靖" }, { "id": "530800", "name": "普洱" }, { "id": "530600", "name": "昭通" }, { "id": "532300", "name": "楚雄" }, { "id": "532600", "name": "文山" }, { "id": "530400", "name": "玉溪" }, { "id": "533100", "name": "德宏" }, { "id": "533300", "name": "怒江" }] },
             { "id": "220000", "name": "吉林", "city": [{ "id": "220200", "name": "吉林" }, { "id": "220300", "name": "四平" }, { "id": "220100", "name": "长春" }, { "id": "220600", "name": "白山" }, { "id": "220500", "name": "通化" }, { "id": "220800", "name": "白城" }, { "id": "220400", "name": "辽源" }, { "id": "220700", "name": "松原" }] },
             { "id": "140000", "name": "山西", "city": [{ "id": "140500", "name": "晋城" }, { "id": "141000", "name": "临汾" }, { "id": "141100", "name": "吕梁" }, { "id": "140400", "name": "长治" }, { "id": "140700", "name": "晋中" }, { "id": "140100", "name": "太原" }, { "id": "140800", "name": "运城" }, { "id": "140600", "name": "朔州" }, { "id": "140300", "name": "阳泉" }, { "id": "140900", "name": "忻州" }, { "id": "140200", "name": "大同" }] },
             { "id": "510000", "name": "四川", "city": [{ "id": "511100", "name": "乐山" }, { "id": "513400", "name": "凉山" }, { "id": "512000", "name": "资阳" }, { "id": "511900", "name": "巴中" }, { "id": "510300", "name": "自贡" }, { "id": "513300", "name": "甘孜" }, { "id": "511600", "name": "广安" }, { "id": "510800", "name": "广元" }, { "id": "511800", "name": "雅安" }, { "id": "511700", "name": "达州" }, { "id": "510600", "name": "德阳" }, { "id": "510700", "name": "绵阳" }, { "id": "511500", "name": "宜宾" }, { "id": "513200", "name": "阿坝" }, { "id": "511000", "name": "内江" }, { "id": "510100", "name": "成都" }, { "id": "510500", "name": "泸州" }, { "id": "510900", "name": "遂宁" }, { "id": "510400", "name": "攀枝花" }, { "id": "511300", "name": "南充" }, { "id": "511400", "name": "眉山" }] },
             { "id": "640000", "name": "宁夏", "city": [{ "id": "640100", "name": "银川" }, { "id": "640300", "name": "吴忠" }, { "id": "640500", "name": "中卫" }, { "id": "640200", "name": "石嘴山" }, { "id": "640400", "name": "固原" }] }]
    for i in lst:
        prov = i['name']
        for l in i['city']:
            try:
                time.sleep(1)
                city = l['name']
                print(city, prov)
                infodic, infotdic = getweather(city, prov)
                wea_now = Weather_now.objects.get(city=(prov+'-'+city))
                a = time.ctime()
                a = a.split(' ')[4]
                a = a[:5] + '更新'
                print(a)
                wea_now.time_now=a
                wea_now.weat_now=infodic['date']
                wea_now.temp_now=infodic['temp']
                wea_now.humi_now=infodic['humi']
                wea_now.airq_now=infodic['airq']
                wea_now.wind_now=infodic['wind']
                wea_now.rays_now=infodic['rays']
                wea_now.save()
                wea_tom = Weather_tom.objects.get(city_id=(prov+'-'+city))
                wea_tom.date_tom=infotdic['date']
                wea_tom.weat_tom=infotdic['tomw']
                wea_tom.temp_tom=infotdic['temp']
                wea_tom.airq_tom=infotdic['airq']
                wea_tom.wind_tom=infotdic['wind']
                wea_tom.save()
            except Exception as e:
                print(e)