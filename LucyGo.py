#!/usr/bin/python
# -*- coding: UTF-8 -*-

from __future__ import division
import random
import time


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
    def __init__(self, price_list, cost_list):
        ''''''
        ##全局销售情况##
        self.vm_cost = 0
        self.vm_get  = 0
        self.user_cost = 0
        self.user_get  = 0
        self.orders  = 0
        ##幸运值##
        self.lucy    = 1000
        self.vm_meet_ratio = -0.1
        
        ##sku 价格表##
        self.sku_list = []
        for i in range(0, len(price_list)):
            ''''''
            sku = Sku(cost_list[i], price_list[i])
            self.sku_list.append(sku)
            ''''''
        ''''''
        self._userInfos = dict()
        self._sku_lucy_range = []
        skus = len(self.sku_list)
        step = int(self.lucy/skus)
        mx  = step * skus
        delt = self.lucy - mx 
        start = 0
        for i in range(0, skus):
            ''''''
            end = 0
            if i == 0:
                ''''''
                end = start + step + delt 
            else:
                ''''''
                end = start + step
            ''''''
            self._sku_lucy_range.append((start, end))
            start = end
        
        ''''''
        ##初始化随机函数，python 用的是 梅森旋转函数，质量比较高##
        random.seed(time.time())
    
    
    def checkMinMeet(self):
        ''''''
        ##可以满足：self.vm_get - self.vm_cost > 0##
        ##是否满足预期## 
        ##vm 利润率##
        if self.vm_get == 0:
            ''''''
            return True
        ''''''
        #ratio = (self.vm_get - self.vm_cost)/self.vm_cost
        #return (ratio >= self.vm_meet_ratio)
        return True
    
    def getBiggerPrice(self, price):
        ''''''
        for sku in self.sku_list:
            ''''''
            if sku.getPrice() > price:
                ''''''
                return sku.getPrice()
            ''''''
        ''''''
        return self.sku_list[len(self.sku_list) - 1].getPrice()
    
    def getLastLowerPrice(self, price):
        ''''''
        l = len(self.sku_list)
        while (l > 0):
            ''''''
            if self.sku_list[l - 1].getPrice() < price:
                ''''''
                break
            ''''''
            l = l - 1
        ''''''
        return self.sku_list[l - 1].getPrice()
        
    
    def getUserLuckyRange(self,down, up):  
        ''''''
        ##获取让用户亏对lucky 值##、
        lk = -1
        skul = len(self.sku_list)
        for i in range(skul):
            ''''''
            sku = self.sku_list[i]
            if sku.getPrice() >= down:
                ''''''
                lk = i
                break 
            ''''''
        ''''''
        if lk < 0:
            ''''''
            lk = (skul - 1)
        
        mk = skul
        while (mk > 0):
            ''''''
            sku = self.sku_list[mk - 1]
            if (sku.getPrice() <= up):
                ''''''
                break
            ''''''
            mk = mk - 1
        ''''''
        if mk < lk:
            ''''''
            mk = lk
        if mk >= skul:
            ''''''
            mk = skul - 1
            
        llucky = self._sku_lucy_range[lk][0]
        mlucky = self._sku_lucy_range[mk][1] - 1
        lucky  = random.randint(llucky, mlucky)
        #print "down:%d up:%d, lk:%d mk:%d, lucky:%d" %(down, up, lk, mk, lucky)
        return lucky
            
        
        
    def getUserWinLucy(self, price, user):
        ''''''
        ##用户赢##
        vmDeficit = user.getVmProfit()
        ##根据vm 输赢情况，动态调整，但整体上，要抑制下用户的盈利##
        lucky = 0
        l  = len(self.sku_list)
        if vmDeficit < 0:
            ''''''
            ##vm 对该用户亏，则要让用户赔##
            up = price
            down = self.sku_list[0].getPrice()
            if self.checkMinMeet() == True:
                ''''''
                ##全局赢的情况下，有一定概率让用户也赢###
                #up = self.getBiggerPrice(price)
                up  = self.sku_list[l - 1].getPrice()
            else:
                ''''''
                ##全局亏，没有办法，得宰你##
                ##price - price * self.vm_meet_ratio##
                up = self.getLastLowerPrice(price)
            ''''''
            lucky = self.getUserLuckyRange(down, up)
        else:
            ''''''
            ##vm 赢， 用户赢##
            down = self.sku_list[0].getPrice()
            up   = 0
            if self.checkMinMeet() == True:
                ''''''
                ##双赢，各安天命##
                up = self.sku_list[l - 1].getPrice()
            else:
                ''''''
                ##全局亏, 没有办法，得宰你##
                ##price - price * self.vm_meet_ratio##
                #up = self.getLastLowerPrice(price)
                up  = self.getBiggerPrice(price)
            ''''''
            lucky = self.getUserLuckyRange(down, up)            
        ''''''
        return lucky 
            
        
    def getDeficitLucy(self, price, user):
        ''''''
        ##用户亏##
        vmDeficit = user.getVmProfit()
        lucky = 0
        ##根据vm 输赢情况 进行动态调整，但是整体上要控制用户亏损##
        l = len(self.sku_list)
        if vmDeficit < 0:
            ''''''
            ##用户亏了， 你还亏， 智商有问题##
            down = self.getBiggerPrice(price)
            up  = self.sku_list[l - 1].getPrice()
            if self.checkMinMeet() == False:
                ''''''
                ##全局亏##
                down = self.getLastLowerPrice(price)
                up   = self.getBiggerPrice(price)
            ''''''
            #####
            lucky = self.getUserLuckyRange(down, up)
        else:
            ''''''
            ##vm 赢###
            down = self.getBiggerPrice(price)
            up  = self.sku_list[l - 1].getPrice()
            lucky = self.getUserLuckyRange(down, up)
        ''''''
        return lucky
        
        
        
    def getUserZeroLucy(self,price ,user):
        ''''''
        ##用户不亏 不赚##
        down = self.sku_list[0].getPrice()
        up   = self.sku_list[len(self.sku_list) - 1].getPrice()
        if self.checkMinMeet():
            ''''''
            ##各安天命##
        else:
            ''''''
            ##没有办法, 亏赢还是要靠运气##
            up = self.getBiggerPrice(price)
        ''''''    
        return self.getUserLuckyRange(down, up)
        
    
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
            ##根据用户盈利情况 和 vm 盈利情况进行决策##
            if user.getUserProfit() > 0:
                ''''''
                ##用户赚##
                lucky = self.getUserWinLucy(price, user)
            elif user.getUserProfit() < 0:
                ''''''
                ##用户亏##
                lucky = self.getDeficitLucy(price, user)
            else:
                ''''''
                ##用户没有亏、赚##
                lucky = self.getUserZeroLucy(price, user)
            ''''''
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
        fos.write("Vm deficit:%d User deficit:%d\n" %(vmdeficit, userdeficit))
                
        
        
    
def test(persons, price, sku_price, sku_cost, fos):
    ''''''
    persion_list = []
    for p in range(persons):
        ''''''
        tp = (p, random.randint(1,10))
        persion_list.append(tp)
        
    ''''''
    ##初始化策略##
    luckyGo = LuckyGo(sku_price, sku_cost)
    for tp in persion_list:
        ''''''
        for t in range(tp[1]):
            ''''''
            skus = luckyGo.userBuy(tp[0], price)
            ##打印情况##
            #fos.write("User %d times %d get %d %d\n" % (tp[0], t, skus[0], skus[1]))
        ''''''
    ''''''
    luckyGo.stat_print(fos)
    
    
if __name__ == "__main__":
    ''''''
    persons = 10000
    sku_price = [3,5,7,9,11,15,17]
    sku_cost  = [1,3,5,7,9,12,14]
    price    = 10
    fos = open("./out", "w")
    
    for i in range(1000):
        ''''''
        print "Times:%d" % i
        fos.write("Times:%d\n" % i)
        test(persons, price, sku_price, sku_cost, fos)         
        fos.write("-----------------------------------\n")
        print "---------------------------------------"
    ''''''
    fos.close()
        