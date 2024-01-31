import bcrypt
import redis


class ShoppingCart:
    def __init__(self):
        self.redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

    def register_user(self, username, password):
        #перевірити чи існує користувач
        if self.redis_client.hexists(username, 'password_hash'):
            print("Користувач вже існує")
            return False
        #створення та зберігання хешу
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.redis_client.hset(username, 'password_hash', password_hash)
        print("Користувач успішно зареєстрований!")
        return True

    def login(self, username, password):
        #перевірка логіну та паролю
        stored_password_hash = self.redis_client.hget(username, 'password_hash')
        if stored_password_hash and bcrypt.checkpw(password.encode('utf-8'), stored_password_hash.encode("utf-8")):
            print(f'Ви увійшли як {username}')
            self.current_user = username
            return True
        else:
            print("Невірний логін або пароль")
            return False

    def add_item(self, item_id, quantity = 1):
        key = f'cart:{self.current_user}:{item_id}'
        if self.redis_client.hexists(key, 'quantity'):
            self.redis_client.hincrby(key, 'quantity', quantity)
        else:
            self.redis_client.hset(key, mapping={'item_id':item_id, 'quantity': quantity})
            print(f"Товар {item_id} додано до кошика")

    def remove(self, item_id):
        key = f'cart:{self.current_user}:{item_id}'
        self.redis_client.delete(key)
        print("Товар видалено з кошика!")

    def update_item_quantity(self, item_id, quantity):
        key = f'cart:{self.current_user}:{item_id}'
        if self.redis_client.hexists(key, 'quantity'):
            self.redis_client.hset(key, 'quantity', quantity)
            print(f'Кількість товару {item_id} оновлено!')
        else:
            print(f'Товар {item_id} не знайдено у кошику!')

cart_app = ShoppingCart()
if cart_app.register_user('user4', '123'):
    if cart_app.login('user4', '123'):
        print("Успіх")