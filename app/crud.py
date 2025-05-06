# from sqlalchemy.orm import Session
# from app import models, schemas

# # ➕ Создать пользователя
# # Принимает сессию базы данных и данные нового пользователя.
# # Создаёт объект пользователя, добавляет его в БД и возвращает.
# def create_user(db: Session, user: schemas.UserCreate):
#     db_user = models.User(**user.dict())  # Создаём экземпляр модели User из данных схемы
#     db.add(db_user)                       # Добавляем в сессию
#     db.commit()                           # Фиксируем изменения в базе данных
#     db.refresh(db_user)                   # Обновляем объект, чтобы получить сгенерированный ID
#     return db_user                        # Возвращаем созданного пользователя

# # 📄 Получить пользователя по ID
# # Возвращает одного пользователя из БД по его идентификатору.
# def get_user(db: Session, user_id: int):
#     return db.query(models.User).filter(models.User.id == user_id).first()

# # 📄 Получить список всех пользователей
# # Возвращает список пользователей с возможностью пропуска и ограничения количества.
# def get_users(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.User).offset(skip).limit(limit).all()

# # ✏️ Обновить пользователя
# # Обновляет данные существующего пользователя. Если пользователь не найден — возвращает None.
# def update_user(db: Session, user_id: int, user: schemas.UserUpdate):
#     db_user = db.query(models.User).filter(models.User.id == user_id).first()  # Ищем пользователя
#     if not db_user:
#         return None  # Если не найден — возвращаем None
#     for var, value in vars(user).items():  # Проходимся по полям, обновляем только непустые
#         if value is not None:
#             setattr(db_user, var, value)
#     db.commit()          # Сохраняем изменения
#     db.refresh(db_user)  # Обновляем объект
#     return db_user       # Возвращаем обновлённого пользователя

# # ❌ Удалить пользователя
# # Удаляет пользователя из базы данных. Если не найден — возвращает None.
# def delete_user(db: Session, user_id: int):
#     db_user = db.query(models.User).filter(models.User.id == user_id).first()
#     if not db_user:
#         return None
#     db.delete(db_user)  # Удаляем из базы
#     db.commit()         # Фиксируем изменения
#     return db_user      # Возвращаем удалённого пользователя
