import os
import uuid
from config import Config
from pathlib import Path
from flask import request
from werkzeug.utils import secure_filename
from models import db, MediaFile

from flask_restful import Resource, abort


ALLOWED_EXTENSIONS = 'pdf doc docx png'.split()


def _get_file_path_to_save(filename: str) -> tuple[Path, str]:
    file_name = str(uuid.uuid4()).upper()
    filename_path = Path(filename)
    extension = filename_path.suffix[1:] if filename_path.suffix  else ''

    user_id = 1

    return Path('users', f'{user_id}', f'{file_name}.{extension}'), extension


class FilesResource(Resource):
    def post(self):
        if 'file' not in request.files:
            return {'error': 'No file attached to request'}, 400

        file = request.files['file']

        if file.filename == '':
            return {'error': 'No selected file'}, 400

        if file:
            filename = secure_filename(file.filename)
            relative_path, extension = _get_file_path_to_save(filename)
            absolute_path = Path(Config.MEDIA_ROOT, relative_path)

            print(f'File extension is {extension}')

            os.makedirs(absolute_path.parent, exist_ok=True)
            file.save(absolute_path)

            media_file = MediaFile(
                src=relative_path,
                original_name=filename,
            )

            db.session.add(media_file)
            db.session.commit()

            return media_file.to_dict(), 201
        else:
            return {'error': 'File upload failed'}, 500

    def get(self, file_id: int):
        media_file = MediaFile.query.get(file_id)
        return media_file, 200

    def delete(self, filename):
        return
