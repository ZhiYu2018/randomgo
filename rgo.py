#!/usr/bin/python
# -*- coding: UTF-8 -*-

from __future__ import division
import random
import time


def _int32(x):
    return int(0xFFFFFFFF & x)

##梅森旋转算法##
class MT19937:
    def __init__(self, seed):
        self.mt = [0] * 624
        self.mt[0] = seed
        for i in range(1, 624):
            self.mt[i] = _int32(1812433253 * (self.mt[i - 1] ^ self.mt[i - 1] >> 30) + i)
    ''''''
    def extract_number(self):
        self.twist()
        y = self.mt[0]
        y = y ^ y >> 11
        y = y ^ y << 7 & 2636928640
        y = y ^ y << 15 & 4022730752
        y = y ^ y >> 18
        return _int32(y)
    ''''''
    def twist(self):
        for i in range(0, 624):
            y = _int32((self.mt[i] & 0x80000000) + (self.mt[(i + 1) % 624] & 0x7fffffff))
            self.mt[i] = y ^ self.mt[(i + 397) % 624] >> 1
            if y % 2 != 0:
                self.mt[i] = self.mt[i] ^ 0x9908b0df 
    ''''''

class Sku:
    ''''''
    def __init__(self, cost, price):
        ''''''
        self.cost = cost
        self.price = price
    
    def getCost(self):
        ''''''
        return self.cost
    
    def getPrice(self):
        ''''''
        return self.price
    
    

class User:
    ''''''
    def __init__(self,uid):
        ''''''
        self.user_cost = 0
        self.vm_cost   = 0
        self.user_get  = 0
        self.vm_get    = 0
        self.uid       = uid
        
    
    def add(self, price, src_price, src_cost):
        ''''''
        ##user cost##
        self.user_cost = self.user_cost + price
        ##user get##
        self.user_get  = self.user_get + src_price
        
        ##vm cost##
        self.vm_cost = self.vm_cost + src_cost
        ##vm get##
        self.vm_get  = self.vm_get + price 
        
    def getUid(self):
        ''''''
        return self.uid
        
    def getVmProfit(self):
        ''''''
        return (self.vm_get - self.vm_cost)
    
    def getUserProfit(self):
        ''''''
        return (self.user_get - self.user_cost)
    
    def getVmCost(self):
        ''''''
        return self.vm_cost
    
    def getUserCost(self):
        ''''''
        return self.user_cost
    
    
    
