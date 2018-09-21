#!/usr/bin/env python

import redis
from pds_pipelines.config import redis_info as ri

class RedisLock(object):

    def __init__(self, name):
        """
        Parameters
        ----------
        name : str
          The name of the RedisLock object
        """
        #self.__db = redis.StrictRedis(host=ri['host'], port=ri['port'], db=ri['db'])
        self.__db = redis.StrictRedis()
        self.name = 'lock:%s' % (name)


    def contains(self, key):
        """ Test if a key exists in the hash map.
        Parameters
        ----------
        element : str
            The key for which the function will search
        
        Returns
        -------
        bool
            True if the key exists in the hash map, otherwise False
        """
        return self.__db.hexists(self.name, key)


    def add(self, item):
        """ Adds a key : value pair to the hash map.
        Parameters
        ----------
        item : dict
            A key value pair to be added to the hash map.
        
        Returns
        -------
        None
        """
        self.__db.hmset(self.name, item)


    def delete(self):
        """ Removes the underlying hash map from the Redis DB.
        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.__db.delete(name)


    def _set(self, key, value):
        """ Sets the value in the key : value pair.
        
        Parameters
        ----------
        key : str
            The key that will be added to the hash map
        value : obj
            The value associated with the key
        
        Returns
        -------
        None
        """
        self.__db.hset(self.name, key, value)


    def get(self, key):
        """ Returns the value given a key.

        Automatically decodes byte strings returned by Redis.

        Parameters
        ----------
        key : str
            The key associated with the value to be returned
        
        Returns
        -------
        str
            The value associated with the specified key.
        """
        return (self.__db.hget(self.name, key)).decode('utf-8')


    def get_all(self):
        """ Convenience function that returns a dict of all.
        Parameters
        ----------
        None

        Returns
        -------
        dict
            The dictionary of all key:value pairs in the hash map.
        """
        return self.__db.hgetall(self.name)


    def lock(self, key):
        """
        Parameters
        ----------
        key : str
            The name of the queue that we wish to lock
        
        Returns
        -------
        None
        """
        self._set(key, '0')


    def unlock(self, key):
        """
        Parameters
        ----------
        key : str
            The name of the queue that we wish to unlock
        
        Returns
        -------
        None
        """

        self._set(key, '1')


    def lock_all(self):
        """ A convenience function that locks all queues in the hash map.
        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        for key in self.get_all():
            self.lock(key)


    def unlock_all(self):
        """ A convenience function that unlocks all queues in the hash map.
        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        for key in self.get_all():
            self.unlock(key)


    def available(self, key):
        """
        Parameters
        ----------
        key : str
            The key to be tested for locked/unlocked status.
        
        Returns
        -------
        bool
            True if the associated queue is unlocked, else False
        """
        return self.get(key) == '1'
