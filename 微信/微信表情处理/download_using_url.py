#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 使用 URL 下载表情
"""
import requests

__author__ = '__L1n__w@tch'

if __name__ == "__main__":
    all_requests = """/mmemoticon/Q3auHgzwzM4A2oaOBRow3QusFtDibfvFwlerlg2OPj2wWU5RC5crUO92fy5G3eLxZ/0
/mmemoticon/Q3auHgzwzM4vIcERO1iaWN9g1fcvT3XvaJLbHNfztXd4oFxpgAUDXUiaiaU2bBbLO12/0
/mmemoticon/Q3auHgzwzM5VJ08oQa1qKVobndzRJicwTMsD4oDZ23vcicEcA4ZViaNEANnfdkpnJhB/0
/mmemoticon/Q3auHgzwzM796icNEn7Xd4XwNX1hCYyAPWRbbf7dBnFpgn3joUVfxlC6zkLg6mCA3/0
/mmemoticon/Q3auHgzwzM7B8OOkp5LFWTBicVKEnicu7z8TTLGxFc6okAA3FiaKt2ArsOXEHCQGcpK/0
/mmemoticon/Q3auHgzwzM7a38SyvibMdKunsdqV7dnHvPq0flZfmwgE9NvweLA6AiaiauO5h2lovvD/0
/mmemoticon/Q3auHgzwzM7lf1vRwFDtwCI11lgdHPFGicmUTkaNI01xru5eIdlPcQ5cUiaRibQQBjL/0
/mmemoticon/ajNVdqHZLLA0S5KxD3YJjR6KKCBFZxsz3p6dKZUiaWXbhgxoXAN7sp8NhxFpZBELh/0
/mmemoticon/ajNVdqHZLLA4XqclcticIpDr9IjVKeWicsAVjnUmhTtIwpVuKl6GjXcoP4aDFibLia5L/0
/mmemoticon/ajNVdqHZLLA8JYkwicuPa1EO5g50MibOWe9lfXYTficZWNDwEyeDZCiceSVZW6YuH3Bia/0
/mmemoticon/ajNVdqHZLLACNZkcWvHBNRqNvibqdRKUZRNZLmCx5ctib2mWUuu1m5tzHB6cPicPYmib/0
/mmemoticon/ajNVdqHZLLALxSLBT9ia2YKjKr9oZby9OZ9GlZUPqqt4EJ9OlhiakL214KcMKVQZ83/0
/mmemoticon/ajNVdqHZLLAWgbExnXhiceJeWLYWwLC66A7rwANBgAib7xglvFIQNpZUEQCoQbibFSW/0
/mmemoticon/ajNVdqHZLLAhXBBjIqSl2YFpG9AnaSYkX9d7vwttXGKa8j4XaLo5F9Hf2NW9DGAL/0
/mmemoticon/ajNVdqHZLLAszSAQ4gJlh2uYUaF9WWKjwUHFRjFst34FiaJmFzevpCcic4driblPibAy/0
/mmemoticon/ajNVdqHZLLBG3Rhvyaot4E9q3EseLXTiclcm7Hx7upyIDKCeuB8ViaqniaCy6cB0Kht/0
/mmemoticon/ajNVdqHZLLBpI7y0C4mp9tUMsI5zceAvHOeJuKL3EFz2PQLvuELWibVHJEknlwIxJ/0
/mmemoticon/ajNVdqHZLLC3ib2qk5SSCGPlDmbFemiapQZH3yL0WLJZlcFCzRReuELkANmyZNAWzN/0
/mmemoticon/ajNVdqHZLLCDicxCiafP2KpuGLVCGfgJhMy03gjQVVKUhnI8lTeg0dpoGZOohLrqAj/0
/mmemoticon/ajNVdqHZLLCdwOLyl7c6JEooibPeicSlDrVAyUhBsJTGRBx1FUfCVxX13IceibR5hQG/0
/mmemoticon/ajNVdqHZLLCekdibhG6xrkUubuPJ4n5ZGicbJw12hLLK05OGWJUw606MWO8AcFoAyU/0
/mmemoticon/ajNVdqHZLLCmxPqI7fND1snSXT3ITlib8rELQo239CreibABo4SMjLgJ2TaJ0QH9m4/0
/mmemoticon/ajNVdqHZLLDOlsGtttOfyNHPic8yL4LxL8TyeYClx25Sr2JUgATXIZiakL2ibbAia7gh/0
/mmemoticon/ajNVdqHZLLDSKTMRgM8agjLEV9o473jC9VuQlVicGXfnrOImmVbUXrSWsG2icciaicEV/0"""
    url = "http://mmbiz.qpic.cn{}"
    for i,each_url in enumerate(all_requests.split()):
        true_url = url.format(each_url)
        with open("{}.gif".format(i),"wb") as f:
            response = requests.get(true_url)
            f.write(response.content)
