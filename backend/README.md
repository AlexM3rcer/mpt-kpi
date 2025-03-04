### Актуализация модулей с помощью [pip-tools](https://pypi.org/project/pip-tools/)
```bash
docker compose -f docker-compose.dev.yml run --rm backend bash
pip-compile -vv requirements.in
pip-compile -vv requirements.dev.in
```

### Обновление модулей (может поломать совместимость)
```bash
docker compose -f docker-compose.dev.yml run --rm backend bash
pip-compile -vv --upgrade requirements.in
pip-compile -vv --upgrade requirements-dev.in
```

### Создание БД без миграций
TODO: сдалать чтобы было с миграциями
Сначала заходишь в интерпритатор flask (Выполнять в корне проекта)

```bash
docker compose -f docker-compose.dev.yml exec backend python -m flask shell
```

Импортируем и создаем для моделей таблицы:

```python
from models import db, Criterion, CertificateMark, CertificateMediaFiles, MediaFile, Certificate, User, Position
db.drop_all()
db.create_all()
```
