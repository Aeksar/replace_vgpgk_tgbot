from redis.asyncio.client import Redis

from config.conf import environ, logger

def get_redis_client(host=environ.R_HOST, port=environ.R_PORT, db=environ.R_DB) -> Redis:
    
    try:
        redis_conn = Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=True
        )
        logger.debug(f'Установленно соединение с redis://{host}:{port}')
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

            
            await redis_client.set('key', 'val')
            value = await redis_client.get('key')
            await redis_client.delete('key')
            print(f"Значение по ключу 'key': {value}")

        except Exception as e:
            print(f"Не удалось установить соединение с Redis. {e}")
        
    asyncio.run(main())