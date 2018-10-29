#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import division
import sys
import time
from decimal import Decimal


def _int32(x):
    return int(0xFFFFFFFF & x)


def get1000Float(f):
    ''''''
    return float(Decimal(f).quantize(Decimal('0.000')))

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

def CheckProbability(x,n, d, price_arry):
    ''''''
    prob = []
    s  = 0
    for p in price_arry:
        ''''''
        s = s + abs(x - p)
    
    r1 = 0
    r2 = 0
    for p in price_arry:
        ''''''
        pi = get1000Float(abs(x - p)/s)
        prob.append(pi)
        if x <= p:
            ''''''
            r1 = r1 + pi
        else:
            r2 = r2 + pi
    print "%s %s" % (r1, r2)
    
    amount = 0
    profit = 0
    i = 0
    for p in price_arry:
        ''''''
        amount = amount + p * prob[i]
        profit = profit + (x - p) * prob[i]
        i = i + 1
    
    amount = get1000Float(amount)
    profit = get1000Float(profit)
    ratio  = get1000Float(profit/amount)
    print "Amount:%d, profit:%d, %s" % (amount, profit, ratio)
    print prob
    if ratio >= (n/d):
        ''''''
        return prob
    else:
        ''''''
        return None
    
class Strategy:
    ''''''
    def __init__(self, price_arry, price):
        ''''''
        self._sku_price = price_arry
        self._ucost = price
        self._positProb = []
        self._ngProb = []
        self._ngp = 0
    
    def checkProbability(self, n, d):
        ''''''
        s1 = 0
        s2 = 0
        for p in self._sku_price:
            ''''''
            if p <= self._ucost:
                ''''''
                s1 = s1 + abs(p - self._ucost)
            else:
                ''''''
                s2 = s2 + abs(p - self._ucost)
        ''''''
        ##计算概率##
        for p in self._sku_price:
            ''''''
            if p <= self._ucost:
                ''''''
                pi = get1000Float(abs(self._ucost - p)/s1)
                self._positProb.append(pi)
            else:
                ''''''
                pi = get1000Float(abs(self._ucost - p)/s2)
                self._ngProb.append(pi)
        
        ##计算两种概率下，输赢情况##
        amount_p = 0
        profit_p = 0
        amount_n = 0
        profit_n = 0
        i_p = 0
        i_n = 0
        for p in self._sku_price:
            ''''''
            if p <= self._ucost:
                ''''''
                ##我们赚##
                pi = self._positProb[i_p]
                amount_p = amount_p + p * pi
                profit_p = profit_p + (self._ucost - p) * pi
                i_p = i_p + 1
            else:
                ''''''
                ##我们亏##
                pi = self._ngProb[i_n]
                amount_n = amount_n + p * pi
                profit_n = profit_n + (self._ucost - p) * pi
                i_n = i_n + 1
            ''''''
        ''''''
        ##打印目前亏损情况##
        amount_p = get1000Float(amount_p)
        amount_n = get1000Float(amount_n)
        profit_p = get1000Float(profit_p)
        profit_n = get1000Float(profit_n)
        print "amount:(%s, %s) profig:(%s,%s)" % (amount_p, amount_n, profit_p, profit_n)
        ##由公式 d*[r*profit_p + (1-r)*profig_n] = n*[r*amount_p + (1-r)*amount_n] ##
        ##求得R##
        n1 = (n * amount_n - d * profit_n)
        d1 = (d * profit_p - d * profit_n + n * amount_n - n * amount_p)
        self._ngp = get1000Float(n1/d1)
        print "ngp:%s" % self._ngp
        if self._ngp < 0 or self._ngp >= 1:
            ''''''
            return False
        
        amount = get1000Float(self._ngp * amount_p + (1 - self._ngp) * amount_n)
        profit = get1000Float(self._ngp * profit_p + (1 - self._ngp) * profit_n)
        print "Amount %s Profit %s, ratio:%s" % (amount, profit, get1000Float(profit/amount))
        if (profit/amount) < (n/d):
            ''''''
            print "Find none such"
            return False
        
        ''''''
        return True
    
    def init_hash(self):
        ''''''
        BASE = 1000
        ##按照前面的计算，三个概率是独立概率，所以随机数要用三个##
        self._rngp  = MT19937(int(time.time()))
        self._rposit = MT19937(int(time.time()) + 1000)
        self._rnp = MT19937(int(time.time()) + 2000)
        self._ngp_lucky = [(0, int(BASE * self._ngp)), (int(BASE * self._ngp), BASE)]
        
        ##Posit##
        self._posit_lucky = []
        start = 0
        for pi in self._positProb:
            ''''''
            end = start + int(BASE * pi)
            self._posit_lucky.append((start, end))
            start = end
        ''''''
        ##Ng##
        self._ng_lucky = []
        start = 0
        for pi in self._ngProb:
            ''''''
            end = start + int(BASE * pi)
            self._ng_lucky.append((start, end))
            start = end
        ''''''
        print "Prob:%d,%d" % (len(self._positProb),len(self._ngProb))
        print "Hash:Poist %d, Ng:%d" % (len(self._posit_lucky), len(self._ng_lucky))
    ''''''
    def getPositPrice(self):
        ''''''
        BASE = 1000
        v = self._rposit.extract_number()%BASE
        i = 0
        for t in self._posit_lucky:
            ''''''
            if (v >= t[0]) and (v < t[1]):
                ''''''
                break
            ''''''
            i = i + 1
        ''''''
        if (i >= len(self._posit_lucky)):
            ''''''
            i = i - 1
        ''''''
        return self._sku_price[i]
        
    def getNgPrice(self):
        ''''''
        BASE = 1000
        v = self._rnp.extract_number()%BASE
        i = 0
        for t in self._ng_lucky:
            ''''''
            if (v >= t[0]) and (v < t[1]):
                ''''''
                break
            ''''''
            i = i + 1
        ''''''
        if (i >= len(self._ng_lucky)):
            ''''''
            i = i - 1
        ''''''
        return self._sku_price[i + len(self._posit_lucky)]
    
    def GetIncentives(self, price):
        ''''''
        for p in self._sku_price:
            ''''''
            if (p > price):
                ''''''
                return p
            
    def getPrice(self):
        ''''''
        BASE = 1000
        lucy = self._rngp.extract_number()%BASE
        ##Lucy 值的算法 可以多种##
        bp = (lucy >= self._ngp_lucky[0][0] and lucy < self._ngp_lucky[0][1])
        if bp == True:
            ''''''
            return self.getPositPrice()
        else:
            ''''''
            return self.getNgPrice()
        ''''''
    ''''''    
