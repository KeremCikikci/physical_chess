import berserk

API_TOKEN = 'lip_I07d8jqSPHAYzacfCumR'
session = berserk.TokenSession(API_TOKEN)
client = berserk.Client(session=session)

game_id = 'VkWGl6tt'

# FETCH MOVES
print(client.games.export(game_id)['moves'])

# FETCH TIME
#print(client.games.export(game_id))


# MAKE MOVE
#berserk.clients.Board(session=session).make_move(game_id, 'd8d5')