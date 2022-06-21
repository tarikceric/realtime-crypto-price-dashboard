-- Create initial tables in Questdb
CREATE TABLE
      quotes(stock_symbol SYMBOL CAPACITY 5 CACHE INDEX,
             current_price DOUBLE,
             high_price DOUBLE,
             low_price DOUBLE,
             open_price DOUBLE,
             percent_change DOUBLE,
             tradets TIMESTAMP, -- timestamp of trade
             ts TIMESTAMP)      -- time of insert in our table
      timestamp(ts)
PARTITION BY DAY;