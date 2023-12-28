from enum import Enum

class ApiScope(str, Enum):
    PUBLIC = "public"
    IDENTIFY = "identify"
    DELEGATE = "delegate"
    FORUM_WRITE = "forum.write"
    FRIENDS_READ = "friends.read"
    CHAT_WRITE = "chat.write"

    # thanks lazer
    ALL = "*"