import pandas as pd


def detect_attacks(data):

    # Required columns check
    required_columns = ["ip", "action"]

    for col in required_columns:
        if col not in data.columns:
            return pd.DataFrame()


    # Sirf blocked requests lena
    blocked = data[
        data["action"].str.upper() == "BLOCKED"
    ]


    # IP ke blocked attempts count karna
    attack_count = (
        blocked.groupby("ip")
        .size()
        .reset_index(name="attempts")
    )


    # 3 ya zyada attempts suspicious maanenge
    suspicious_ips = attack_count[
        attack_count["attempts"] >= 3
    ]


    return suspicious_ips
