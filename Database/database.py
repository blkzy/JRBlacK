from collections import namedtuple
from pymongo import MongoClient
from datetime import datetime

from Database import MONGOURL, BOTID

import discord

class check:
    """
    Value: Boolean
    return: True or False
    """
    def __init__(self, client=False):
        self.coll = MongoClient(MONGOURL, retryWrites=False)["jrblack"]
        self.client = client

    def guild(self, GuildID:int):
        for x in self.coll["guilds"].find({"GuildID": GuildID}):
            return True
        return False

    def user(self, GuildID:int, MemberID:int):
        for x in self.coll["users"].find({"GuildID": GuildID, "MemberID": MemberID}):
            return True
        return False

    def bot(self, GuildID:int, BotID:int):
        for x in self.coll["bot"].find({"GuildID": GuildID, "BotID": BotID}):
            return True
        return False

class guild:
    """
    return guild info in database(MongoDB)
    """
    def __init__(self, client=False):
        self.coll   = MongoClient(MONGOURL, retryWrites=False)["jrblack"]["guilds"]
        self.tuple  = namedtuple("database_guild", ["status", "text"])
        self.check  = check()
        self.client = client

    def create(self, GuildID:int, GuildOW:int):
        if self.check.guild(GuildID):
            return self.tuple(False, 0)

        json = {"GuildID":     GuildID, 
                "GuildOW":     GuildOW,
                "Config":{
                    "Prefix": ".",
                    "BackgroundW": "False"},
                "ChannelID":{
                    "ChannelNews":       0,
                    "ChannelLogs":       0,
                    "ChannelLogsBan":    0,
                    "ChannelLottery":    0,
                    "ChannelCounter":    0,
                    "ChannelWelcome":    0,
                    "ChannelHardDisk":   0,
                    "ChannelHardDisk2":  0,
                    "ChannelHardDisk3":  0,
                    "ChannelWhitelist":  0,
                    "ChannelSuggestion": 0},
                "RoleID":{
                    "AutoRole":          0,
                    "MuteRole":          0},
                "System":{
                    "XpLevel":"False",
                    "Economy":"False"},
                    "GuildDate": datetime.utcnow()}

        return self.tuple(True, self.coll.insert(json))

    def delete(self, GuildID:int):
        if self.check.guild(GuildID):
            return self.tuple(True, self.coll.delete({"GuildID": GuildID}))

        return self.tuple(False, 0)

    def post_logs(self, GuildID:int, ChannelID:int):
        return self.tuple(True, self.coll.update_one({'GuildID': GuildID}, {'$set':{'ChannelID.ChannelLogs': ChannelID}}))

    def post_autoReact(self, GuildID:int, ChannelID:int):
        return self.tuple(True, self.coll.update_one({'GuildID': GuildID}, {'$set':{'ChannelID.ChannelSuggestion': ChannelID}}))

    def post_harddisk(self, GuildID:int, ChannelID:int):
        return self.tuple(True, self.coll.update_one({'GuildID': GuildID}, {'$set':{'ChannelID.ChannelHardDisk': ChannelID}}))

    def post_harddisk2(self, GuildID:int, ChannelID:int):
        return self.tuple(True, self.coll.update_one({'GuildID': GuildID}, {'$set':{'ChannelID.ChannelHardDisk2': ChannelID}}))

    def post_harddisk3(self, GuildID:int, ChannelID:int):
        return self.tuple(True, self.coll.update_one({'GuildID': GuildID}, {'$set':{'ChannelID.ChannelHardDisk3': ChannelID}}))

    def post_welcome(self, GuildID:int, ChannelID:int):
        return self.tuple(True, self.coll.update_one({'GuildID': GuildID}, {'$set':{'ChannelID.ChannelWelcome': ChannelID}}))

    def post_counter(self, GuildID:int, ChannelID:int):
        return self.tuple(True, self.coll.update_one({'GuildID': GuildID}, {'$set':{'ChannelID.ChannelCounter': ChannelID}}))

    def post_news(self, GuildID:int, ChannelID:int):
        return self.tuple(True, self.coll.update_one({'GuildID': GuildID}, {'$set':{'ChannelID.ChannelNews': ChannelID}}))

    def post_lottery(self, GuildID:int, ChannelID:int):
        return self.tuple(True, self.coll.update_one({'GuildID': GuildID}, {'$set':{'ChannelID.ChannelLottery': ChannelID}}))

    def post_autoRole(self, GuildID:int, RoleID:int):
        return self.tuple(True, self.coll.update_one({'GuildID': GuildID}, {'$set':{'RoleID.AutoRole': RoleID}}))

    def post_muteRole(self, GuildID:int, RoleID:int):
        return self.tuple(True, self.coll.update_one({'GuildID': GuildID}, {'$set':{'RoleID.MuteRole': RoleID}}))

    def post_systemXpLevel(self, GuildID:int):
        if ([x['System']['XpLevel'] for x in self.coll.find({'GuildID':GuildID})])[0] == "True":
            return self.tuple(False, self.coll.update_one({'GuildID': GuildID}, {'$set':{'System.XpLevel': 'False'}}))

        return self.tuple(True, self.coll.update_one({'GuildID': GuildID}, {'$set':{'System.XpLevel': 'True'}}))

    def post_systemEconomy(self, GuildID:int):
        if ([x['System']['Economy'] for x in self.coll.find({'GuildID':GuildID})])[0] == "True":
            return self.tuple(False, self.coll.update_one({'GuildID': GuildID}, {'$set':{'System.Economy': 'False'}}))

        return self.tuple(True, self.coll.update_one({'GuildID': GuildID}, {'$set':{'System.Economy': 'True'}}))

    def post_whitelist(self, GuildID:int, ChannelID:int):
        return self.tuple(True, self.coll.update_one({'GuildID': GuildID}, {'$set':{'ChannelID.ChannelWhitelist': ChannelID}}))

    def get_logs(self, GuildID:int):
        return self.tuple(True, ([x['ChannelID']['ChannelLogs'] for x in self.coll.find({'GuildID':GuildID})])[0])

    def get_autoReact(self, GuildID:int):
        return self.tuple(True, ([x['ChannelID']['ChannelSuggestion'] for x in self.coll.find({'GuildID':GuildID})])[0])

    def get_harddisk(self, GuildID:int):
        return self.tuple(True, ([x['ChannelID']['ChannelHardDisk'] for x in self.coll.find({'GuildID':GuildID})])[0])

    def get_harddisk2(self, GuildID:int):
        return self.tuple(True, ([x['ChannelID']['ChannelHardDisk2'] for x in self.coll.find({'GuildID':GuildID})])[0])

    def get_harddisk3(self, GuildID:int):
        return self.tuple(True, ([x['ChannelID']['ChannelHardDisk3'] for x in self.coll.find({'GuildID':GuildID})])[0])

    def get_welcome(self, GuildID:int):
        return self.tuple(True, ([x['ChannelID']['ChannelWelcome'] for x in self.coll.find({'GuildID':GuildID})])[0])

    def get_counter(self, GuildID:int):
       return self.tuple(True, ([x['ChannelID']['ChannelCounter'] for x in self.coll.find({'GuildID':GuildID})])[0])

    def get_news(self, GuildID:int):
        return self.tuple(True, ([x['ChannelID']['ChannelNews'] for x in self.coll.find({'GuildID':GuildID})])[0])

    def get_lottery(self, GuildID:int):
        return self.tuple(True, ([x['ChannelID']['ChannelLottery'] for x in self.coll.find({'GuildID':GuildID})])[0])

    def get_autoRole(self, GuildID:int):
        return self.tuple(True, ([x['RoleID']['AutoRole'] for x in self.coll.find({'GuildID':GuildID})])[0])

    def get_muteRole(self, GuildID:int):
        return self.tuple(True, ([x['RoleID']['MuteRole'] for x in self.coll.find({'GuildID':GuildID})])[0])

    def get_systemXpLevel(self, GuildID:int):
        return self.tuple(True, ([x['System']['XpLevel'] for x in self.coll.find({'GuildID':GuildID})])[0])

    def get_systemEconomy(self, GuildID:int):
        return self.tuple(True, ([x['System']['Economy'] for x in self.coll.find({'GuildID':GuildID})])[0])

    def get_whitelist(self, GuildID:int):
        return self.tuple(True, ([x['ChannelID']['ChannelWhitelist'] for x in self.coll.find({'GuildID':GuildID})])[0])

