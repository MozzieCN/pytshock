import unittest

from pytshock.api import Api

from pytshock.datastructure import Server, User, Ban, Player


class TestData(unittest.TestCase):
    def setUp(self):
        self.api = Api('vstab', 'Terraria1353', '119.23.209.227', '7878',
                       '871506A8C624FCC7A3B32513985B2D2B0D19BCCB72F43D6A1445B8675F60F45F')
        self.server = Server()

    def testServer(self):
        server = Server()
        print(server.status(players=True, rules=True, api=self.api))

        print(server.broadcast('马上有一波Goblin入侵开始', api=self.api))

    def testOff(self):
        self.server.off(api=self.api)

    def testRawCmd(self):
        self.server.raw_cmd(api=self.api, cmd='/invade goblin 1')

    def testFinduser(self):
        print(User.find(type='name', user='CJ', api=self.api).name)

    def testCreateUser(self):
        print(User.create(type='name', user='RL', password='123456', api=self.api))

    def testAllUser(self):
        all = User.all(self.api)
        print(all)

    def test_update_user(self):
        user = User.find(api=self.api, type='name', user='RL')

        user.password = '1234456677'
        user.update(api=self.api)

    def test_active_list(self):
        print(User.active_list(self.api))

    def test_ban_find(self):
        print(Ban.find(type='name', ban='dd',ip='192.168.0.1', api=self.api))

    def test_ban_create(self):
        print(Ban.create(type='user', user='RL',ip='192.168.0.1', api=self.api, reason='test'))
    def test_ban_list(self):
        print(Ban.all(api=self.api))


    def test_player(self):
        palyers  = Player.all(api=self.api)
        print(palyers[0])

        p = palyer = Player.find(palyers[0].nickname,api=self.api)
        print(p.__dict__)