from redis import asyncio as aioredis


class RedisTools:
    __CONNECT_POINT = aioredis.from_url("redis://localhost")

    async def set_value(self, key, value):
        await self.__CONNECT_POINT.set(key, value, 300)

    async def get_value(self, key):
        return await self.__CONNECT_POINT.get(key)

    async def del_value(self, key):
        await self.__CONNECT_POINT.delete(key)

    @property
    def redis_config(self):
        return self.__CONNECT_POINT