class user:
    """
    return user info in database(MongoDB)
    """
    def __init__(self, client=False):
        self.coll   = MongoClient(MONGOURL, retryWrites=False)['jrblack']['users']
        self.tuple  = namedtuple("database_user", ["status", "text"]) 
        self.check  = check()
        self.client = client

    def create(self, GuildID:int, MemberID:int):
        if self.check.user(GuildID, MemberID):
            return self.tuple(False, 0)

        json = {"GuildID":        GuildID,
                "MemberID":       MemberID,
                "Messages":       0,
                "Report":         0,
                "Job":            "False",
                "Background":     "False",
                "Social":{
                    "Facebook":   "False",
                    "Youtube":    "False",
                    "Github":     "False",
                    "Instagram":  "False",
                    "TikTok":     "False",
                    "Twitter":    "False",
                    "Telegram":   "False"},
                "Bank":{
                    "Number":     0,
                    "MoneyHand":  0,
                    "MoneyBank":  0},
                "XpLevel":{
                    "Level":      0,
                    "Xp":         0},
                "Inventory":{
                    "Background": [],
                    "Weapon":     [],
                    "CreditCard": 0},
                "About":          "Sem descrição."
        }

        return self.tuple(True, self.coll.insert(json))

    def delete(self, GuildID:int, MemberID:int):
        if self.check.guild(GuildID):
            return self.tuple(True, self.coll.delete({"GuildID": GuildID, "MemberID": MemberID}))
        return self.tuple(False, 0)

    def post_report(self, GuildID:int, MemberID:int):
        return self.tuple(True, self.coll.update_one({"GuildID": GuildID, "MemberID": MemberID}, {"$inc":{"Report": 1}}))

    def post_messages(self, GuildID:int, MemberID:int):
        return self.tuple(True, self.coll.update_one({"GuildID": GuildID, "MemberID": MemberID}, {"$inc":{"Messages": 1}}))

    def post_about(self, GuildID:int, MemberID:int, About:str):
        return self.tuple(True, self.coll.update_one({"GuildID": GuildID, "MemberID": MemberID}, {"$set":{"About": About}}))

    def post_moneyBank(self, GuildID:int, MemberID:int, Money:int):
        return self.tuple(True, self.coll.update_one({"GuildID": GuildID, "MemberID": MemberID}, {"$inc":{"Bank.MoneyBank": Money}}))

    def post_moneyHand(self, GuildID:int, MemberID:int, Money:int):
        return self.tuple(True, self.coll.update_one({"GuildID": GuildID, "MemberID": MemberID}, {"$inc":{"Bank.MoneyHand": Money}}))

    def post_level(self, GuildID:int, MemberID:int):
        if ([x["XpLevel"]["Level"] for x in self.coll.find({"GuildID":GuildID, "MemberID":MemberID})])[0] < int(([x["XpLevel"]["Xp"] for x in self.coll.find({"GuildID":GuildID, "MemberID":MemberID})])[0] ** (1/4)):
            return self.tuple(True, self.coll.update_one({"GuildID": GuildID, "MemberID": MemberID}, {"$inc":{"XpLevel.Level": 1}}))
        return self.tuple(False, 0)

    def post_xp(self, GuildID:int, MemberID:int):
        return self.tuple(True, self.coll.update_one({"GuildID": GuildID, "MemberID": MemberID}, {"$inc":{"XpLevel.Xp": 2}}))

    def post_background(self, GuildID:int, MemberID:int, Url:str):
        return self.tuple(True, self.coll.update_one({"GuildID": GuildID, "MemberID": MemberID}, {"$set":{"Background": Url}}))

    def post_inventoryBackground(self, GuildID:int, MemberID:int, Url:str):
        return self.tuple(True, self.coll.update_one({"GuildID": GuildID, "MemberID": MemberID}, {"$push":{"Inventory.Background": Url}}))

    def post_inventoryWeapon(self, GuildID:int, MemberID:int, Weapon:str):
        return self.tuple(True, self.coll.update_one({"GuildID": GuildID, "MemberID": MemberID}, {"$push":{"Inventory.Weapon": Weapon}}))

    def post_creditCard(self, GuildID:int, MemberID:int, CardNumber:int):
        return self.tuple(True, self.coll.update_one({"GuildID": GuildID, "MemberID": MemberID}, {"$inc":{"Inventory.CreditCard": CardNumber}}))

    def post_job(self, GuildID:int, MemberID:int, Job:int):
        return self.tuple(True, self.coll.update_one({"GuildID": GuildID, "MemberID": MemberID}, {"$set":{"Job": Job}}))

    def get_report(self, GuildID:int, MemberID:int):
        return self.tuple(True, ([x["Report"] for x in self.coll.find({'GuildID':GuildID, "MemberID": MemberID})])[0])

    def get_messages(self, GuildID:int, MemberID:int):
        return self.tuple(True, ([x["Messages"] for x in self.coll.find({'GuildID':GuildID, "MemberID": MemberID})])[0])

    def get_about(self, GuildID:int, MemberID:int):
        return self.tuple(True, ([x["About"] for x in self.coll.find({'GuildID':GuildID, "MemberID": MemberID})])[0])

    def get_moneyBank(self, GuildID:int, MemberID:int):
        return self.tuple(True, ([x["Bank"]["MoneyBank"] for x in self.coll.find({'GuildID':GuildID, "MemberID": MemberID})])[0])

    def get_moneyHand(self, GuildID:int, MemberID:int):
        return self.tuple(True, ([x["Bank"]["MoneyHand"] for x in self.coll.find({'GuildID':GuildID, "MemberID": MemberID})])[0])

    def get_moneyRank(self, GuildID:int, MemberID:int):
        Rank = []
        Count = 0
        for i in self.coll.find({"GuildID":GuildID}).sort('Bank.MoneyBank', -1).limit(10):
            Count += 1
            Rank.append(f"**{Count}º ➜** <@{i['MemberID']}> - **${i['Bank']['MoneyBank']}**")

        return self.tuple(True, "\n\n".join(Rank))

    def get_level(self, GuildID:int, MemberID:int):
        return self.tuple(True, ([x["XpLevel"]["Level"] for x in self.coll.find({"GuildID":GuildID, "MemberID":MemberID})])[0])

    def get_xp(self, GuildID:int, MemberID:int):
        return self.tuple(True, ([x["XpLevel"]["Xp"] for x in self.coll.find({"GuildID":GuildID, "MemberID":MemberID})])[0])

    def get_background(self, GuildID:int, MemberID:int):
        return self.tuple(True, ([x["Background"] for x in self.coll.find({"GuildID":GuildID, "MemberID":MemberID})])[0])

    def get_inventoryBackground(self, GuildID:int, MemberID:int):
        return self.tuple(True, ([x["Inventory"]["Background"] for x in self.coll.find({"GuildID":GuildID, "MemberID":MemberID})])[0])

    def get_inventoryWeapon(self, GuildID:int, MemberID:int):
        return self.tuple(True, ([x["Inventory"]["Weapon"] for x in self.coll.find({"GuildID":GuildID, "MemberID":MemberID})])[0])

    def get_creditCard(self, GuildID:int, MemberID:int):
        return self.tuple(True, ([x["Inventory"]["CreditCard"] for x in self.coll.find({"GuildID":GuildID, "MemberID":MemberID})]))

    def get_job(self, GuildID:int, MemberID:int):
        return self.tuple(True, ([x["Job"] for x in self.coll.find({"GuildID":GuildID, "MemberID":MemberID})]))

