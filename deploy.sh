#!/bin/bash

echo "Pushing db"

docker save memedb:latest | \
  bzip2 | \
  ssh hugo@blog.hugo-klepsch.tech 'bunzip2 | docker load'

echo "done"

echo "Pushing server"

docker save memeserver:latest | \
  bzip2 | \
  ssh hugo@blog.hugo-klepsch.tech 'bunzip2 | docker load'

echo "done"

echo "Push start.sh"
cat start.sh | \
  bzip2 | \
  ssh hugo@blog.hugo-klepsch.tech \
    'bunzip2 > /home/hugo/cis3750memestream/start.sh && chmod u+x /home/hugo/cis3750memestream/start.sh'

echo "done"

echo "Push stop.sh"
cat stop.sh | \
  bzip2 | \
  ssh hugo@blog.hugo-klepsch.tech \
    'bunzip2 > /home/hugo/cis3750memestream/stop.sh && chmod u+x /home/hugo/cis3750memestream/stop.sh'

echo "done"
