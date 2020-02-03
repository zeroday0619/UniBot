from cogs.Twitch.ext.TwitchLiveAlert import StreamAlert

def TLSA(client_id: str, client_secret: str):
    TLSA = StreamAlert(client_id, client_secret)
    return TLSA
