class Server(object):
    url_prefix = '/server'

    @classmethod
    def status(cls, players=True, rules=True, api=None) -> dict:
        api = api or api
        data = {
            'players': players,
            'rules': rules,
        }
        return api.send_request('/status', data)

    #
    def broadcast(self, msg: str, api=None) -> str:
        api = api
        data = {
            'msg': msg
        }
        return api.send_request(self.url_prefix + '/broadcast', data)

    def off(self, confirm=True, nosave=False, api=None):
        api = api
        data = {
            'confirm': confirm,
            'nosave': nosave,
        }
        return api.send_request(self.url_prefix + '/off', data)

    def raw_cmd(self, cmd: str, api=None):
        api = api
        data = {
            'cmd': cmd
        }
        res = api.send_request('/v3/server/rawcmd', data)
        return res.pop('response')


class User(object):
    url_prefix = '/users'

    def __init__(self, *args, **kwargs):
        self.__dict__.update(kwargs)

    @classmethod
    def find(cls, api=None, **args):
        res = api.send_request(cls.url_prefix + '/read', args)
        return cls(**res)

    def update(self, api=None):
        type = None
        user = None
        if self.id:
            type = 'id'
            user = self.id
        elif self.name:
            type = 'name'
            user = self.name
        elif self.ip:
            type = 'ip'
            user = self.ip

        data = {
            'type': type,
            'user': user,
            'password': self.password,
            'group': self.group or ''
        }
        res = api.send_request(self.url_prefix + '/update', data)
        return res

    @classmethod
    def active_list(cls, api=None):
        res = api.send_request(cls.url_prefix + '/activelist')
        return res.pop('activeusers', '').split('\t')

    @classmethod
    def all(cls, api=None):
        res = api.send_request(cls.url_prefix + '/list')
        users = res.pop('users', [])

        all = []
        for u in users:
            all.append(User(**u))
        return all

    def destroy(self, api=None, **args):
        res = api.send_request(self.url_prefix + '/', args)
        return True

    @classmethod
    def create(cls, api=None, **args):
        res = api.send_request(cls.url_prefix + '/create', args)
        return cls(**args)


class Player(object):
    url_prefix = '/players'

    def __init__(self, **data: dict):
        self.__dict__.update(data)

    @classmethod
    def all(cls, api=None):
        res = api.send_request(cls.url_prefix + '/list')
        all = []
        for u in res.pop('players', []):
            all.append(Player(**u))
        return all

    @classmethod
    def find(cls, nickname, api=None):
        res = api.send_request(cls.url_prefix + '/read', {'player': nickname})
        return Player(**res)

    def kick(self, reason=None, api=None):
        data = {
            'player': self.nickname,
            'reason': reason or ''
        }
        return api.send_request(self.url_prefix + '/kick', data)

    def ban(self, reason=None, api=None):
        data = {
            'player': self.nickname,
            'reason': reason or ''
        }
        return api.send_request(self.url_prefix + '/ban', data)

    def kill(self, api=None):
        data = {
            'player': self.nickname
        }
        return api.send_request(self.url_prefix + '/kill', data)

    def mute(self, reason=None, api=None):
        data = {
            'player': self.nickname,
            'reason': reason or ''
        }
        return api.send_request(self.url_prefix + '/mute', data)

    def unmute(self, reason=None, api=None):
        data = {
            'palyer': self.nickname,
            'reason': reason or ''
        }
        return api.send_request(self.url_prefix + '/unmute', data)


class Ban(object):
    url_prefix = '/bans'

    @classmethod
    def create(cls, api=None, **kwargs):
        res = api.send_request('/create', kwargs)
        print(res)

    @classmethod
    def all(cls, api=None):
        res = api.send_request('/list')
        all = []
        for b in res.pop('bans', []):
            all.append(Ban(**b))
        return all

    @classmethod
    def find(cls, api=None, **kwargs):
        res = api.send_request(cls.url_prefix + '/read', kwargs)
        return Ban(**res)


class Group(object):
    url_prefix = '/groups'

    def __init__(self, *args, **kwargs):
        self.__dict__.update(kwargs)

    @classmethod
    def all(cls, api=None):
        res = api.send_request(cls.url_prefix + '/list')
        all = []
        for g in res.poop('groups', []):
            all.append(Group(**g))
        return all

    @classmethod
    def find(cls, api=None, *args, **kwargs):
        res = api.send_request(cls.url_prefix + '/read', kwargs)
        return Group(**res)

    @classmethod
    def create(cls, group, api=None, **kwargs):
        kwargs.update({
            'group': group
        })
        res = api.send_request(cls.url_prefix + '/create', kwargs)
        return Group(**kwargs)

    def update(self, api=None):
        data = {
            'group': self.group,
            'parent': self.parent or None,
            'chatcolor': self.parent or None,
            'permissions': self.permissions or None

        }
        res = api.send_request(api.url_prefix + '/update', data)
        return self
