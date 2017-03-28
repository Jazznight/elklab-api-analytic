#!/bin/sh

curl -XPUT "http://localhost:9200/_template/elklab-nginx?pretty" -d '{
  "template": "elklab-nginx-*",
  "order": 1,
  "settings": {
    "number_of_shards": 4,
    "number_of_replicas": 3,
    "index.refresh_interval": "5s"
  },
  "mappings": {
    "_default_": {
      "_all": { "enabled": false }, 
      "properties" : {
        "size":          { "type": "long"},
        "agent":         { "type": "text", "doc_values": false },
        "path":          { "type": "text", "doc_values": false },
        "referer":       { "type": "text", "doc_values": false },
        "code":          { "type": "keyword" },
        "host":          { "type": "keyword", "doc_values": false },
        "method":        { "type": "keyword", "doc_values": false },
        "user":          { "type": "keyword", "doc_values": false },
        "remote":        { "type": "keyword" },
        "device":        { "type": "keyword" },
        "resource_item": { "type": "keyword" },
        "resource":      { "type": "keyword" },
        "resource_type": { "type": "keyword" },
        "is_continue":   { "type": "boolean", "doc_values": false },
        "@timestamp" : {
          "format": "strict_date_optional_time||epoch_millis",
          "type": "date"
        },
        "geoip" : {
          "properties" : {
            "continent_code":{"type":"keyword", "doc_values": false},
            "continent":     {"type":"keyword", "doc_values": false},
            "country":       {"type":"keyword" },
            "city":          {"type":"keyword" },
            "coordinates":   {"type":"geo_point"}
          }
        }
      }
    }
  }
}'
