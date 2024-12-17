from flask import Blueprint, abort, make_response, request, Response
from ..db import db
from app.models.cat import Cat
from .route_utilities import validate_model, create_model, get_models_with_filters

bp = Blueprint("cats_bp", __name__, url_prefix="/cats")

@bp.post("")
def create_cat():
    request_body = request.get_json()
    return create_model(Cat, request_body)
    

@bp.get("")
def get_all_cats():
    return get_models_with_filters(Cat, request.args)

@bp.get("/<cat_id>")
def get_single_cat(cat_id):
    cat = validate_model(Cat,cat_id)
    return cat.to_dict()

@bp.patch("/<cat_id>/pet")
def pet_cat(cat_id):
    cat = validate_model(Cat, cat_id)

    if cat.pet_count is None:
        cat.pet_count = 1
    else:
        cat.pet_count += 1
    
    db.session.commit()

    return cat.to_dict()


@bp.put("/<cat_id>")
def update_cat(cat_id):
    cat = validate_model(Cat,cat_id)
    request_body = request.get_json()

    cat.name = request_body["name"]
    cat.personality = request_body["personality"]
    cat.color = request_body["color"]

    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.delete("/<cat_id>")
def delete_cat(cat_id):
    cat = validate_model(Cat, cat_id)

    db.session.delete(cat)
    db.session.commit()

    return Response(status=204, mimetype="application/json")