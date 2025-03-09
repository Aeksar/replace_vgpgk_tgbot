from redis.asyncio.client import Redis

from config.conf import environ, logger

def get_redis_client(host=environ.R_HOST, port=environ.R_PORT, db=environ.R_DB) -> Redis:
    
    try:
        redis_conn = Redis(
            host=host,
            port=port,
            db=db
        )
        logger.debug('Установленно соединение с Redis')
        return redis_conn
    
    except Exception as e:
        logger.error(f'Ошибка при подключени к Redis: {e}')
        raise
    
if __name__ == "__main__":
    try:
        redis_client = get_redis_client() 

        
        redis_client.set('mykey', 'myvalue')
        value = redis_client.get('mykey')
        print(f"Значение по ключу 'mykey': {value}")

    except Exception as e:
        print(f"Не удалось установить соединение с Redis. {e}")