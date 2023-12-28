import asyncio
import bcrypt

async def verify_password(password: str, bcrypt_hash: str) -> bool:
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(
        None, # default executor,
        bcrypt.checkpw,
        password.encode(),
        bcrypt_hash.encode(),
    )

    return result