async def fetch_name(client, user_id):
    response = client.get(user_id)
    return response["name"]
