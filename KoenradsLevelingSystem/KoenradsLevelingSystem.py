__author__ = 'koenrad'
__version__ = '0.3'

import clr
clr.AddReferenceByPartialName("Pluton")
import Pluton
import math

#globals
weapons = {"Thompson","Bolt Action Rifle","Revolver","Hunting Bow","Stone Spear","Wood Spear","Waterpipe Shotgun","Rock","Bone Knife","Salvaged Axe","Hammer","Salvaged Hammer","Hatchet","Pickaxe","Stone Hatchet","Torch","Salvaged Icepick"}
weaponsDict = {}
animals = {"stag(Clone)","bear(Clone)","wolf(Clone)","boar(Clone)"}
animalsDict = {}

#class
class KoenradsLevelingSystem:
    def On_PluginInit(self):
        if not Plugin.IniExists("ExpTable"):
            ini = Plugin.CreateIni("ExpTable")
            ini.AddSetting("ExpTable", "Thompson", "66")
            ini.AddSetting("ExpTable", "Bolt Action Rifle", "66")
            ini.AddSetting("ExpTable", "Revolver", "135")
            ini.AddSetting("ExpTable", "Hunting Bow", "251")
            ini.AddSetting("ExpTable", "Stone Spear", "358")
            ini.AddSetting("ExpTable", "Wood Spear", "358")
            ini.AddSetting("ExpTable", "Waterpipe Shotgun", "124")
            ini.AddSetting("ExpTable", "Rock", "251")
            ini.AddSetting("ExpTable", "Bone Knife", "355")
            ini.AddSetting("ExpTable", "Salvaged Axe", "410")
            ini.AddSetting("ExpTable", "Hammer", "202")
            ini.AddSetting("ExpTable", "Salvaged Hammer", "256")
            ini.AddSetting("ExpTable", "Hatchet", "280")
            ini.AddSetting("ExpTable", "Pickaxe", "366")
            ini.AddSetting("ExpTable", "Stone Hatchet", "155")
            ini.AddSetting("ExpTable", "Torch", "921")
            ini.AddSetting("ExpTable", "Salvaged Icepick", "199")
            ini.AddSetting("ExpTable", "stag(Clone)", "150")
            ini.AddSetting("ExpTable", "bear(Clone)", "250")
            ini.AddSetting("ExpTable", "wolf(Clone)", "250")
            ini.AddSetting("ExpTable", "boar(Clone)", "150")
            ini.Save()
        ini = Plugin.GetIni("ExpTable")

        weaponsDict["Thompson"] = int(ini.GetSetting("ExpTable", "Thompson"))
        weaponsDict["Bolt Action Rifle"] = int(ini.GetSetting("ExpTable", "Bolt Action Rifle"))
        weaponsDict["Revolver"] = int(ini.GetSetting("ExpTable", "Revolver"))
        weaponsDict["Hunting Bow"] = int(ini.GetSetting("ExpTable", "Hunting Bow"))
        weaponsDict["Stone Spear"] = int(ini.GetSetting("ExpTable", "Stone Spear"))
        weaponsDict["Wood Spear"] = int(ini.GetSetting("ExpTable", "Wood Spear"))
        weaponsDict["Waterpipe Shotgun"] = int(ini.GetSetting("ExpTable", "Waterpipe Shotgun"))
        weaponsDict["Rock"] = int(ini.GetSetting("ExpTable", "Rock"))
        weaponsDict["Bone Knife"] = int(ini.GetSetting("ExpTable", "Bone Knife"))
        weaponsDict["Salvaged Axe"] = int(ini.GetSetting("ExpTable", "Salvaged Axe"))
        weaponsDict["Hammer"] = int(ini.GetSetting("ExpTable", "Hammer"))
        weaponsDict["Salvaged Hammer"] = int(ini.GetSetting("ExpTable", "Salvaged Hammer"))
        weaponsDict["Hatchet"] = int(ini.GetSetting("ExpTable", "Hatchet"))
        weaponsDict["Pickaxe"] = int(ini.GetSetting("ExpTable", "Pickaxe"))
        weaponsDict["Stone Hatchet"] = int(ini.GetSetting("ExpTable", "Stone Hatchet"))
        weaponsDict["Torch"] = int(ini.GetSetting("ExpTable", "Torch"))
        weaponsDict["Salvaged Icepick"] = int(ini.GetSetting("ExpTable", "Salvaged Icepick"))
        animalsDict["stag(Clone)"] = int(ini.GetSetting("ExpTable", "stag(Clone)"))
        animalsDict["bear(Clone)"] = int(ini.GetSetting("ExpTable", "bear(Clone)"))
        animalsDict["wolf(Clone)"] = int(ini.GetSetting("ExpTable", "wolf(Clone)"))
        animalsDict["boar(Clone)"] = int(ini.GetSetting("ExpTable", "boar(Clone)"))

    def On_Command(self, cmd):
        player = cmd.User
        args = cmd.args
        if cmd.cmd.lower() == "help":
            player.MessageFrom("KLS", "Koenrad's Leveling System: /lvl, /kills, /lvl [player name], /kills [player name]")

        if cmd.cmd.lower() == "lvl":
            if len(args) > 0:
                target = getPlayer(player," ".join(args),"KLS")
                if target is not None:
                    userID = target.SteamID
                    suicides = getKey("suicides", userID, 0)
                    deaths = target.Stats.PlayerDeaths - suicides
                    kills = target.Stats.PlayerKills - suicides
                    player.MessageFrom("KLS", "Koenrad's Leveling System: " + target.Name + "'s stats are:" )
                    target.MessageFrom("KLS", "Koenrad's Leveling System: " + player.Name + " just checked your stats with /stats!" )
                else:
                    return
            else:
                player.MessageFrom("KLS", "Koenrad's Leveling System:")
                userID = player.SteamID
                suicides = getKey("suicides", userID, 0)
                deaths = player.Stats.PlayerDeaths - suicides
                kills = player.Stats.PlayerKills - suicides
            if int(deaths) > 0:
                kdr = float(kills)/float(deaths)
            else:
                kdr = int(kills)
            kdr= "{0:.2f}".format(kdr)
            player.MessageFrom("KLS", "KILLS: " + str(kills)+ " | DEATHS: " + str(deaths) + " | KDR: " + str(kdr) + " | SUICIDES: " + str(suicides))
            player.MessageFrom("KLS", "LVL: " + str(getKey("level", userID, 1)) + " | BLOOD: " + str(getKey("exp", userID, 0)))

        if cmd.cmd.lower() == "kills":
            if len(args) > 0:
                target = getPlayer(player," ".join(args),"KLS")
                if target is not None:
                    userID = target.SteamID
                    player.MessageFrom("KLS", "Koenrad's Leveling System: " + target.Name + "'s kills are:" )
                    target.MessageFrom("KLS", "Koenrad's Leveling System: " + player.Name + " just checked your kills with /kills!" )
                else:
                    return
            else:
                player.MessageFrom("KLS", "Koenrad's Leveling System:")
                userID = player.SteamID
            for weapon in weapons:
                player.MessageFrom("KLS", weapon + ": " + str(getKey(weapon, userID, 0)))

        elif cmd.cmd.lower() == "exp":
            if player.Admin:
                giveExp(player.SteamID, 1)
                item = Pluton.InvItem("Wood")
                player.Inventory.Add(item)
                expmodifier = "1." + str(getKey("level", player.SteamID, 1))
                Server.BroadcastFrom("KLS", expmodifier)
                Server.BroadcastFrom("KLS", str(Pluton.InvItem.GetItemID("Wood")))
            else:
                player.MessageFrom("KLS", "So, you found the test function.... You're so clever!")

        elif cmd.cmd.lower() == "purgestats":
            if player.Admin:
                DataStore.Flush("ExpTable")
                DataStore.Flush("exp")
                DataStore.Flush("level")
                for weapon in weapons:
                    DataStore.Flush(weapon)
                player.MessageFrom("KLS", "Player experience, levels and weapon kills cleared!")
            else:
                player.MessageFrom("KLS", "Nigga plz.... Get admin nub!")

    def On_NPCKilled(self, NpcDeathEvent):
        if NpcDeathEvent.Attacker.ToPlayer() is None:
            return
        animalName = NpcDeathEvent.Victim.Name
        attackerID = str(NpcDeathEvent.Attacker.userID)
        attacker = NpcDeathEvent.Attacker
        for animal in animals:
            if animal == animalName:
                exp = modifyExp(animalsDict[animal], attackerID)
                attacker.Command("note.inv 11955 " + str(int(exp)))
                giveExp(attackerID, exp)
                break

    def On_PlayerConnected(self, player):
        playerDict = Plugin.CreateDict()
        playerDict["player"] = player
        Plugin.CreateParallelTimer("OnConnectTimer", 10000, playerDict).Start()
        giveExp(player.SteamID, 0)


    def OnConnectedTimerCallBack(self, timer):
        player = timer.Args["player"]
        giveExp(player.SteamID, 0)
        player.MessageFrom("KLS", "Nigga plz.... Get admin nub!")
        timer.Kill()

    def On_PlayerDied(self, PlayerDeathEvent):
        if PlayerDeathEvent.Attacker.ToPlayer() is None:
            return

        attacker = PlayerDeathEvent.Attacker
        victim = PlayerDeathEvent.Victim
        victimID = str(victim.SteamID)
        attackerID = str(attacker.userID)

        if attackerID == victimID:          #increase suicide count
            incrementKey("suicides", attackerID)
            return
        killerweapon = PlayerDeathEvent._info.Weapon.info.displayname

        for weapon in weapons:
            if weapon == killerweapon:
                exp = modifyExp(weaponsDict[weapon], attackerID)
                attacker.Command("note.inv 11955 " + str(int(exp)))
                giveExp(attackerID, exp)
                incrementKey(weapon,attackerID)
                break