class bot:
    def __init__(self, client):
        self.coll  = MongoClient(MONGOURL, retryWrites=False)["jrblack"]["bot"]
        self.tuple = namedtuple("database_bot", ["status", "text"])
        self.check = check()
        self.client = client

    def create(self, GuildID:int, BotID:int):
        if self.check.bot(GuildID, BotID):
            return self.tuple(False, 0)

        json = {"GuildID": GuildID,
                "BotID": BotID,
                "Lottery":{
                    "Money":5000},
                "Casanik":{
                  "Money": 10000}}

        return self.tuple(True, self.coll.insert(json))

    def delete(self, GuildID:int, BotID:int):
        if not self.check.guild(GuildID):
            return self.tuple(False, 0)
        
        return self.tuple(True, self.coll.delete({"GuildID": GuildID, "BotID": BotID}))

    def post_casanik(self, GuildID:int, BotID:int, Money:int):
        return self.tuple(True, self.coll.update_one({"GuildID": GuildID, "BotID": BotID}, {"$inc":{"Casanik.Money": Money}}))

    def get_casanik(self, GuildID:int, BotID:int):
        return self.tuple(True, ([x["Casanik"]["Money"] for x in self.coll.find({"GuildID":GuildID, "BotID":BotID})]))

print("Database: Conectado!")

