# -*- coding: utf-8 -*-

import rethinkdb as r

class RethinkdbPipeline(object):

    conn = None
    rethinkdb_settings = {}
    
    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings

        ## get rethinkdb settings from settings.py
        rethinkdb_settings = settings.get('RETHINKDB', {})

        return cls(rethinkdb_settings)

    def __init__(self, rethinkdb_settings):
        self.rethinkdb_settings = rethinkdb_settings

    def open_spider(self, spider):
        if self.rethinkdb_settings:
            
            self.table_name = self.rethinkdb_settings['table_name']
            self.db_name = self.rethinkdb_settings['db']
            self.conn = r.connect('localhost', 28015)
            table_list = r.db(self.db_name).table_list().run(self.conn)
            
            ## verify if table already exists and creates a table in database              
            if self.table_name not in table_list:
                r.db(self.db_name).table_create(self.table_name).run(self.conn)

    def close_spider(self, spider):
        if self.conn:
            self.conn.close()

    def process_item(self, item, spider):
        if self.conn:
            r.db(self.db_name).table(self.table_name).insert(item).run(self.conn)
        return item
