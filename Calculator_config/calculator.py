#!/usr/bin/env python3
import sys
import csv
from collections import namedtuple

IncomeTaxQuickLookupItem=namedtuple(
    'IncomeTaxQuickLookupItem',
    ['Start_Point','Tax_rate','Quick_Cal']
)

Income_Tax_Start_Point=3500

Income_Tax_Quick_Lookup_Table=[
    IncomeTaxQuickLookupItem(80000,0.45,13505),
    IncomeTaxQuickLookupItem(55000,0.35,5505),
    IncomeTaxQuickLookupItem(35000,0.30,2755),
    IncomeTaxQuickLookupItem(9000,0.25,1005),
    IncomeTaxQuickLookupItem(4500,0.2,555),
    IncomeTaxQuickLookupItem(1500,0.1,105),
    IncomeTaxQuickLookupItem(0,0.03,0)
]
    
class Args(object):
    def __init__(self):
        self.args=sys.argv[1:]
    def _get_init(self,option):
        try:
            index=self.args.index(option)
            return self.args[index+1]
        except(ValueError,IndexError):
            print('ValueError,IndexError')
   
    @property
    def config_path(self):
        return self._get_init('-c')
    
    @property
    def userdata_path(self):
        return self._get_init('-d')

    @property
    def userpay_path(self):
        return self._get_init('-o')

args=Args()

class Config(object):
    def __init__(self):
        self.config=self._read_config()
    def _read_config(self):
        config={}
        configpath=args.config_path
        try:
            with open(configpath) as file:
                for eline in file.readlines():
                    key,value=eline.strip().split(' = ')
                    config[key.strip()]=float(value.strip())
        except ValueError:
             print('config error')
             exit()
        return config
    def _get_config(self,key):
         try:
             return self.config[key]
         except KeyError:
             print('KeyError!')
             exit()
    @property
    def ins_low(self):
         try:
             return self._get_config('JiShuL')
         except KeyError:
             print('Not exists!')
    @property
    def ins_high(self):
         try:
             return self._get_config('JiShuH')
         except KeyError:
             print('Not exists!')
    @property
    def ins_sum(self):
         return sum([
                     self._get_config('YangLao'),
                     self._get_config('YiLiao'),
                     self._get_config('ShiYe'),
                     self._get_config('GongShang'),
                     self._get_config('ShengYu'),
                     self._get_config('GongJiJin')
                   ])

config=Config()

class Userdata(object):
    def __init__(self):
        self.userdata=self._read_userdata()
    def _read_userdata(self):
        _userdata=[]
        userdata_file=args.userdata_path
        with open(userdata_file) as file:
            for eline in file.readlines():
                try:
                    userID,income_string=eline.strip().split(',')
                    income=int(income_string)
                except ValueError:
                    print('Income num is not available')
                    exit()
                _userdata.append((userID,income))
        return _userdata

    def __iter__(self):
        return iter(self.userdata)

class IncomeCalculator(object):
    def __init__(self,userdata):
        self.userdata=userdata
    
    @staticmethod
    def cal_ins(income):
        ins_money=0
        if(income<config.ins_low):
            ins_money=config.ins_low*config.ins_sum
        elif(income>config.ins_high):
            ins_money=config.ins_high*config.ins_sum
        else:
            ins_money=income*config.ins_sum
        return ins_money
   
    @classmethod 
    def cal_tax(cls,income):
        after_ins_money=income-cls.cal_ins(income)
        tax=0
        after_tax_money=after_ins_money
        tax_part=after_ins_money-3500
        if tax_part<=0:
            return '0.00','{:.2f}'.format(after_ins_money)
        for item in Income_Tax_Quick_Lookup_Table:
            if tax_part>item.Start_Point:
                tax=tax_part*item.Tax_rate-item.Quick_Cal
                after_tax_money=after_ins_money-tax
                return '{:.2f}'.format(tax),'{:.2f}'.format(after_tax_money)

    def calc_for_all_userdata(self):
         result=[]
         for userid,income in self.userdata:
             data=[userid,income]
             ins_money='{:.2f}'.format(self.cal_ins(income))   
             tax,ati=self.cal_tax(income)
             data+=[ins_money,tax,ati]
             result.append(data)
         return result
  
    def export(self,default='csv'):
         result=self.calc_for_all_userdata()
         with open(args.userpay_path,'w') as file:
             writer=csv.writer(file)
             writer.writerows(result)

if __name__=='__main__':
    cal=IncomeCalculator(Userdata())
    cal.export()




        



         