"""
class Questions:
    def __init__(self):
        self.coll = MongoClient("mongodb://blackzacky:black12345@ds133659.mlab.com:33659/sapponnetwork", retryWrites=False)["sapponnetwork"]["Questions"]

    def Check(self, Question):
        for x in self.coll.find({"Question": Question}):
            return True
        return False

    def Add(self, GuildID:int, MemberID:int, Question:str, Answer:str):

        self.coll.insert({
            "GuildID": GuildID,
            "MemberID": MemberID,
            "Question": Question,
            "Answer": Answer
       })

class Store:
    def __init__(self):
        self.coll = MongoClient("mongodb://blackzacky:black12345@ds133659.mlab.com:33659/sapponnetwork", retryWrites=False)["sapponnetwork"]["Store"]

    def Check(self, Store):
        for x in self.coll.find({"Store": Store}):
            return True
        return False
    
    def Add(self, GuildID:int):
        self.coll.insert({
            "GuildID": GuildID,
            "Backgrounds":{
                "Background 1":{
                    "Url":"https://i.imgur.com/nhEfmIY.jpg",
                    "Price":10000
                },
                "Background 2":{
                    "Url":"https://i.imgur.com/UM0icxL.jpg",
                    "Price":12000
                },
                "Background 3":{
                    "Url":"https://i.imgur.com/7Lg3aRy.jpg",
                    "Price":13000
                },
                "Background 4":{
                    "Url":"https://i.imgur.com/M1SEbiF.jpg",
                    "Price":14000
                },
                "Background 5":{
                    "Url":"https://i.imgur.com/8zNOkSC.jpg",
                    "Price":16000
                },
                "Background 6":{
                    "Url":"https://i.imgur.com/2ys3opI.jpg",
                    "Price":17000
                },
                "Background 7":{
                    "Url":"https://i.imgur.com/Vsob00Q.jpg",
                    "Price":18000
                },
                "Background 8":{
                    "Url":"https://i.imgur.com/aV6ssxS.jpg",
                    "Price":19000
                },
                "Background 9":{
                    "Url":"https://i.imgur.com/249EcCz.jpg",
                    "Price":20000
                },
                "Background 10":{
                    "Url":"https://i.imgur.com/8GxmCE8.jpg",
                    "Price":5000
                }
            },
            "Weapons":{
                "Pistol":}
        })
"""
