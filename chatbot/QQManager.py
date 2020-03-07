#!/usr/bin/env python
# -*- coding:utf-8-*-
# encoding=utf-8

class INFO(object):
    def __init__(self):
        self.msgBuff = []
        self.senders = {}


from aiocqhttp import CQHttp
import socket, urllib, sys, importlib
from collections import defaultdict


# CoolQ usage:
# https://cqhttp.cc/docs/4.7/#/


# get the criminal's ID and role, like
# 123456, account
# 234567, simcard
# 345678, scalping
def readRoles():
    dic = {}
    for line in open("data/roles.txt"):
        senderQQ = line.split(",")[0]
        role = line.split(",")[1]
        # print(senderQQ)
        # print(role)
        # senderQQ, role = line.strip().split(", ")
        dic[senderQQ] = role
    return dic

bot = CQHttp(api_root='http://127.0.0.1:5700/')
# bot = CQHttp(api_root='http://127.0.0.1:5700/',
#              access_token='your-token',
#              secret='your-secret')

roleDict = readRoles()
# send greeting "hi there?" to start the conversation
greeting = urllib.parse.quote("在吗老板?")
for senderQQ, role in roleDict.items():
    url = "http://127.0.0.1:5700/send_private_msg?user_id=" + senderQQ + "&message=" + greeting
    print(url)
    contents = urllib.request.urlopen(url).read()

HOST, PORT = 'localhost', 50007
sClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sClient.connect((HOST, PORT))

info = INFO()


# # callback of receiving msgs, put the incoming msgs into a msg buffer
# # send the msgs together to the processor with socket
# @bot.on_message('private')
# async def handle_msg(context):
#     print("receive a message")
#     senderQQ = str(context['sender']['user_id'])
#     if senderQQ in roleDict:
#         if senderQQ not in info.senders:
#             info.senders[senderQQ] = context
#         print(senderQQ + " to chatbot: \t" + context['message'])
#         msgText, senderName = context['message'], context['sender']['nickname']
#         if len(msgText) > 0:
#             info.msgBuff.append(senderQQ + " - " + senderName + " - " + msgText)
#             print(info.msgBuff)
#
#
# # this callback will collect the messages in every 15s
# # in case that the role may send multimessages in a row
# @bot.on_meta_event()
# async def handle_meta_event(context):
#     print("meta event")
#     content = " ;; ".join(info.msgBuff)
#     print(content)
#     if len(content) != 0:
#         sClient.send(content.encode('utf-8'))
#         response = sClient.recv(1024).decode('utf-8')
#         reponseList = response.split(" ;; ")
#         for response in reponseList:
#             senderQQ, rspMsg = response.split(" - ")
#             print("chatbot to " + senderQQ + ": \t" + rspMsg)
#             if (rspMsg == "ENDEND"):
#                 continue
#             if len(rspMsg) > 0:
#                 if senderQQ in info.senders:
#                     sender = info.senders.get(senderQQ)
#                     await bot.send(sender, rspMsg)
#         info.msgBuff = []


@bot.on_message('private')
async def handle_msg(context):
    print("receive a message")
    senderQQ = str(context['sender']['user_id'])
    if senderQQ in roleDict:
        if senderQQ not in info.senders:
            info.senders[senderQQ] = context
        print(senderQQ + " to chatbot: \t" + context['message'])
        msgText, senderName = context['message'], context['sender']['nickname']
        if len(msgText) > 0:
            msg = senderQQ + " - " + senderName + " - " + msgText
            print(msg)
            sClient.send(msg.encode('utf-8'))
            response = sClient.recv(1024).decode('utf-8')
            reponseList = response.split(" ;; ")
            print(reponseList)
            for response in reponseList:
                if len(response) == 0:
                    continue
                print(response)
                senderQQ, rspMsg = response.split(" - ")
                print("chatbot to " + senderQQ + ": \t" + rspMsg)
                if (rspMsg == "ENDEND"):
                    continue
                if len(rspMsg) > 0:
                    if senderQQ in info.senders:
                        sender = info.senders.get(senderQQ)
                        await bot.send(sender, rspMsg)


bot.run(host='127.0.0.1', port=8080)
