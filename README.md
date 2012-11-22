Atom register
=============

Модуль расширения моделей для быстрой организации одноразовых
действий (like, confirm, ...).


Пример
======

 **settings**
 
```python
ATOMREGISTER_CODE_LIKE = 1
ATOMREGISTER_CODE_CONFIRM = 2

ATOMREGISTER = {
    'pictures.Picture': {
        'names': 'like',
        'code': ATOMREGISTER_CODE_LIKE,
        'positive_only': True,
    },
    'articles.Fact': {
        'names': 'confirm',
        'code': ATOMREGISTER_CODE_CONFIRM,
        'counter_field': ['confirm_count','confirm_positive_count','confirm_negative_count'],
        'positive_only': False,
    },
}
```

В модель **Picture** добавится несколько методов: set_like:user;   uset_like:user;   is_like:user;   count_like;   users_like.
В модель **Fact**: set_like:user,positive=True;   uset_like:user,positive=True;   is_like:user;   count_like:positive=True;   users_like.
Можно задать свои названия методов в поле **names** только в таком порядке.

**counter_field** указавает поля которые могут быть использованы для хранения количества
зарегистрированных действий с данным кодом. Если поля не существует, оно будет добавлено.

**positive_only** принимать и считать только положительные события.

**code** уникальное значение маркирующее данное действие.

```python
for p in Picture.objects.all():
    if p.is_like(user):
        print "%s was marked!" % str(p)
```