#module methods
def checkLevel(userID, playerExp):
        points = 0
        for level in range(1,100):
            diff = int(level + 300 * math.pow(2, float(level)/7) )
            points += diff
            lvlExp = points/4
            if playerExp < lvlExp:
                DataStore.Add("level",userID,level)
                break
                #return level
        player = Server.FindPlayer(long(userID))
        if player is None:
            return

        altNick = DataStore.Get("nickname", str(userID))
        if altNick is None:
            player.basePlayer.displayName = player.basePlayer.net.connection.username + "[" + str(level) + "]"
            return
        player.basePlayer.displayName = altNick + "[" + str(level) + "]"
        return level

def getKey(table, key, default):
    if not DataStore.ContainsKey(table, key):
            DataStore.Add(table, key, default)
            return default
    else:
        return DataStore.Get(table, key)

def incrementKey(table, key):
    if not DataStore.ContainsKey(table, key):
            DataStore.Add(table, key, 1)
            return
    else:
        val = DataStore.Get(table, key)
        val = int(val) + 1
        DataStore.Add(table, key, val)

def getPlayer(Player, name, sysname):
    player = Server.FindPlayer(name)
    if player is not None:
        return player
    found = False
    for player in Player.basePlayer.activePlayerList:
        for name in name:
            if name in player.displayName:
                found = True
                break
    if found:
        return player
    else:
        Player.MessageFrom(sysname, "Can't find " + name + ".")
        return None

def modifyExp(baseExp, userID):
    lvl = getKey("level", str(userID), 1)
    if int(lvl) > 9:
        expmodifier = "1." + str(lvl)       #this part gets the exp modifier based on level
    else:
        expmodifier = "1.0" + str(lvl)
    return baseExp * float(expmodifier)

def giveExp(userID, expIncrement):     #giveExp(userID, int)
    if not DataStore.ContainsKey("exp", userID):
            DataStore.Add("exp", userID, int(expIncrement))
            return
    else:
        num = int(DataStore.Get("exp", userID))
        num += int(expIncrement)
        DataStore.Add("exp", userID, num)
        checkLevel(userID, num)