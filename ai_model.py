import pandas as pd
from sklearn.ensemble import IsolationForest

def prepare_features(df):
    """
    Convert firewall log data into numeric features
    suitable for anomaly detection.
    """

    data = df.copy()

    protocol_map = {
        "TCP": 1,
        "UDP": 2,
        "ICMP": 3
    }

    action_map = {
        "ALLOW": 0,
        "DENY": 1
    }

    data["protocol"] = data["protocol"].map(protocol_map).fillna(0)
    data["action"] = data["action"].map(action_map).fillna(0)

    features = data[
        [
            "port",
            "bytes",
            "protocol",
            "action"
        ]
    ]

    return features


def detect_anomalies(df):
    """
    Train Isolation Forest on the supplied data and
    assign anomaly labels and risk scores.
    """

    X = prepare_features(df)

    model = IsolationForest(
        contamination=0.10,
        random_state=42
    )

    model.fit(X)

    prediction = model.predict(X)
    score = model.decision_function(X)

    result = df.copy()

    # -1 = anomaly, 1 = normal
    result["anomaly"] = prediction

    # Convert score into 0–100 risk
    risk = (score.max() - score) / (score.max() - score.min() + 1e-6)
    result["risk_score"] = (risk * 100).round(2)

    result["threat_level"] = result["risk_score"].apply(get_level)

    return result


def get_level(score):

    if score >= 80:
        return "Critical"

    elif score >= 60:
        return "High"

    elif score >= 40:
        return "Medium"

    return "Low"
