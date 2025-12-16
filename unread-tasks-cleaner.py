import redis
from redis.connection import SSLConnection

redis_url = "rediss://:aRPsR1MsTgsNfsRa5sOS-QjWDhgLdHSgfGN6-UaXsYg8T-IXnJhfKdISXS0D@prod-ha-cluster-1-001.prod-ha-cluster-1.0mpaqo.use1.cache.amazonaws.com:6379"

r = redis.Redis.from_url(redis_url, connection_class=SSLConnection)

cnt = 0
pattern = '{unread-tasks}*'
assigned_task_keys = []
members = r.hgetall('unread-tasks')

for key, value in members.items():
    assigned_task_keys.append('{unread-tasks}:' + value.decode("utf-8") )

print('scanning has started')
for key in r.scan_iter(pattern):
    decoded_key = key.decode("utf-8")
    if decoded_key not in assigned_task_keys and 'redisson_set' not in decoded_key:
        print(decoded_key)
        r.delete(decoded_key)
        cnt += 1
print('scanning is complete, total:', cnt)
