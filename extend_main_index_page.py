from flask import url_for


def start_app(app):

    @app.route('/js/plugins/waypoint/jquery.waypoints.min.js')
    def url_1():
        url = url_for('static', filename='/js/plugins/waypoint/jquery.waypoints.min.js')[1:].replace('//', '/')
        return open(url.replace('/', '\\')).read()

    @app.route('/js/plugins/swiper/js/swiper.min.js')
    def url_2():
        url = url_for('static', filename='/js/plugins/swiper/js/swiper.min.js')[1:].replace('//', '/')
        return open(url.replace('/', '\\')).read()

    @app.route('/js/plugins/ajaxchimp/jquery.ajaxchimp.min.js')
    def url_3():
        url = url_for('static', filename='/js/plugins/ajaxchimp/jquery.ajaxchimp.min.js')[1:].replace('//', '/')
        return open(url.replace('/', '\\')).read()

    @app.route('/js/plugins/matchHeight/jquery.matchHeight.min.js')
    def url_4():
        url = url_for('static', filename='/js/plugins/matchHeight/jquery.matchHeight.min.js')[1:].replace('//', '/')
        return open(url.replace('/', '\\')).read()

    @app.route('/js/plugins/waypoint/sticky.min.js')
    def url_5():
        url = url_for('static', filename='/js/plugins/waypoint/sticky.min.js')[1:].replace('//', '/')
        return open(url.replace('/', '\\')).read()

    @app.route('/js/plugins/scrollTo/jquery.scrollTo.min.js')
    def url_6():
        url = url_for('static', filename='/js/plugins/scrollTo/jquery.scrollTo.min.js')[1:].replace('//', '/')
        return open(url.replace('/', '\\')).read()
