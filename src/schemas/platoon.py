from typing import Dict

from pydantic import BaseModel


class PlatoonNumberDTO(BaseModel):
    platoon_number: int


class PlatoonDTO(PlatoonNumberDTO):
    vus: int
    semester: int


class CountSquadDTO(BaseModel):
    count: int
