base_challenge_schema = {
    "type": "object",
    "properties": {
        "Username": {"type": "string"},
        "Challenge": {
            "type": "object",
            "properties": {
                "ChallengeName": {"type": "string"},
                "Session": {"type": "string"},
                "ChallengeResponses": {
                    "type": "object",
                    "properties": {
                        "USERNAME": {"type": "string"},
                        "NEW_PASSWORD": {"type": "string"},
                        "SMS_MFA_CODE": {"type": "string"},
                        "PASSWORD_CLAIM_SIGNATURE": {"type": "string"},
                        "PASSWORD_CLAIM_SECRET_BLOCK": {"type": "string"},
                        "TIMESTAMP": {"type": "string"},
                        "ANSWER": {"type": "string"},
                        "NEW_PASSWORD": {"type": "string"},
                        "SOFTWARE_TOKEN_MFA_CODE": {"type": "string"},
                        "DEVICE_KEY": {"type": "string"},
                        "SRP_A": {"type": "string"},
                        "SESSION": {"type": "string"},
                    },
                    "required": ["USERNAME"]
                }
            },
            "required": ["ChallengeName", "Session", "ChallengeResponses"]
        }
    },
    "required": ["Username", "Challenge"]
}

base_logout_schema = {
    "type": "object",
    "parameters": {
        "Username": {"type": "string"}
    },
    "required": ["Username"]
}
