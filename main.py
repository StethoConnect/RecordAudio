from StethoConnect import StethoConnect 
import asyncio

async def main():
    steth = StethoConnect()
    await steth.record_audio()

asyncio.run(main())