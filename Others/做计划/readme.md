# 程序说明
用来生成时间安排表的, 形式如下:
```Python
2016.07.21 周四:
    早上:
        08:05~09:05:   GitHub 整理
        09:05~10:05:   Python 学习
        10:05~11:05:   尚未安排
        11:05~11:30:   尚未安排
    下午:
        13:31~14:31:   GitHub 整理
        14:31~15:31:   Python 学习
        15:31~16:31:   尚未安排
        16:31~17:30:   尚未安排
    晚上:
        18:59~19:59:   GitHub 整理
        19:59~20:59:   Python 学习
        20:59~21:30:   尚未安排

2016.07.22 周五:
    早上:
        08:05~09:05:   GitHub 整理
        09:05~10:05:   Python 学习
        10:05~11:05:   尚未安排
        11:05~11:30:   尚未安排
    下午:
        13:31~14:31:   GitHub 整理
        14:31~15:31:   Python 学习
        ...
```
最终结果保存在同文件夹下 result.txt 文件

# 参数说明
更改代码里的:
* things = ["GitHub 整理", "Python 学习"], ``这是待办事项``
* date_plan = create_date(number=33), ``决定了要生成多少天的时间安排``
* morning_hour_plan = create_format_hour_plan("08:05", "11:30", things), ``决定了早晨安排的时间段``
* afternoon_hour_plan = create_format_hour_plan("13:31", "17:30", things), ``决定了下午安排的时间段``
* night_hour_plan = create_format_hour_plan("18:59", "21:30", things), ``决定了晚上安排的时间段``

