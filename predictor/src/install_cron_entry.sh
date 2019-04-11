touch /var/log/cron.log
cd /etc/cron.d && echo "*/1 * * * * root bash /usr/bin/src/precompute_scheduler.sh" > precompute