class LuckyGo:
    ''''''
    def __init__(self, price, price_list, cost_list):
        ''''''
        ##全局销售情况##
        self.vm_cost = 0
        self.vm_get  = 0
        self.user_cost = 0
        self.user_get  = 0
        self.orders  = 0
        ##幸运值##
        self.lucy    = 1000
        self.vm_meet_ratio = 0.15
        self.user_price = price
        
        ##sku 价格表##
        skus = len(price_list)
        self.sku_list = []
        sku_get_list = []
        for i in range(0, len(price_list)):
            ''''''
            sku = Sku(cost_list[i], price_list[i])
            self.sku_list.append(sku)
            sku_get_list.append((price - cost_list[i]))
            ''''''
        ''''''
        ##对获利表进行处理##
        min_get = 1000
        for p in sku_get_list:
            ''''''
            if min_get > p and p > 0:
                ''''''
                min_get = p
            ''''''
        ''''''
        sum_get = 0
        for i in range(0, len(sku_get_list)):
            ''''''
            if sku_get_list[i] < 0:
                ''''''
                sku_get_list[i] = min_get
            ''''''
            sum_get = sum_get + sku_get_list[i]
        ''''''  
        self._userInfos = dict()
        self._sku_lucy_range = []
        
        
        start = 0
        end = 0
        for i in range(0, skus):
            ''''''
            p = sku_get_list[i]/sum_get
            delta = int(self.lucy * p)
            end = start  + delta
            if i == (skus - 1):
                ''''''
                end = self.lucy
            print "%d range [%d,%d) P:%0.2f:%0.2f" % (i, start, end, (end - start)/self.lucy, p)
            self._sku_lucy_range.append((start, end))
            start = end
        ''''''
        ##初始化随机函数，python 用的是 梅森旋转函数，质量比较高##
        random.seed(time.time())
    
    def winCheck(self):
        ''''''
        user_get  = 0
        vm_cost   = 0
        vm_get    = 0
        skus      = len(self._sku_lucy_range)
        for i in range(0, skus):
            ''''''
            luck = self._sku_lucy_range[i]
            p = round((luck[1] - luck[0])/self.lucy, 2)
            sku = self.sku_list[i]
            vm_get = vm_get + round(self.user_price * p, 2)
            vm_cost = vm_cost + round(sku.getCost() * p, 2)
            user_get = user_get + round(sku.getPrice() * p, 2)
        ''''''
        user_cost = vm_get
        print "VM: get %d cost:%d, profit:%s" % (vm_get, vm_cost, (vm_get - vm_cost)/vm_cost)
        print "User:get %d cost:%d, profit:%s" %(user_get, user_cost, (user_get - user_cost)/user_cost)
   
    def checkVmProfit(self):
        ''''''
        ##根据需求，可以适当调整##
        return (self.vm_get - self.vm_cost)
    
    
    def GetBiggerPriceLucky(self, price):
        ''''''
        idx = 0
        ##乘上一个系数：用户不亏的价格##
        lprice = price * 1.1
        for sku in self.sku_list:
            ''''''
            if sku.getPrice() >= lprice:
                ''''''
                break
            ''''''
            idx = idx + 1
        ''''''
        if idx >= len(self._sku_lucy_range):
            ''''''
            idx = idx -1
        ''''''
        lucky = random.randint(self._sku_lucy_range[idx][0], self.lucy)
        return lucky
    
    def GetLowHighPriceLucky(self):
        ''''''
        ##去掉两个最高价：控制用户赢太多##
        idx = len(self.sku_list) - 3
        if idx < 0:
            ''''''
            idx = 0
        ''''''
        lucky = random.randint(0, self._sku_lucy_range[idx][1])
        return lucky
    
        
    def vmWinLucky(self, price, user):
        ''''''
        ##VM 赢##
        if user.getUserProfit() < 0:
            ''''''
            ##用户亏##
            return self.GetBiggerPriceLucky(price)
        elif user.getUserProfit() < price:
            ''''''
            ##用户微赚:全随机##
            return random.randint(0, self.lucy)
        else:
            ''''''
            ##用户大赚:去掉最高价的随机##
            return self.GetLowHighPriceLucky()
        
    def getW2WLucky(self, price):
        ''''''
        ##双赢价格##
        lidx = 10000
        uidx = -1
        mx = len(self.sku_list)
        for i in range(mx):
            ''''''
            sku = self.sku_list[i]
            if sku.getCost() >= price:
                ''''''
                break
            ''''''
            if lidx == 10000:
                ''''''
                lidx = i
            if uidx < i:
                uidx = i
        ''''''
        if lidx >= 10000:
            ''''''
            ##当前价格没有满足要求##
            lidx = 0
        if uidx == -1:
            ''''''
            ##当前价格没有满足要求##
            uidx = 0
        return random.randint(self._sku_lucy_range[lidx][0], self._sku_lucy_range[uidx][1])
    
    def getLowCostLucky(self, price):
        ''''''
        ##我们不亏的价格##
        mx = len(self.sku_list)
        uidx = -1
        for i in range(mx):
            ''''''
            sku = self.sku_list[i]
            if sku.getCost() > price:
                ''''''
                uidx = i - 1
                break
            ''''''
        ''''''
        if uidx < 0:
            ''''''
            ##价格不满足条件##
            uidx = 0
        ''''''
        return random.randint(0, self._sku_lucy_range[uidx][1])
        
    def vmDeficitLucky(self, price, user):
        ''''''
        ##VM 亏损##
        if user.getUserProfit() < 0:
            ''''''
            ##用户亏, 获取当前用户 不亏，我们不亏的价格##
            return self.getW2WLucky(price)
        else:
            ''''''
            ##用户赚，出所有成本价 比price 低的价格##
            return self.getLowCostLucky(price)
            
    
    def userBuy(self, uid, price):
        ''''''
        ##通过用户 盈亏 和vm 盈亏情况，进行动态平衡##
        user = self._userInfos.get(uid)
        if user == None:
            ''''''
            user = User(uid)
            self._userInfos[uid] = user
            ''''''
        ''''''
        lucky = 0
        if user.getUserCost() == 0:
            ''''''
            ##第一次玩，大家都靠运气吧，这里不考虑是否全局亏损，做活动做成这样，也是醉了##
            lucky = random.randint(0, self.lucy)
        else:
            ''''''
            if self.checkVmProfit() > 0:
                ''''''
                ##VM 赚##
                lucky = self.vmWinLucky(price, user)
            else:
                ''''''
                ##VM 亏##
                lucky = self.vmDeficitLucky(price, user)
        ''''''
        i = 0
        for i in range(len(self._sku_lucy_range)):
            ''''''
            lk = self._sku_lucy_range[i]
            if (lk[0] <= lucky) and (lucky < lk[1]):
                ''''''
                break
            ''''''
        ''''''
        if i >= len(self.sku_list):
            ''''''
            i = i - 1
        ##这里可以再做二次调整，就不写了##
            
        ##统计##
        sku = self.sku_list[i]
        user.add(price, sku.getPrice(), sku.getCost())
        
        ##vm 成本 获取统计##
        self.vm_cost = self.vm_cost + sku.getCost()
        self.vm_get  = self.vm_get + price
        
        self.orders  = self.orders + 1
        ##用户成本， 获取统计##
        self.user_cost = self.user_cost + price 
        self.user_get  = self.user_get + sku.getPrice()
        return (sku.getPrice(), lucky)
    ''''''
    def stat_print(self, fos):
        ''''''
        profit = self.vm_get - self.vm_cost
        ratio = profit/self.vm_cost
        ctx = (self.orders, self.vm_get, self.vm_cost, profit, ratio)
        print "Orders:%d, Vm get:%d, Vm cost:%d,Profit:%d,Ratio:%s" % ctx
        fos.write("Orders:%d, Vm get:%d, Vm cost:%d,Profit:%d,Ratio:%s\n" % ctx)
        
        profit = self.user_get - self.user_cost;
        ratio = profit/self.user_cost
        ctx   = (self.orders, self.vm_get, self.vm_cost, profit, ratio)
        print "Orders:%d, User get:%d, User cost:%d,Profit:%d,Ratio:%s" % ctx
        fos.write("Orders:%d, User get:%d, User cost:%d,Profit:%d,Ratio:%s\n" % ctx)
        
        vmdeficit = 0
        userdeficit = 0
        for (k,u) in self._userInfos.items():
            ''''''
            ctx = (u.getUid(), u.getUserProfit(), u.getUserCost(), u.getVmProfit(), u.getVmCost())
            #fos.write("UserId:%d profit %d cost:%d, vm profit:%d vm cost:%d\n" % ctx)
            if u.getUserProfit() < 0:
                ''''''
                userdeficit = userdeficit + 1
            if u.getVmProfit() < 0:
                ''''''
                vmdeficit = vmdeficit + 1
            ''''''
        ''''''
        fos.write("Total user:%d Vm deficit:%d User deficit:%d\n" %(len(self._userInfos),vmdeficit, userdeficit))
                
        
        
    
def test(persons, price, sku_price, sku_cost, fos):
    ''''''
    persion_list = []
    for p in range(persons):
        ''''''
        tp = (p, random.randint(1,10))
        persion_list.append(tp)
        
    ''''''
    ##初始化策略##
    luckyGo = LuckyGo(price, sku_price, sku_cost)
    luckyGo.winCheck()
    for tp in persion_list:
        ''''''
        for t in range(tp[1]):
            ''''''
            skus = luckyGo.userBuy(tp[0], price)
            ##打印情况##
            fos.write("User %d times %d get price:%d Lucky:%d\n" % (tp[0], t, skus[0], skus[1]))
        ''''''
    ''''''
    luckyGo.stat_print(fos)
        
if __name__ == "__main__":
    ''''''
    persons = 10000
    sku_price = [10,12,13,14,15,16,20]
    sku_cost  = [7,8.4,9.1,9.8,10.5,11.2,14]
    price    = 10
    fos = open("./out", "w")
    for i in range(1):
        ''''''
        print "Times:%d" % i
        fos.write("Times:%d\n" % i)
        test(persons, price, sku_price, sku_cost, fos)         
        fos.write("-----------------------------------\n")
        print "---------------------------------------"
    ''''''
    fos.close()
