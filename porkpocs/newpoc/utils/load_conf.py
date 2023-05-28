import configparser
from newpoc.utils.dicter import Dicter

def ini_to_dict():
    """
    读取conf配置文件，将数据转成字典，并转换为对象格式调用返回
    """
    config = configparser.ConfigParser()
    with open('./newpoc/conf.ini', encoding='utf-8') as conf:
        config.read_file(conf)
    ini_dict = {}
    for section in config.sections():
        section_dict = {}
        for option in config.options(section):
            section_dict[option] = config.get(section, option)
        ini_dict[section] = section_dict
    conf_dicts = Dicter(ini_dict)
    return conf_dicts
