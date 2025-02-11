from __future__ import annotations

import logging
import uuid
from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands

from src.utils import DiscordIdType, InterfaceType


if TYPE_CHECKING:
    from main import Oisol

