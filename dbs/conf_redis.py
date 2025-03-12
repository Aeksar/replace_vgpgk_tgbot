from redis.asyncio.client import Redis

from config.conf import environ, logger

def get_redis_client(host=environ.R_HOST, port=environ.R_PORT, db=environ.R_DB, password=environ.R_PASS, username=environ.R_USER) -> Redis:
    
    try:
        redis_conn = Redis(
            host=host,
            port=port,
            password=password,
            username=username,
            db=db,
            decode_responses=True
        )
        logger.debug('Установленно соединение с Redis')
        return redis_conn
    
    except Exception as e:
        logger.error(f'Ошибка при подключени к Redis: {e}')
        raise
    
if __name__ == "__main__":
    import asyncio
    async def main():
        try:
            redis_client = Redis(
                decode_responses=True
            )

            
            await redis_client.set('mykey', 'myvalue')
            value = await redis_client.get('mykey')
            await redis_client.delete('mykey')
            print(f"Значение по ключу 'mykey': {value}")

        except Exception as e:
            print(f"Не удалось установить соединение с Redis. {e}")
        
    asyncio.run(main())