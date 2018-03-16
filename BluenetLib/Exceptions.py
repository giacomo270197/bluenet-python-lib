from enum import Enum


class BleError(Enum):
    CAN_NOT_FIND_SERVICE             = "CAN_NOT_FIND_SERVICE"
    CAN_NOT_FIND_CHACTERISTIC        = "CAN_NOT_FIND_CHACTERISTIC"
    CAN_NOT_GET_CHARACTERISTIC       = "CAN_NOT_GET_CHARACTERISTIC"
    CAN_NOT_FIND_CCCD                = "CAN_NOT_FIND_CCCD"
    NO_NOTIFICATION_DATA_RECEIVED    = "NO_NOTIFICATION_DATA_RECEIVED"
    INVALID_SESSION_NONCE            = "INVALID_SESSION_NONCE"
    INVALID_SESSION_DATA             = "INVALID_SESSION_DATA"
    INVALID_ENCRYPTION_PACKAGE       = "INVALID_ENCRYPTION_PACKAGE"
    INVALID_ENCRYPTION_USER_LEVEL    = "INVALID_ENCRYPTION_USER_LEVEL"
    COULD_NOT_VALIDATE_SESSION_NONCE = "COULD_NOT_VALIDATE_SESSION_NONCE"
    COULD_NOT_READ_SESSION_NONCE     = "COULD_NOT_READ_SESSION_NONCE"
    NO_SESSION_NONCE_SET             = "NO_SESSION_NONCE_SET"
    NO_ENCRYPTION_KEYS_SET           = "NO_ENCRYPTION_KEYS_SET"
    ENCRYPTION_VALIDATION_FAILED     = "ENCRYPTION_VALIDATION_FAILED"

class BluenetBleException(Exception):
    code    = None
    type    = None
    message = None
    
    def __init__(self, type, message, code=0):
        self.type = type
        self.message = message
        self.code = code
        

class BluenetException(Exception):
    code    = None
    type    = None
    message = None
    
    def __init__(self, type, message, code=0):
        self.type = type
        self.message = message
        self.code = code