class LuckyGo:
    ''''''
    def __init__(self, stg):
        ''''''
        self._rsurprised = MT19937(int(time.time()) + 1000)
        self._stg = stg

            
    def GetSurprised(self):
        ''''''
        ##惊讶将概率##
        #v = self._rsurprised.extract_number() % 1000
        #if (v < 950):
        #    ''''''
        #    return None
        #
        #return self._price[len(self._price) - 1]
        return None
    
    def GetIncentives(self, price):
        ''''''
        return self._stg.GetIncentives(price)
    
    def GetPrice(self):
        ''''''
        return self._stg.getPrice()

    
def test(fos):
    ''''''
    price_arry = [2, 5, 7, 9, 15, 20, 25]
    #pidx = int(14*len(price_arry)/20)
    price = 13
    ####
    stg = Strategy(price_arry, price)
    if stg.checkProbability(2, 10) == False:
        ''''''
        print "Find none probability"
        sys.exit()
    ##初始化奖项##    
    stg.init_hash()
        
    lucyGo = LuckyGo(stg)
    amount = 0
    cost   = 0
    positive = 0
    usersTimes = []
    usersPositive = []
    usersCost = []
    mrt = MT19937(int(time.time()))
    persons = 5000
    for i in range(persons):
        ''''''
        times = (mrt.extract_number() % 30)
        if times < 3:
            ''''''
            times = 3
        usersTimes.append(times)
        usersPositive.append(0)
    ''''''
    #####
    maxOrders = 10000
    buyOrders = 0
    total_Surprised = 0
    for i in range(persons):
        ''''''
        ut = usersTimes[i]
        up = usersPositive[i]
        uc = 0
        ua = 0
        nt = 0
        utotal = 0
        
        for b in range(ut):
            ''''''
            if buyOrders >= maxOrders:
                ''''''
                break
            
            buyOrders = buyOrders + 1
            if buyOrders >= maxOrders:
                ''''''
                break
            cp = lucyGo.GetSurprised()
            if cp == None:
                ''''''
                cp = lucyGo.GetPrice()
            else:
                ''''''
                total_Surprised = total_Surprised + 1
            
            utotal = utotal + 1
            ##为了复购率，如果用户连续两次输，找一个安慰奖给他##
            if (nt >= 2) and (cp < price) and (utotal <= 2):
                ''''''
                ##用户连续输两次，给个安慰奖##
                cp = lucyGo.GetIncentives(price)
                
            ##Blue pay amount##
            amount = amount + price
            ##blue pay cost##
            cost = cost + cp
            ##user amount##
            ua = ua + cp
            ##user cost##
            uc = uc + price
            if price < cp:
                ''''''
                ##用户赢##
                positive = positive + 1
                up = up + 1
                nt = 0
            else:
                ##用户输##
                nt = nt + 1
            ''''''
            ##用户亏太多退出##
            if uc/ua >= 2:
                ''''''
                break
        ''''''
        usersPositive[i] = up
        usersCost.append((ua, uc))
    ''''''
    users = 0
    for i in range(persons):
        ''''''
        uac = usersCost[i]
        if uac[0] <= uac[1]:
            ''''''
            continue
        users = users + 1
        #print "User %d times %d Positive %d, Get:%s " % (i, usersTimes[i], usersPositive[i], (uac[0] - uac[1]))
    ''''''
    print "Total orders:%d" % buyOrders
    print "Users: %d of %d Own,Surprised %d" % (users, persons, total_Surprised)
    print "Amount:%d Cost:%d Positive:%d ratio:%s" % (amount, cost, positive, (amount - cost)/cost)
    fos.write("Amount:%d Cost:%d Positive:%d ratio:%s\n" % (amount, cost, positive, (amount - cost)/cost))
    fos.flush()
    ''''''
    
    
if __name__ == '__main__':
    ''''''
    fos = open("./lucygo.log", "w")
    for i in range(100):
        ''''''
        print "%d:" % i
        test(fos)
        print "------------------------------------------------"
    ''''''
    fos.close()
''''''
