from flask import Blueprint, jsonify, request, abort
from src.services.UserFavoriteService import UserFavoriteService
from src.utils.errors.CustomException import CustomException, MissingKeyException # Errors

main = Blueprint('user_favorite_blueprint',__name__)

@main.route('/<int:user_id>', methods=['GET'], strict_slashes=False)
def get_favorites(user_id):
    try:
        data = UserFavoriteService.get_favorites(user_id)

        return jsonify({'data': {'favorites' : data}, 'success': True})

    except CustomException as ex:
        print(str(ex))
        return CustomException(ex)

@main.route('/', methods=['POST'], strict_slashes=False)
def toggle_favorites():
    try:

        data = request.json
        user_id_key = 'user_id'
        favorites_key = 'favorites'
        
        if user_id_key not in data:
            raise MissingKeyException(user_id_key)

        if favorites_key not in data:
            raise MissingKeyException(favorites_key)

        user_id = request.json[user_id_key]
        favorites = request.json[favorites_key]
    except MissingKeyException as ex:
        print(f'Error: {ex.message}')
        response = jsonify({'message': f"Error: {ex.message}", 'success': False})
        return response,500
    else:
        data = UserFavoriteService.toggle_favorites(user_id, favorites)

        return jsonify({'data': {'favorites' : data}, 'success': True})

