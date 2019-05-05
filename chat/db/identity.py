from quart import g
from nacl.utils import random


async def create_or_update_identity(key, alias=None):
    access_token = random(64)

    row = await g.conn.fetchrow(
        """
        INSERT INTO identities (key, access_token, alias)
        VALUES ($1, $2, $3)
        ON CONFLICT (key) DO UPDATE SET
            alias=EXCLUDED.alias
        RETURNING *
    """,
        key,
        access_token,
        alias,
    )

    return row


async def get_identity_by_access_token(access_token):
    return await g.conn.fetchrow(
        """
        SELECT * FROM identities
        WHERE access_token=$1
    """,
        access_token,
    )


def serialize_identity(identity):
    return {"id": identity["id"], "key": identity["key"], "alias": identity["alias"]}
