import httpx

origins = [
    "https://dicer.unvisitor.site/store/plugins.json",
    "https://unvisitor.gitee.io/dicer/store/plugins.json",
]


async def get_plugins():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://dicer.unvisitor.site/store/plugins.json")
        result = response.json()

        if "official" in result.keys():
            official = result["official"]
        else:
            official = {}

        if "community" in result.keys():
            community = result["community"]
        else:
            community = {}

        return official, community


async def get_plugins_mixed():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://dicer.unvisitor.site/store/plugins.json")
        result = response.json()

        if "official" in result.keys():
            official = result["official"]
        else:
            official = {}

        if "community" in result.keys():
            community = result["community"]
        else:
            community = {}

        official.update(community)
        return official


async def get_official_plugins():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://dicer.unvisitor.site/store/plugins.json")
        result = response.json()

        if "official" in result.keys():
            official = result["official"]
        else:
            official = {}

        return official


async def get_community_plugins():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://dicer.unvisitor.site/store/plugins.json")
        result = response.json()

        if "community" in result.keys():
            community = result["community"]
        else:
            community = {}

        return community


if __name__ == "__main__":
    import asyncio

    print(asyncio.run(get_plugins()))
