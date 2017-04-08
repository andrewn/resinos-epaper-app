FROM jannis/embeddedartists-epaper

WORKDIR /usr/src/app
COPY . .

COPY start.sh /bin/start.sh
RUN chmod +x /bin/start.sh
ENTRYPOINT ["/bin/start.sh"]
