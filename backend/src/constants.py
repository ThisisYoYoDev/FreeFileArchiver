from itertools import cycle

CHUNK_SIZE = 1024 * 1024 * (25 - 1)  # 25MB - 1MB

WEBHOOK_LIST = set([
    "https://discord.com/api/webhooks/1151595851530125374/7Sl0rVMIYtzT29sYCXUy0omsTQVw5ktgrOOtdguqe6JODyQoBZvOq-6-6Yr6ggJUMKLN",
    "https://discord.com/api/webhooks/1151595822656536617/gYNFomgUU6fF5hDNQiOab-Bc133ZGhXJEcLfB1qOXzU-SutVic4Qn9T6mx_R1Juk2eTM",
    "https://discord.com/api/webhooks/1151595925593141300/CLJkT-gsPzgS13aQ7Jr6xXsON3gCEvYH4fYgQ7gxJZRwNkj2-LT84XzGiblVeARSn-KJ",
    "https://discord.com/api/webhooks/1151595886774861825/xDNIpxiemeFTeBLi_RLrbKsOIIhZ2PruMVcADVs-pNbczSmETNRaZQIsmuRLpMQJsFS9",
    "https://discord.com/api/webhooks/1151595907293401179/6zFJjRO-837jMxOv1kClWS4LuZIlx2kFtkdpzCHvr7q-Q48z2z1wgdU_aKPo8-AQ_XEf",
    "https://discord.com/api/webhooks/1151595846450806946/SET94Gl8a5v16Z3QEyX5VLaxeNrsoi0Oel05KoWm7wFBcEulejFCE609_CNdeSVsHupG",
    "https://discord.com/api/webhooks/1151595855749595298/8dnssXcgaBvh6AekHTneY744ma9yzqs-cJpO7fmAdBkcEsy6ZhgS8h4ZJ9kyNdGSNdgs",
    "https://discord.com/api/webhooks/1151595889438232618/1ozT7EoT4laBqL20hks2ZEoSjcxbufDaJ-M5Ssj2aBaIjgpj6ukJWautGQkV2Y_jcsk_",
    "https://discord.com/api/webhooks/1151595820488085655/1bhY8ZcbjiUa9PBK1JeQ-kQ5lfkY1vVEIhQ3m2vkye5X5_GaktDCe0Dy0l79YQbZSA1y",
    "https://discord.com/api/webhooks/1151595832127266868/qBw_gN_a6VJ2ufRdETVYJEZgNvb-v97hrPgnTpPNL6W2BBmvQ3FdX79YXgbnkZMsDz6b",
    "https://discord.com/api/webhooks/1151595858807230586/0R-LW-A6Fn6W6ut5siBGJGX5okOzNFjNbgbNWLgz-DVHe3SB8bwBJHlRgbqi0UIPY57w",
    "https://discord.com/api/webhooks/1151595869330751542/pSZVU6p42dnqA6FRu0e971O2T9IXAZTh1_O-agUALM_p44KkOVyoMAQjNkNh8F1rLxce",
    "https://discord.com/api/webhooks/1151595849026117665/3ZYj7ej-PFfR6ytuT4FfmIay7nIrC75EaZdf5B2q93BJiCZpGFr4T-ykX6mElB4UnKCm",
    "https://discord.com/api/webhooks/1151595871721488466/dHrXTnJUa7zkZgfjHju1VfqQSKBiU-tReDhvTPxOdMg85V_5k9vjBUsHRy9Ui1fifRXF",
    "https://discord.com/api/webhooks/1151595912758562888/KD2Q1d4jwuu4Hj1TnnYugqaXOIua9ApyUxFTlKhPfYqKOwi7ef-QE1ZB9dYq7fgVjxZB",
    "https://discord.com/api/webhooks/1151595862414331977/N5X1oN4Fwt9leE33XClohGpJ0uQ2sULM13JEvTLiHWYSpEomAkuDN0Bf6yXUlE6HeJKG",
    "https://discord.com/api/webhooks/1151595865119658126/fQHu8FRBwir1ka2M3I6_z2tlxbPIaS70MsBXmeU_jmldDDPog_-x1dH4XvFivhkg_eyd",
    "https://discord.com/api/webhooks/1151595895255744573/bMcBFyfwOR1X7Gw6T7_YuD3Xb80r1ogRMgP6FoMSQeKsRJ6APr6ii9jHhlCL8ZtS_SRp",
    "https://discord.com/api/webhooks/1151595917594603643/-NKn5TVqYrkhDlpIVLbrvag422uIjEkEWirqpqChN2x9U40NBJhWar4XYqMmT5AoW7w2",
    "https://discord.com/api/webhooks/1151595910384586763/j3I4e_F858nujwlcrNdWpKkQecbBl7HkicCbZpuPVdA9OZOMjA3eVVjxEVYTqIqwvzw6",
    "https://discord.com/api/webhooks/1151595814448287875/tdDUnNcClz2nGXpRmdlJa_8pX86__HHjIz3uJci_SESj3NVVdhIsQqkXl2bC5SlazaRr",
    "https://discord.com/api/webhooks/1151595904747458571/HlWC1xHCADlc9le6Re4G18dxHvAvvBRATnoFYZaJBtPibssSDGlq9LmPzRCumN6yBRRm",
    "https://discord.com/api/webhooks/1151595853484658842/-3cZuyIrB1MctE-W-Wu5Lq0hP65IpFKzA0qmQ26Uv3m5Qk8x1J5R2f76HXPDyiQnTRBw",
    "https://discord.com/api/webhooks/1151595835574996993/mj7aYTdoDKRzx1KfP34wha7gIQ7dMpoNH7kWBm6cEF8gV06XF7B4mxejoh89Wp-piEb0",
    "https://discord.com/api/webhooks/1151595915380006964/WIOKYxxr5kVV90RLiJWiIUrGD1-kfBKjRSulA5nhq0xIxArtkvpcotwC3MPNGYxKui-o",
    "https://discord.com/api/webhooks/1151595897596170271/naLS3NtlRwN35Ex88HUdsKVfSWv_N5hH3aDGjxRGPX9zZMh2LHo32R0KLn1jpzBElXf4",
    "https://discord.com/api/webhooks/1151595837818945605/rPDzHZgPyapJlvJGtiNjeAn-7rj8-2_chuAIEz4pThu9vgdA9itI1jriQFPbSHp1ZjD9",
    "https://discord.com/api/webhooks/1151595922191568947/BgPt1qxp6-7uBqPjz-Xkss3bUglWmAFnleanjoOngA9Jhrj0j1Djl3Sjyyn8afy1pizw",
    "https://discord.com/api/webhooks/1151595877098594367/YDEqdsTw_FzqLCowZPVfKpiKakuXBfoVxhXSfwfZIu_NJqCt5ShuZJqpBPS-qvmF1ph9",
    "https://discord.com/api/webhooks/1151595920098603009/vzFWiIxewuA3Z7PA0T8faU0dMXc0yf5-dOIbu1oqBnGlZiK8SoD6FfxdeoRJXnJunobs",
    "https://discord.com/api/webhooks/1151595817220718714/fbIisvz68hoJ7I9I_2vrxFV-V9MgqD6itnbflEsQ8ej56vqpDDO7oyclwSjfIhQVTqMs",
    "https://discord.com/api/webhooks/1151595891992567849/jGDCkc9zPHMYnxg_iGDGaVtoUAIv-bWl3TrNnCE80SqMkTKpQjOd4KBlGksQYCfx0xR7",
    "https://discord.com/api/webhooks/1151595879489351713/9rCT5EC8r5qSFOEooqqQWnAZRdxgo0N-wxcY7dfVfNNq6jBPTcKHoOr0rN-deFUz0yTl",
    "https://discord.com/api/webhooks/1151595825538023516/4TsOR4GzQl0kn7lK64kWgO6Nju_XZOPeb5S1DyNn3wbt236K8mgvuZjikL5Fkg7ylwVl",
    "https://discord.com/api/webhooks/1151595874170978366/-afFn5PKCj8K45tZ-Cxhs0IiJzpPLyJ4h17mKJzTs_goNHjS8Y7KXHSzh1ImtspMsr7X",
    "https://discord.com/api/webhooks/1151596058829389906/YK8vkiVf7EAmutjeBlnwtPhRzQT7tAbIORorn2UEeNkRE0jQG9NB-jpKQcXPobu1VwSK",
    "https://discord.com/api/webhooks/1151595840134185112/hTITzB9kXkFYdwPAToWvzWxGMdFWNz1ZxdkdY7-z8BecwbdEzaWDMbRiP0oJfUDCjccu",
    "https://discord.com/api/webhooks/1151595843045036114/d6ffV0iXF7BVWPCe-c0ZJhcE-u0HKJRwDudTYl35ChNOfuiRS1iwaLJbZUZSLhlRRaHw",
    "https://discord.com/api/webhooks/1151595900695740499/5LWKOnSgfpIZLFGuSsg9AEw2QQYeow-pawOd-KvjPQ_XZHo5b5HDYSYXHJhdYm-lnnRC",
    "https://discord.com/api/webhooks/1151595828960559175/bzciT1SOyvbVjXLVb_VpQDDvQz-Or2PlZPNBv9bCH9G72QRk3PvhVl0SJ6SeoYkUc_Qd",
    "https://discord.com/api/webhooks/1151595881875906653/hy-zwx0h654PqWIKTxrm25wEP266ZUF-evWhOm5pTfPyXNAWI2vmb0b1s5yb3q7-65qM",
    "https://discord.com/api/webhooks/1151595884430237696/pL6P-yui_sSHr7E_KFhRAzNzvw6SrmOwmc0lkmNWoV78T2m_u18zrmNHQ8qhXbI30UAT"
])

WEBHOOK = cycle(WEBHOOK_LIST)
WEBHOOK_DICT = {webhook: {"x-ratelimit-remaining": None, "x-ratelimit-reset-after": None} for webhook in WEBHOOK_LIST}

KEY = b'Z:!A' * 8  # La taille doit être de 16, 24 ou 32 octets
IV = b'fedcba9876543210'
