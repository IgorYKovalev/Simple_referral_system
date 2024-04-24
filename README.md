# Реферальная система

[Документация API](http://igor0405.pythonanywhere.com/api/schema/redoc/)

[Swagger UI](http://igor0405.pythonanywhere.com/api/schema/swagger-ui/)

[Регистрация пользователя](http://igor0405.pythonanywhere.com/api/v1/register/)

[Верификация пользователя](http://igor0405.pythonanywhere.com/api/v1/verify/)

[Профиль пользователя](http://igor0405.pythonanywhere.com/api/v1/profile/)

[Активация пригласительного кода](http://igor0405.pythonanywhere.com/api/v1/activate_invite_code/)

[Список приглашенных пользователей](http://igor0405.pythonanywhere.com/api/v1/invited_users/)

## Описание

Простая реферальная система с использованием Django и Django REST Framework.

## Использование

1. **Регистрация пользователя**
   - URL: `/api/v1/register/`
   - Метод: `POST`
   - Входные данные: JSON с номером телефона (`phone_number`)
   - Описание: Регистрирует нового пользователя с указанным номером телефона. Генерирует и отправляет на телефон 4-значный код подтверждения.
   - Пример запроса:
     ```json
     {
         "phone_number": "ваш_номер_телефона"
     }
     ```
   - Пример успешного ответа: `201 Created`

2. **Подтверждение пользователя**
   - URL: `/api/v1/verify/`
   - Метод: `POST`
   - Входные данные: JSON с номером телефона (`phone_number`) и кодом подтверждения (`verification_code`)
   - Описание: Подтверждает пользователя по номеру телефона и коду подтверждения.
   - Пример запроса:
     ```json
     {
         "phone_number": "ваш_номер_телефона",
         "verification_code": "ваш_код_подтверждения"
     }
     ```
   - Пример успешного ответа: `200 OK`

3. **Профиль пользователя**
   - URL: `/api/v1/profile/`
   - Метод: `GET`, `PATCH`
   - Аутентификация: Требуется токен аутентификации
   - `GET`: Возвращает данные о текущем аутентифицированном пользователе, включая инвайт-код и список приглашенных пользователей.
   - `PATCH`: Обновляет данные профиля пользователя, включая инвайт-код.
   - Пример успешного ответа: `200 OK`

4. **Активация инвайт-кода**
   - URL: `/api/v1/activate_invite_code/`
   - Метод: `POST`
   - Входные данные: JSON с инвайт-кодом (`invite_code`)
   - Описание: Активирует инвайт-код пользователя.
   - Пример запроса:
     ```json
     {
         "invite_code": "ваш_инвайт_код"
     }
     ```
   - Пример успешного ответа: `200 OK`

5. **Список приглашенных пользователей**
   - URL: `/api/v1/invited_users/`
   - Метод: `GET`
   - Аутентификация: Требуется токен аутентификации
   - Описание: Возвращает список пользователей, которых пригласил текущий пользователь.
   - Пример успешного ответа: `200 OK`
