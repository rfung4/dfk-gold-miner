from dfktools.hero import hero_core
from dfktools.hero.heroes import Heroes

from definitions import DFK_CHAIN_RPC
from web.src.static.loggers import logger

crystalvale_heroes = Heroes(hero_core.CRYSTALVALE_CONTRACT_ADDRESS, DFK_CHAIN_RPC, logger)
