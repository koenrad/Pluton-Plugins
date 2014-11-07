__author__ = 'koenrad'
__version__ = '0.2'

import clr
clr.AddReferenceByPartialName("Pluton")
import Pluton

class NameChanger:
    AdminOnly = True
    LimitChars = True
    ValidChars = ""
    def On_PluginInit(self):
        if not Plugin.IniExists("NameChanger"):
            ini = Plugin.CreateIni("NameChanger")
            ini.AddSetting("NameChanger", "AdminOnly", "true")
            ini.AddSetting("NameChanger", "LimitChars", "true")
            ini.AddSetting("NameChanger", "ValidChars", "abcdefghijklmnopqrstuvwxyz 0123456789")
            ini.Save()
        ini = Plugin.GetIni("NameChanger")
        self.AdminOnly = ini.GetBoolSetting("NameChanger", "AdminOnly", True)
        self.LimitChars = ini.GetBoolSetting("NameChanger", "LimitChars", True)
        self.ValidChars = ini.GetSetting("NameChanger", "ValidChars")

    def On_Command(self, cmd):
        player = cmd.User
        args = cmd.args
        if cmd.cmd.lower() == "help":
            if self.AdminOnly:
                if not player.Admin:
                    return
            player.MessageFrom("NameChanger", "/setnick [nickname], /removenick")

        if cmd.cmd.lower() == "setnick":
            if len(args) > 0:
                if self.AdminOnly:
                    if not player.Admin:
                        player.MessageFrom("NameChanger", "Command not found")
                        return
                altNick = " ".join(args)
                if self.LimitChars: #Check name for valid chars
                    valid = False
                    for nchar in altNick:
                        for vchar in self.ValidChars:
                            if nchar == vchar:
                                valid = True
                                break
                        if not valid:
                            player.MessageFrom("NameChanger", "Invalid character: " + nchar)
                            return
                if DataStore.Get("origname", str(player.SteamID)) is None:
                    DataStore.Add("origname", str(player.SteamID), player.basePlayer.displayName)
                DataStore.Add("nickname", str(player.SteamID), altNick)
                player.basePlayer.displayName = altNick
                player.MessageFrom("NameChanger", "Your new nickname is " + altNick)
            else:
                if self.AdminOnly:
                    if not player.Admin:
                        player.MessageFrom("NameChanger", "Command not found")
                        return
                player.MessageFrom("NameChanger", "Use /setnick [new name] to change your name")

        if cmd.cmd.lower() == "removenick":
            if self.AdminOnly:
                if not player.Admin:
                    player.MessageFrom("NameChanger", "Command not found")
                    return
            origName = DataStore.Get("origname", str(player.SteamID))
            if origName is None:
                player.MessageFrom("NameChanger", "Your name was never changed")
                return
            player.basePlayer.displayName = origName
            DataStore.Remove("nickname", str(player.SteamID))
            player.MessageFrom("NameChanger", "Nickname removed")

    def On_Chat(self, msg):
        if msg.User.basePlayer.displayName != msg.User.basePlayer.net.connection.username:
            msg.BroadcastName = msg.User.basePlayer.displayName
            return
        altNick = DataStore.Get("nickname", str(msg.User.SteamID))
        if altNick is None:
            return
        msg.BroadcastName = altNick