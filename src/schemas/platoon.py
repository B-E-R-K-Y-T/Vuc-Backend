from pydantic import BaseModel


class PlatoonNumber(BaseModel):
    platoon_number: int


class Platoon(PlatoonNumber):
    vus: int
    semester: int


class CountSquad(BaseModel):
    count: int

