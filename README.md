# Chinesename

Generate Chinese name according to statistic model.

通过统计模型生成中文姓名。

    import chinesename
    nm = NameModel('namemodel.m')
    print(nm.getname())
    print(nm.processinput('wangxiaoming', 100))

## 功能

* 随机生成
* 拼音分词
* 拼音查询

包括部分修正的 [python-pinyin/pypinyin/pinyin_dict.py](https://github.com/mozillazg/python-pinyin/blob/master/pypinyin/pinyin_dict.py)

## 授权

MIT License
