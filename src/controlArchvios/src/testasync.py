import os
import asyncio




async def contar(num_p):
    for i in range(1,6):
        await asyncio.sleep(1)
        print(str(num_p)+str(i))

async def main():
    for i in range(0,3):
        asyncio.create_task(contar(i))
    
    while True:
        print('--')
        await asyncio.sleep(1)


asyncio.run(main())