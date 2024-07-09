from app.models.group import Group as GroupModel
from app.crud.base import CRUDbase


group_crud = CRUDbase(GroupModel)
