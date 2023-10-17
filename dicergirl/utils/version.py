import asyncio
import httpx


async def get_latest_version(package_name):
    """获取当前 Pypi 上`dicergirl`的最新版本号"""
    async with httpx.AsyncClient() as client:
        url = f"https://pypi.org/pypi/{package_name}/json"
        try:
            response = await client.get(url)
        except httpx.ReadTimeout:
            return "0.0.0"

        if response.status_code == 404:
            return "0.0.0"

        package_info = response.json()
        return package_info["info"]["version"]


async def run_shell_command(command):
    """异步执行 shell 指令的原始方法"""
    process = await asyncio.create_subprocess_shell(
        command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )

    stdout, stderr = await process.communicate()

    return {
        "stdout": stdout.decode().strip(),
        "stderr": stderr.decode().strip(),
        "returncode": process.returncode,
    }
