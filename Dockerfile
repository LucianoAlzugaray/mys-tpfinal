FROM nodered/node-red-docker

RUN ls -n /usr/share/zoneinfo/America/Argentina/Rio_Gallegos /etc/localtime
RUN  npm install node-red-dashboard
RUN  npm install node-red-node-ui-table
