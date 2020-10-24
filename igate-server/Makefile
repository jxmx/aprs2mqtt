INSTALL = \
	  /etc/igate.conf \
	  /etc/systemd/system/igate.service \
	  /etc/systemd/system/kissqueue.service \
	  /usr/local/sbin/igate \
	  /usr/local/bin/igate-console

all:	$(INSTALL)


/etc/igate.conf:	direwolf.conf
	install -m 0644 $< $@

/etc/systemd/system/igate.service:	igate.service
	install -m 0644 $< $@
	systemctl daemon-reload

/etc/systemd/system/kissqueue.service:	kissqueue.service
	install -m 0644 $< $@
	systemctl daemon-reload

/usr/local/sbin/igate:	igate
	install -m 0755 $< $@

/usr/local/bin/igate-console:	igate-console
	install -m 0755 $< $@
