import asyncio
import aiofiles
import aiohttp
import re


async def get_data(session, url):
    """Получаем данные от сервера и получаем ссылки для скачивания картинок."""
    print('start init', url, '\n\n')
    async with session.get(url) as response:
        response_json = await response.json()
        response_child = response_json['data']['children']
        tasks = []
        # Проходим по всем постам
        for child in response_child:
            data = child['data']
            # Если пост имеет картику и оценки поста больше 50
            if data.get('post_hint') and data['score'] > 50:
                img_url = data['url']
                re_url = re.sub(r'https://', '', img_url).split('/')[-1]
                img_path = f'img/{re_url}'
                tasks.append(save_img(session, img_url, img_path))
        # Отправляем задачи на скачивание и сохранение картинок.
        await asyncio.gather(*tasks)        
                                

async def save_img(session, img_url, img_path):
    """Скачивает картинку и сохраняем ее на диск."""
    async with session.get(img_url) as response:
        img = await response.read()
        async with aiofiles.open(img_path, mode='wb') as f:
            await f.write(img)


async def main(urls):
    """Создает сессию и задачи задачи."""
    async with aiohttp.ClientSession() as session:
        tasks = [get_data(session, url) for url in urls]
        await asyncio.gather(*tasks)
        

#url for download count=20
url_doomer = 'https://www.reddit.com/r/Doomers/top/.json?count=20'
url_wojak = 'https://www.reddit.com/r/Wojak/top/.json?count=20'
game_meme = 'https://www.reddit.com/r/gamingmemes/top/.json?count=20'
URLS = [url_doomer, url_wojak, game_meme]

asyncio.run(main(URLS))
