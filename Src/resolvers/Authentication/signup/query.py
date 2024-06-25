from prisma import Prisma
from helpers.prisma_connect import connect_to_prisma
from helpers.auth import is_authenticated

prisma = Prisma()


class UserQuery:
    # Listing all users
    async def list_users(self, info):
        is_authenticated(info)
        if await connect_to_prisma(prisma):
            return await prisma.user.find_many(
                order={
                    'id': 'desc'
                }
            )
