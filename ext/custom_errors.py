from discord.ext import commands


# Raised when no sub command is found
class NoSubcommandFound(commands.CommandError):
    pass

# Raised when Whitelist is already in database
class WhitelistAlreadyExists(commands.CommandError):
    pass

# Raised when whitelist is not found
class WhitelistNotFound(commands.CommandError):
    pass

# Raised when Blacklist is already in database
class BlacklistAlreadyExists(commands.CommandError):
    pass

# Raised when blacklist is not found
class BlacklistNotFound(commands.CommandError):
    pass