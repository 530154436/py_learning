# /usr/bin/env python3
# -*- coding:utf-8 -*-
from xml.parsers.expat import ParserCreate

class DefaultSaxHandler(object):
    '''
    解析XML
    '''
    def start_element(self, name, attrs):
        print('sax:start_element: %s, attrs: %s' % (name, str(attrs)))

    def end_element(self, name):
        print('sax:end_element: %s' % name)

    def char_data(self, text):
        print('sax:char_data: %s' % text)

xml = r'''<?xml version="1.0"?>
<ol>
    <li><a href="/python">Python</a></li>
    <li><a href="/ruby">Ruby</a></li>
</ol>
'''
def parse_xml():
    handler = DefaultSaxHandler()
    parser = ParserCreate()
    parser.StartElementHandler = handler.start_element
    parser.EndElementHandler = handler.end_element
    parser.CharacterDataHandler = handler.char_data
    parser.Parse(xml)

def generate_xml():
    L = []
    L.append(r'<?xml version="1.0"?>')
    L.append(r'<root>')
    L.append('some & data')
    L.append(r'</root>')

    print(''.join(L))

class Weather(object):
    '''
    {
        'city': 'Beijing',
        'country': 'China',
        'today': {
            'text': 'Partly Cloudy',
            'low': 20,
            'high': 33
        },
        'tomorrow': {
            'text': 'Sunny',
            'low': 21,
            'high': 34
        }
    }
    '''
    def __init__(self):
        self._data = {}
        self._day_count = 0

    @property
    def data(self):
        return self._data

    def start_element(self, name, attrs):
        if name == 'yweather:location':
            self._data['city'] = attrs['city']
            self._data['country'] = attrs['country']
        if name == 'yweather:forecast':
            if self._day_count == 0:
                today = {}
                today['text'] = attrs['text']
                today['low'] = int(attrs['low'])
                today['high'] = int(attrs['high'])
                self._data['today'] = today
                self._day_count = self._day_count + 1
            elif self._day_count == 1:
                tomorrow = {}
                tomorrow['text'] = attrs['text']
                tomorrow['low'] = int(attrs['low'])
                tomorrow['high'] = int(attrs['high'])
                self._data['tomorrow'] = tomorrow
                self._day_count = self._day_count + 1
            else:
                pass


    def end_element(self, name):
        pass

    def char_data(self, text):
        pass


def parse_weather(xml):
    handler = Weather()
    parser = ParserCreate()
    parser.StartElementHandler = handler.start_element
    parser.EndElementHandler = handler.end_element
    parser.CharacterDataHandler = handler.char_data
    parser.Parse(xml)
    print(handler.data)
    return handler.data

def exercise():
    '''
    利用SAX编写程序解析Yahoo的XML格式的天气预报，获取当天和第二天的天气
    '''
    data = r'''<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
    <rss version="2.0" xmlns:yweather="http://xml.weather.yahoo.com/ns/rss/1.0" xmlns:geo="http://www.w3.org/2003/01/geo/wgs84_pos#">
        <channel>
            <title>Yahoo! Weather - Beijing, CN</title>
            <lastBuildDate>Wed, 27 May 2015 11:00 am CST</lastBuildDate>
            <yweather:location city="Beijing" region="" country="China"/>
            <yweather:units temperature="C" distance="km" pressure="mb" speed="km/h"/>
            <yweather:wind chill="28" direction="180" speed="14.48" />
            <yweather:atmosphere humidity="53" visibility="2.61" pressure="1006.1" rising="0" />
            <yweather:astronomy sunrise="4:51 am" sunset="7:32 pm"/>
            <item>
                <geo:lat>39.91</geo:lat>
                <geo:long>116.39</geo:long>
                <pubDate>Wed, 27 May 2015 11:00 am CST</pubDate>
                <yweather:condition text="Haze" code="21" temp="28" date="Wed, 27 May 2015 11:00 am CST" />
                <yweather:forecast day="Wed" date="27 May 2015" low="20" high="33" text="Partly Cloudy" code="30" />
                <yweather:forecast day="Thu" date="28 May 2015" low="21" high="34" text="Sunny" code="32" />
                <yweather:forecast day="Fri" date="29 May 2015" low="18" high="25" text="AM Showers" code="39" />
                <yweather:forecast day="Sat" date="30 May 2015" low="18" high="32" text="Sunny" code="32" />
                <yweather:forecast day="Sun" date="31 May 2015" low="20" high="37" text="Sunny" code="32" />
            </item>
        </channel>
    </rss>
    '''
    weather = parse_weather(data)
    assert weather['city'] == 'Beijing', weather['city']
    assert weather['country'] == 'China', weather['country']
    assert weather['today']['text'] == 'Partly Cloudy', weather['today']['text']
    assert weather['today']['low'] == 20, weather['today']['low']
    assert weather['today']['high'] == 33, weather['today']['high']
    assert weather['tomorrow']['text'] == 'Sunny', weather['tomorrow']['text']
    assert weather['tomorrow']['low'] == 21, weather['tomorrow']['low']
    assert weather['tomorrow']['high'] == 34, weather['tomorrow']['high']
    print('Weather:', str(weather))

if __name__ == '__main__':
    # parse_xml()
    # generate_xml()
    exercise()





