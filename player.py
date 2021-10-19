import networkx as nx
from .arena import Arena


class Player:
    # Network where all players reside
    network = None

    # Average bias between tags
    global_bias = [[0.5, 0.5], [0.5, 0.5]]

    def __init__(self, arena=None, player_id=None, player_info=None, tag=0.5):
        # Check for environment
        assert arena is not None, TypeError('No arena given.')

        # Newborn player parameters
        self.id = player_id
        self.info = player_info
        self.tag = tag
        self.bias = Player.global_bias

        # Initialize network
        Player.network = arena.G

        # For SimPy
        self.env = arena
        self.action = self.env.process(self.run())

    def run(self):
        while True:
            self.play()

    # Prisoner's Dilemma
    def play(self):
        self.interact_with_all_neighbors()
        self.update_strategy()

    def interact_with_all_neighbors(self):
        for player in self.get_neighboring_players():
            # beats me

    def update_strategy(self):
        raise NotImplementedError(self)

    def get_all_nodes(self):
        return Player.network.nodes()

    def get_players(self, tag_id=None, limit_neighbors=False):
        if limit_neighbors:
            players = Player.network.neighbors(self.id)
        else:
            players = self.get_all_nodes()

        if tag_id is None:
            return [Player.network.node[_]['player'] for _ in players]  # return all regardless of tag
        else:
            return [Player.network.node[_]['player'] for _ in players
                    if Player.network.node[_]['player'].tag['id'] == tag_id]

    def get_all_players(self, tag_id=None):
        return self.get_players(tag_id=tag_id, limit_neighbors=False)

    def get_neighboring_players(self, tag_id=None):
        return self.get_players(tag_id=tag_id, limit_neighbors=True)

    def get_neighboring_nodes(self):
        return Player.network.neighbors(self.id)

    def get_player(self, player_id):
        return Player.network.node[player_id]['player']

    def add_node(self, player_type=None, tag=None):
        player_id = int(len(Player.network.nodes()))
        player = player_type(self.env, player_id=player_id, tag=tag)
        Player.network.add_node(player_id, {'player': player})
        return player_id


    def add_edge(self, player_id1, player_id2):
        if player_id1 in Player.network.nodes(data=False):
            if player_id2 in Player.network.nodes(data=False):
                Player.network.add_edge(player_id1, player_id2)
            else:
                raise ValueError('\'Player 2\'[{}] doesn\'exist'.format(player_id2))
        else:
            raise ValueError('\'Player 1\'[{}] doesn\'exist'.format(player_id1))

    def remove_node(self, player_id):
        Player.network.remove_node(player_id)

    def die(self):
        self.remove_node(self.id)