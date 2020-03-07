#!/usr/bin/env python
# -*- coding:utf-8-*-
# encoding=utf-8
from statemachine import StateMachine, State
import random
from Util import isStoreLink, isNegative

class MiscreantAccount(StateMachine):
    getLink = False
    isNeg = False
    firstChat = True
    senderQQ = ''
    senderName = ''
    bestAnswer = ''
    role = 'account'
    
    # initiate the states in the FSM for the account miscreants
    init = State('Initial', initial=True)
    types = State('IntentAndType')
    website = State('Website')
    payment = State('Payment')
    simcard = State('Simcard')
    scalping = State('Scalping')
    end = State('End')

    # define the state transition in this FSM
    askType = init.to(types)
    askWebsite = types.to(website)
    askPayment = website.to(payment)
    askSimcard = payment.to(simcard)
    askScalping = simcard.to(scalping)
    askEnd = scalping.to(end)


    def getAnswer(self, sentence):
        if isStoreLink(sentence) and not self.getLink:
            self.getLink = True
        if isNegative(sentence):
            self.isNeg = True
        answer = ''
        if self.is_init:
            answer = self.askType()
        elif self.is_types:
            answer = self.askWebsite()
            if self.getLink:
                self.askPayment()
                answer = self.askSimcard()
            elif self.isNeg:
                answer = self.noAccount()
        elif self.is_website:
            if self.getLink:
                self.askPayment()
                answer = self.askSimcard()
            else:
                if not self.isNeg:
                    answer = self.askPayment()
                else:
                    self.askPayment()
                    answer = self.askSimcard()
        elif self.is_payment:
            answer = self.askSimcard()
        elif self.is_simcard:
            answer = self.askScalping()
        elif self.is_scalping:
            answer = self.askEnd()
        elif self.is_end:
            answer = "嗯嗯"
        self.isNeg = False
        self.firstChat = False
        return answer

    # callbacks for the FSM when entering each state
    def on_askType(self):
        list1 = [u'老板你好，我想买XXX账号，你现在有什么类型的账号啊',
                 u'hi，我想买XXX账号，老板你卖什么类型的账号',
                 u'我需要XXX账号，老板你卖什么类型的账号啊',
                 u'我想买XXX小号，老板你有什类型的账号啊',
                 u'需要些XXX小号，老板现在有什么种类的呢',
                 u'老板，我需要些XXX小号，你的小号有什么类型的',
                 u'老板，我需要些XXX小号，现在有哪种方式小号安全放心呢']
        return random.choice(list1)

    def noAccount(self):
        list1 = [u'好吧，那你有其他家推荐的吗', 
                 u'那好吧，知道有其他家可以买到吗']
        return random.choice(list1)

    def on_askPrice(self):
        list1 = [u'正常能领券的小号多少钱？',
                   u'领券的白号直接买的话什么价格？',
                   u'嗯，号大概多少钱一个能抢券下单的那种',
                   u'号现在什么价格啦',
                   u'嗯，现在小号一个要多少钱',
                   u'嗯，一般一个号要多少钱',
                   u'嗯，你家小号现在什么价格啦', 
                   u'嗯，小号多少钱个啊']
        return random.choice(list1)

    def on_askWebsite(self):
        list1 = [u'请问都在哪里买? 有自助购号的网站吗',
                 u'什么网站能直接购买吗？',
                 u'有批量卖账号的网站吗发一个呗',
                 u'哪能买小号呢，提供一下链接呗',
                 u'从哪里买呢？有什么网站链接吗',
                 u'怎么买，有什么自助网站链接之类的吗，能不能发一下',
                 u'怎么买啊，能发一下什么网站链接吗']   
        return random.choice(list1)

    def on_askPayment(self):
        list1 = [u'怎么支付啊老板，能发一下收款码吗',
                 u'有什么付款方式，可以发一下收款码吗？',
                 u'收款码能发一下吗,怎么付钱',
                 u'en咋付款呢，收款码啥的能发一下吗',
                 u'那该怎么支付呢，收款码啥的能发一下吗',]
        return random.choice(list1)

    def on_askSimcard(self):
        list1 = [u'好的，谢谢老板。我还想问一下，你这账号关联的手机号码是哪个平台接的啊？',
                 u'好的，谢了。老板你注册帐号的时候，从哪个平台搞这么多手机号的啊？',
                 u'enen谢了老板。对了，你用的哪个接码平台来注册小号啊',
                 u'好的，感谢。老板你是在哪个平台接的手机号码啊',
                 u'嗯，谢谢。能透露下手机号是哪个平台接的吗？']
        return random.choice(list1)

    def on_askScalping(self):
        list1 = [u'老板你知道有什么线报搜集软件吗？',
                 u'哦哦，老板你知道怎么搜集下单优惠信息，有啥子软件工具吗',
                 u'老板知道有什么自动领券下单的软件吗？',
                 u'你家的小号可以用来撸货吗？有没有靠谱的下单群啊',
                 u'小号怎么下单什么地方有下单信息啊',
                 u'老板知道下单有什么好平台吗，返利比较多的']
        return random.choice(list1)

    def on_askEnd(self):
        list1 = [u'ENDEND好的，谢了老板']
        return random.choice(list1)


