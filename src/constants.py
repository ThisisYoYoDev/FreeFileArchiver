from itertools import cycle

CHUNK_SIZE = 1024 * 1024 * (20 - 5)  # 20MB

WEBHOOK = cycle([
    "https://discord.com/api/webhooks/1132992013638307881/TQQjeRt_-uBAamh4ofZnAhKFB2nft_Fl_8dqYvEyjFTM699_RRS1lBExkOmKGNIBqrsk",
    "https://discord.com/api/webhooks/1139517735081087116/PT-wyWz3YUKY0XiuBnjNKShQqQTLozy6m_ksmPYNMaEky6I9qGcPWD5XQnwAFEa4LwHl",
    "https://discord.com/api/webhooks/1139517830006571059/mcoBE2jkOE36IlHy1wGbaCFsHUOgJbfi-Hr5OVuDZMgrTSXVipn2GqND5EOXG_GGj8so",
    "https://discord.com/api/webhooks/1139517899103535124/cxRHJhcrgXgCLTaRTsYPBP3JuKHvB7pkvGUxIexxNk2tzx_CEK53NSb2zqC-pD0PiDNl"
])

MAX_RETRIES = 20

WAIT_TIME_INITIAL = 0.1