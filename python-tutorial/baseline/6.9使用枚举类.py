#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from enum import Enum,unique

Month = Enum('Month', ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
					   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'))

for name, member in Month.__members__.items():
	print(name, ' => ', member, ' => ', member.value)

class Weekday(Enum):
	Sun = 0
	Mon = 1
	Tue = 2
	Wed = 3
	Thu = 4
	Fri = 5
	Sat = 6
	Sat_ta = 6

# OrderedDict([('Sun', <Weekday.Sun: 0>), ('Mon', <Weekday.Mon: 1>), ('Tue', <Weekday.Tue: 2>), ('Wed', <Weekday.Wed: 3>), ('Thu', <Weekday.Thu: 4>), ('Fri', <Weekday.Fri: 5>), ('Sat', <Weekday.Sat: 6>)])
print(Weekday.__members__)
# Weekday.Mon
print(Weekday.Mon)
# Weekday.Mon
print(Weekday['Mon'])
# 1
print(Weekday.Mon.value)
#Weekday.Mon
print(Weekday(1))

#把值重复的成员也遍历出来，要用枚举的一个特殊属性__members__
for name, member in Weekday.__members__.items():
	print(name, '=>', member)

#值重复的成员，循环遍历枚举时只获取值重复成员的第一个成员
for member in Weekday:
	print(member)