class MiscreantScalping(StateMachine):
    getLink = False
    isNeg = False
    firstChat = True
    senderQQ = ''
    senderName = ''
    bestAnswer = ''
    role = 'scalping'
    
    # initiate the states in the FSM for the scalping miscreants
    init = State('Initial', initial=True)
    item = State('Item')
    shippingLink = State('ShippingLink')
    account = State('Account')
    other = State('Other')
    end = State('End')

    # define the state transition in this FSM
    askItem = init.to(item)
    askShippingLink = item.to(shippingLink)
    askOther = shippingLink.to(other)
    askAccount = other.to(account)
    askEnd = account.to(end)

    def getAnswer(self, sentence):
        if isStoreLink(sentence) and not self.getLink:
            self.getLink = True
        if isNegative(sentence):
            self.isNeg = True

        answer = ''
        if self.is_init:
            answer = self.askItem()
        elif self.is_item:
            answer = self.askShippingLink()
            if self.isNeg:
                answer = self.noItem()
        elif self.is_shippingLink:
            answer = self.askOther()
        elif self.is_other:
            answer = self.askAccount()
        elif self.is_account:
            answer = self.askEnd()
        elif self.is_end:
            answer = "嗯嗯"
        self.isNeg = False
        self.firstChat = False
        return answer

    # callbacks for the FSM when entering each state
    def on_askItem(self):
        list1 = [u'老板，现在有什么XX的下单方案吗',
                 u'老板，请问有啥XX下单方案吗',
                 u'老板，有没有XX下单方案啊',
                 u'请问现在有啥XX下单方案吗，老板',
                 u'老板请问有啥XX下单方案吗',
                 u'老板，现在有啥XX下单方案吗',
                 u'请问有什么XX下单方案吗']
        return random.choice(list1)

    def noItem(self):
        list1 = [u'好吧，那有其他家的吗', 
                 u'那好吧，其他方案都没有吗']
        return random.choice(list1)

    def on_askShippingLink(self):
        list1 = [u'下完单地址发给谁呢？弄完了在哪里查单啊，有链接吗', 
                 u'下单到哪个地址啊老板，怎么报单啊', 
                 u'寄到哪个收货地址啊，怎么报单呢', 
                 u'寄送信息怎么写，能给个报单查单地址吗', 
                 u'收货地址和付款方式怎么弄', 
                 u'下了单寄到哪个地址啊，有报单链接吗']
        return random.choice(list1)

    def on_askOther(self):
        list1 = [u'老板，能透露下你用的什么线报搜集软件啊？', 
                 u'老板你怎么搜集这么多的优惠信息啊，有啥子工具吗', 
                 u'对了老板，知道有什么自动线报收集、领券下单的软件吗？']
        return random.choice(list1)

    def on_askAccount(self):
        list1 = [u'现在下单的小号从哪买到呢，有推荐的卖账号的吗',
                u'老板，下单小号怎样可以批量搞到啊，有推荐的卖账号的吗',
                u'老板有推荐的卖账号的吗',
                u'下单小号哪里搞呀, 有推荐的卖账号的吗',
                u'老板知不知道哪里有下单小号购买',
                u'请教下老板，有推荐的卖账号的吗', 
                u'下单用的账号，老板了解哪有卖的吗', 
                u'下单用的帐号从哪买呢？谢谢']
        return random.choice(list1)

    def on_askEnd(self):
        list1 = [u'ENDEND好的，谢了老板']
        return random.choice(list1)


