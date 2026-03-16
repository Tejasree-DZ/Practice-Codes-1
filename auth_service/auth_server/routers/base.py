from fastapi import APIRouter


def make_router(**kwargs) -> APIRouter:
    return APIRouter(**kwargs)