import redis

from Tripadvisor2.settings import REDIS_HOST, REDIS_PORT, REDIS_PWD, REDIS_DB
from manage import config, section



if __name__ == '__main__':
    client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PWD, db=REDIS_DB)

    redis_key = section.get('name') + ':start_urls'
    start_url = section.get('start_url')
    client.lpush(redis_key, start_url)