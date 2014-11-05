__author__ = 'koenrad'
__version__ = '0.1'

import clr
clr.AddReferenceByPartialName("Pluton")
import Pluton
import sys

belt = {}
inventory = {}
wearables = {}

class SpawnLoadouts:

    def On_PluginInit(self):
        table = 0
        cfg = open(Util.GetPublicFolder() + "\Plugins\SpawnLoadouts\loadouts.cfg").read().splitlines()
        for line in cfg:
            if line[:1] == '[':
                table += 1
                continue
            if table == 1: #belt
                arr = line.split(",")
                belt[arr[0]] = arr[1]
                continue
            if table == 2: #intentory
                arr = line.split(",")
                inventory[arr[0]] = arr[1]
                continue
            if table == 3: #wearables
                arr = line.split(",")
                wearables[arr[0]] = arr[1]
                continue

    def On_Respawn(self, RespawnEvent):
        player = RespawnEvent.Player
        dictionary = Plugin.CreateDict()
        dictionary["player"] = player
        Plugin.CreateParallelTimer("LoadoutTimer", 1000, dictionary).Start()
        item = Pluton.InvItem("Wood")
        player.Inventory.Notice(item)

    def LoadoutTimerCallback(self, timer):
        dictionary = timer.Args
        player = dictionary["player"]

        if player.basePlayer.playerState.state == 0:
            items = player.Inventory.BeltItems()
            loc = player.Location
            loc.Set(0,0,-100)
            items[0].Drop(loc,loc)
            items[1].Drop(loc,loc)

            for item in belt:
                numItems = belt[item]
                itemObj = Pluton.InvItem(item, int(numItems))
                player.Inventory.Add(itemObj, player.Inventory.InnerBelt)
            for item in inventory:
                numItems = inventory[item]
                itemObj = Pluton.InvItem(item, int(numItems))
                player.Inventory.Add(itemObj, player.Inventory.InnerMain)
            for item in wearables:
                numItems = wearables[item]
                itemObj = Pluton.InvItem(item, int(numItems))
                player.Inventory.Add(itemObj, player.Inventory.InnerWear)
            timer.Kill()
    def On_Command(self, cmd):
        Player = cmd.User
        if cmd.cmd.lower() == "help":
            Player.MessageFrom("SL", "SpawnLoadouts by koenrad")