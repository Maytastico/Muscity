from flask import request, abort
from sqlalchemy import or_, text
from flask_restful import Resource, reqparse, fields, marshal_with
from sqlalchemy.sql.expression import true
from flask_jwt_extended import jwt_required
from database.handler import db, AudioFile

title_put_args = reqparse.RequestParser()
title_put_args.add_argument("title", type=str, help="title of the music file")
title_put_args.add_argument("artists", type=str, help="artist of the music file")
title_put_args.add_argument("album", type=str, help="Album of the music file")
title_put_args.add_argument("album_artist", type=str, help="Album artist of the music album")


class TitlesList(Resource):
    def __collect_and_format(results):
        response = {}
        i = 0
        for result in results:
            response[i] = {
                "id": result.id,
                "title": result.title,
                "artists" : result.artists,
                "album" : result.artists,
                "track_lenght" : result.track_lenght,
                "present_on_filesystem" : result.present_on_filesystem
            }
            i = i + 1
        return response;

    @jwt_required()
    def get(self):
        response = {}
        print(request.args.get("title"))
        if "query" in request.args.keys():
            abort(501, "not implemented")
        elif "title" in request.args.keys():
            abort(501, "not implemented")
        elif "artist" in request.args.keys():
            abort(501, "not implemented")
        elif "min_lenght" in request.args.keys():
            abort(501, "not implemented")
        elif "max_lenght" in request.args.keys():
            abort(501, "not implemented")
        else:
            results = AudioFile.query.order_by(AudioFile.file_name).all()
            response = TitlesList.__collect_and_format(results)

        return response, 200

class Titles(Resource):
    @jwt_required()
    def get(self, id):
        results = AudioFile.query.get(id)
        if not results:
            abort(404, "Audio file does not exist")

        response = {
            "id" : results.id,
            "title": results.title,
            "artists" : results.artists,
            "album" : results.artists,
            "file_name" : results.file_name,
            "track_lenght" : results.track_lenght,
            "present_on_filesystem" : results.present_on_filesystem
        }
        return response

    @jwt_required()
    def put(self, id):
        args = title_put_args.parse_args()
        results = AudioFile.query.get(id)
        if not results:
            abort(404, "Audio file does not exist")
        
        modified = False
        if args['title']:
            results.title = args['title']
            modified = True
        if args['artists']:
            results.artists = args['artists']
            modified = True
        if args['album']:
            results.album = args['album']
            modified = True
        if args['album_artist']:
            modified = True
            results.artist_artist = args['album_artist']
        


        response = {
            "id" : results.id,
            "title": results.title,
            "artists" : results.artists,
            "album" : results.album,
            "file_name" : results.file_name,
            "track_lenght" : results.track_lenght,
            "present_on_filesystem" : results.present_on_filesystem
        }
        if modified == True:
            db.session.commit()
            return response, 202
        return response, 200

    @jwt_required()
    def delete(self, id):
        result = AudioFile.query.get(id)
        if not result:
            abort(404, "Audio file does not exist")
        
        db.session.delete(result)
        db.session.commit()
        return {"message":"Deleted successfully"}, 204