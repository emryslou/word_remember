```shell
# run env init
# db init
alembic init alembic
alembic revision -m 'init'
alembic upgrade head

# db upgrade
alembic revision --autogenerate -m "v1"
alembic upgrade head
```