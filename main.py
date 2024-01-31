import redis
import time

#підключення до локального сервера
r = redis.Redis(host='localhost', port=6379, db = 0, decode_responses=True)
#творення числового ключа
r.set('counter', 100)
#інкрементування
r.incr('counter')
r.incr('counter')
r.incr('counter', -101)
#декрементування
r.decr("counter")
value = r.get('counter')
print(value)

# Додавання геоданих
r.geoadd('cities', (-97.7431, 30.2672, 'Austin'))
r.geoadd('cities', (-118.2437, 34.0522, 'Los Angeles'))

# Обчислення відстані між двома точками
distance = r.geodist('cities', 'Austin', 'Los Angeles', unit='km')
print(f"Відстань між Austin та Los Angeles: {distance} км")

# Отримання місцеположення
location = r.geopos('cities', 'Austin')
print(f"Місцеположення Austin: {location}")

#робота з рядками
r.set('Hello', 'World')
print(r.get("hello"))

#списки
r.lpush('mylist', 23)
r.lpush('mylist', 22)
r.rpush('mylist', "one")
print(r.lrange('mylist', 0 , -1))

#множини
r.sadd('myset', 'a', 'b', 'c')
print(r.smembers("myset"))

#хешування
r.hset('myhash','field1', 'value')
print(r.hget("myhash", 'field1'))

print(hash("value") == hash("value"))

# Функція для кешування
def get_cached_data(key):
    if r.exists(key):
        print("Отримано з кешу")
        return r.get(key)
    else:
        # Імітація важкої обчислювальної операції
        time.sleep(2)
        value = "дані"
        r.set(key, value, ex=10)  # Зберігання в кеші з часом життя 10 секунд
        return value

# Використання функції
print(get_cached_data('mykey'))  # Завантаження даних і зберігання в кеші
print(get_cached_data('mykey'))  # Отримання даних з кешу