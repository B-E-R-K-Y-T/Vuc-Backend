from typing import Dict, List

from pydantic import BaseModel


class PlatoonNumberDTO(BaseModel):
    platoon_number: int


class PlatoonDTO(PlatoonNumberDTO):
    vus: int
    semester: int


class PlatoonDataDTO(BaseModel):
    vus: int
    semester: int


class PlatoonsDTO(BaseModel):
    data: Dict[int, PlatoonDataDTO]


class CountSquadDTO(BaseModel):
    count_squad: int
