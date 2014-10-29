from resources.objects.creature import CreatureObject
from java.util import Date
from engine.resources.objects import SWGObject
from services.chat import ChatService
from services.chat import Mail
from services.sui import SUIWindow
from services.sui import SUIService
from services.sui.SUIWindow import Trigger
from services.sui.SUIService import MessageBoxType
from java.util import Vector
from main import NGECore
import sys
import math

# initialize global vars (happens at compile time)
commandArgs = ""
commandLength = 0
actorID = long(0)
targetID = long(0)
tipAmount = 0
bankSurcharge = 0


def setup():
    return
    
def run(core, actor, target, commandString):
    
    # set the global variables
    global actorID
    global targetID
    global commandArgs
    global commandLength
    global tipAmount
    global bankSurcharge

    actorID = actor.getObjectID()
    commandArgs = commandString.split(" ")
    commandLength = len(commandArgs)
    bankSurcharge = int(math.ceil(0.05 * float(tipAmount))) # Accurate tipping tax - prevents floating point error
    
    # Determine type of tip
    if not commandArgs[0].isdigit():
        tipAmount = int(commandArgs[1])
        targetID = core.chatService.getObjectByFirstName(commandArgs[0]).getObjectID();
        if isinstance(commandArgs[2], basestring):
            if not commandArgs[2].lower() == "bank":
                actor.sendSystemMessage('Unrecognized tip command', 0)
                return
        else:
            actor.sendSystemMessage('Unrecognized tip command', 0)
            return
    else: 
        tipAmount = int(commandArgs[0])
        targetID = target.getObjectID()
        if commandLength > 1:
            if isinstance(commandArgs[1], basestring):
                if not commandArgs[1].lower() == "bank":
                    actor.sendSystemMessage('Unrecognized tip command', 0)
                    return
            else:
                actor.sendSystemMessage('Unrecognized tip command', 0)
                return
    
    
    #/tip int || /tip target int
    if commandLength == 1:

        tipAmount = commandArgs[0]
        actorFunds = actor.getCashCredits()
        currentTarget = core.objectService.getObject(target.getObjectId())
        
        if (actor.inRange(target.getPosition(), 100)): # 100 = 10m
            if int(tipAmount) > 0 and int(tipAmount) <= 1000000:
                if actorFunds >= int(tipAmount):
                    currentTarget.addCashCredits(int(tipAmount))  
                    actor.deductCashCredits(int(tipAmount))

                    currentTarget.sendSystemMessage(actor.getCustomName() + ' tips you ' + tipAmount + ' credits.', 0)
                    actor.sendSystemMessage('You successfully tip ' + tipAmount + ' credits to ' + currentTarget.getCustomName() + '.', 0)
                    return
                actor.sendSystemMessage('You lack the cash funds to tip ' + tipAmount + ' credits to ' + currentTarget.getCustomName() + '.', 0)
                return
            actor.sendSystemMessage('Invalid tip amount, set amount between 1 and 1,000,000 credits', 0)
            return
        actor.sendSystemMessage('Target is too far away. Try a wire bank transfer instead.', 0)
        return
    
    #/tip target 30000000 bank
    if commandLength >= 2:
        suiSvc = core.suiService
        suiWindow = suiSvc.createMessageBox(MessageBoxType.MESSAGE_BOX_YES_NO, "@base_player:tip_wire_title", "@base_player:tip_wire_prompt", actor, actor, 10)
        
        returnParams = Vector()
        returnParams.add('btnOk:Text')
        returnParams.add('btnCancel:Text')
        suiWindow.addHandler(0, '', Trigger.TRIGGER_OK, returnParams, handleBankTip)
        suiWindow.addHandler(1, '', Trigger.TRIGGER_CANCEL, returnParams, handleBankTip)
        
        suiSvc.openSUIWindow(suiWindow)
        return
    return

def handleBankTip(core, owner, eventType, returnList):
    core = NGECore.getInstance()
    chatSvc = core.chatService
    actorGlobal = core.objectService.getObject(actorID)
    targetGlobal = 0
    
    #We need to determine how the tip is being delivered, either by /tip 1000 bank (targeted) or /tip name 1000 bank
    if not commandArgs[0].isdigit():
        targetGlobal = core.chatService.getObjectByFirstName(commandArgs[0]);
    else:
        targetGlobal = core.objectService.getObject(targetID)
    actorFunds = actorGlobal.getBankCredits()
    totalLost = int(tipAmount) + bankSurcharge
    
    
    if eventType == 0:
        if int(totalLost) > actorFunds:
            actorGlobal.sendSystemMessage('You do not have ' + str(totalLost) + ' credits (surcharge included) to tip the desired amount to ' + targetGlobal.getCustomName() + '.', 0)
            return
        if int(tipAmount) > 0 and int(actorFunds) >= int(totalLost):
            date = Date()
            targetName = targetGlobal.getCustomName()

            targetMail = Mail()
            targetMail.setMailId(chatSvc.generateMailId())
            targetMail.setTimeStamp((int) (date.getTime() / 1000))
            targetMail.setRecieverId(targetID)
            targetMail.setStatus(Mail.NEW)
            targetMail.setMessage(`tipAmount` + ' credits from ' + actorGlobal.getCustomName() + ' have been successfully delivered from escrow to your bank account')
            targetMail.setSubject('@base_player:wire_mail_subject')
            targetMail.setSenderName('bank')

            actorMail = Mail()
            actorMail.setMailId(chatSvc.generateMailId())
            actorMail.setRecieverId(actorID)
            actorMail.setStatus(Mail.NEW)
            actorMail.setTimeStamp((int) (date.getTime() / 1000))
            actorMail.setMessage('An amount of ' + `tipAmount` + ' credits have been transfered from your bank to escrow. It will be delivered to ' + targetGlobal.getCustomName() + ' as soon as possible.')
            actorMail.setSubject('@base_player:wire_mail_subject')
            actorMail.setSenderName('bank')
            
            targetGlobal.addBankCredits(int(tipAmount))
            actorGlobal.deductBankCredits(int(totalLost))
            actorGlobal.sendSystemMessage('You have successfully sent ' + `tipAmount` + ' bank credits to ' + targetGlobal.getCustomName(), 0)
            targetGlobal.sendSystemMessage('You have successfully received ' + `tipAmount` + ' bank credits from ' + actorGlobal.getCustomName(), 0)
            
            chatSvc.storePersistentMessage(actorMail)
            chatSvc.storePersistentMessage(targetMail)
            chatSvc.sendPersistentMessageHeader(actorGlobal.getClient(), actorMail)
            chatSvc.sendPersistentMessageHeader(targetGlobal.getClient(), targetMail)
            return
        
    else:
        actorGlobal.sendSystemMessage('You lack the bank funds to wire ' + `tipAmount` + ' bank funds to ' + targetGlobal.getCustomName() + '.', 0)
        return
    return