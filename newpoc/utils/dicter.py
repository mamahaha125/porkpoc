'''v0.2.20200518153151'''
from collections import OrderedDict


class Dicter(OrderedDict):
    '''有序字典转换为对象用法'''

    def __getattr__(self, key):
        '''获取时触发'''
        if key[:1] == r'_':
            return super().__getattribute__(key)
        else:
            if self.haskey(key):
                ret = self.__getitem__(key)
                # return ret
                if isinstance(ret, dict):
                    return Dicter(ret)
                if isinstance(ret, list):
                    tmp_ret = []
                    for val in ret:
                        if isinstance(val, dict):
                            val = Dicter(val)
                        tmp_ret.append(val)
                    del ret
                    return tmp_ret
                return ret
            else:
                return None

    def __setattr__(self, key, val):
        '''赋值触发'''
        if key[:1] == r'_':
            super().__setattr__(key, val)
        else:
            self.__setitem__(key, val)

    def __delattr__(self, key):
        '''del触发'''
        if key[:1] == r'_':
            super().__delattr__(key)
        else:
            self.__delitem__(key)

    def haskey(self, key):
        '''keys是否存在'''
        return key in self.keys()

    def hasval(self, val):
        '''val是否存在'''
        return val in self.values()

    def updata(self, dicter1):
        '''更新数据'''
        for key in dicter1.keys():
            self[key] = dicter1[key]
        return self

    # def set(self, key, val):
    #     self[key] = val

    def hasval_set(self, key, val):
        if not val:
            return
        self[key] = val


# d = Dicter()
# # d = {'ff': 1}
# d= {'a': {'SS': 's'}}
# # d['c'] = 'CC'
# print(d.a)