class MiscreantSimcard(StateMachine):
    getLink = False
    isNeg = False
    firstChat = True
    senderQQ = ''
    senderName = ''
    bestAnswer = ''
    role = 'simcard'
    
    # initiate the states in the FSM for the simcard miscreants
    init = State('Initial', initial=True)
    intent = State('Intent')
    website = State('Website')
    amount = State('Amount')
    account = State('Account')
    other = State('Other')
    end = State('End')

    # define the state transition in this FSM
    askIntent = init.to(intent)
    askWebsite = intent.to(website)
    askAmount = website.to(amount)
    askAccount = amount.to(account)
    askOther = account.to(other)
    askEnd = other.to(end)

    def getAnswer(self, sentence):
        if isStoreLink(sentence) and not self.getLink:
            print( 'ChatEngine:\tGet a link')
            self.getLink = True
        if isNegative(sentence):
            self.isNeg = True
        answer = ''
        if self.is_init:
            answer = self.askIntent()
        elif self.is_intent:
            answer = self.askWebsite()
            if self.getLink:
                answer = self.askAmount()
            elif self.isNeg:
                answer = self.noWebsite()
        elif self.is_website:
            answer = self.askAmount()
            if self.isNeg:
                answer = self.askAccount()
        elif self.is_amount:
            answer = self.askAccount()
        elif self.is_account:
            answer = self.askOther()
        elif self.is_other:
            answer = self.askEnd()
        elif self.is_end:
            answer = "嗯嗯"
        self.isNeg = False
        self.firstChat = False
        return answer

     # callbacks for the FSM when entering each state
    def on_askIntent(self):
        list1 = [u'老板你好，有XXX首次吗，注册账号用的那种',
                 u'hi，老板你有没有XXX的码，首次卡', 
                 u'老板你好，有XXX首次卡吗']
        return random.choice(list1)

    def on_askWebsite(self):
        list1 = [u'在哪个平台或者软件可以对接啊？', 
                 u'请问在哪接码啊，能发一下接码链接吗',
                 u'在什么地方接码，或者软件什么的？',
                 u'接码网站发一个呗',
                 u'哪能接到号呢，提供一下网站或者软件呗',
                 u'从哪里接码呢？有什么网站链接吗',
                 u'怎么买，有什么接码软件、网站之类的吗，能不能发一下',
                 u'怎么接号啊，能发一下什么网站链接吗']   
        return random.choice(list1)

    def noWebsite(self):
        list1 = [u'那好吧，请问有其他家可以买到的吗', 
                 u'好吧，那你还知道其他家谁有吗']
        return random.choice(list1)

    def on_askAmount(self):
        list1 = [u'这批号有多少啊，多久换卡一次呢', 
                 u'这批号量有多少个？以后会换卡吗', 
                 u'这批有多少个号啊，会不会换卡啊', 
                 u'嗯，大概有多少个号吗，还会换卡的吗']
        return random.choice(list1)

    def on_askAccount(self):
        list1 = [u'还想请教下，你知道哪里能直接买到注册好的XXX小号吗？',
                 u'老板，你了解有什么软件能自动注册XXX账号的吗',
                 u'老板你知道哪有注册XXX账号的软件吗？怎么弄到', 
                 u'请问你知道有什么卖XXX小号的地方吗']
        return random.choice(list1)

    def on_askOther(self):
        list1 = [u'能透露一下你这号码是从哪弄的吗', 
                 u'能了解下你家的号码怎么来的吗？', 
                 u'请问你是怎么样弄到这么多的手机号的啊']
        return random.choice(list1)

    def on_askEnd(self):
        list1 = [u'ENDEND好的，谢了老板']
        return random.choice(list1)