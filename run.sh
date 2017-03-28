#!/bin/sh


usage() {
  echo ""
  echo "  Usage:"
  echo "    $0 \${FLUENTD_CONFIG_FILE}"
  echo ""
  echo ""
  exit -1
}

if [ -z $1 ];
then
  usage
fi


rm -f buffers/*buffer
rm -f pos/*pos
curl -XDELETE 'localhost:9200/elklab-dstat-*'
curl -XDELETE 'localhost:9200/elklab-nginx-*'

echo ""
echo ""

td-agent -c $1
