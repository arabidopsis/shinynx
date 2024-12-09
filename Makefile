test:
	nginx -c $(realpath .)/sticky.conf


nginx:
	footprint config template templates/nginx.conf  -o shiny.conf server-name=shiny.plantenergy.org workers=4 module=app

systemd:
	footprint config template --user -o shiny.service templates/systemd.service workers=4 appname=app

.PHONY: nginx systemd test
