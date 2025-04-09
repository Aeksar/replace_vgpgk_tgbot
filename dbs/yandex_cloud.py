import yadisk_async
from config.conf import environ, logger
from io import BytesIO


class Cloud:

    def __init__(self):
        self.disk = yadisk_async.YaDisk(token=environ.Y_TOKEN)


    async def upload(self, filepath: str) -> None:
        
        async with self.disk as d: 
            try: 
                await d.upload(filepath, 'bot_files/zameni.docx')
            except yadisk_async.exceptions.PathExistsError:
                await d.remove('bot_files/zameni.docx')
                await d.upload(filepath, 'bot_files/zameni.docx')
            except Exception as e:
                logger.error(f'Ошибка при загрузке файла в облако {e}')
                raise
            finally:
                await d.close()

    async def download(self) -> BytesIO:
        async with self.disk as d:
            try: 
                buf = BytesIO()
                await d.download('bot_files/zameni.docx', buf)
                return buf
            except Exception as e:
                logger.error(f'Ошибка при загрузке файла из облака {e}')
                raise
            finally:
                await d.close()
        
