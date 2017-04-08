FROM jannis/embeddedartists-epaper

COPY start.sh /bin/start.sh
RUN chmod +x /bin/start.sh
ENTRYPOINT ["/bin/start.sh"]
