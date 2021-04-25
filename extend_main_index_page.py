from flask import url_for


def start_app(application):
    @application.route('/third_test/js/plugins/waypoint/jquery.waypoints.min.js')
    @application.route('/third_test/<int:user_id>/js/plugins/waypoint/jquery.waypoints.min.js')
    @application.route('/third_test/<int:user_id>/<int:test_id>/js/plugins/waypoint/jquery.waypoints.min.js')
    @application.route('/open_user_tests/js/plugins/waypoint/jquery.waypoints.min.js')
    @application.route('/open_user_tests/<int:user_id>/js/plugins/waypoint/jquery.waypoints.min.js')
    @application.route('/test_site/js/plugins/waypoint/jquery.waypoints.min.js')
    @application.route('/my_tests/js/plugins/waypoint/jquery.waypoints.min.js')
    @application.route('/js/plugins/waypoint/jquery.waypoints.min.js')
    def url_1(user_id=0, test_id=0):
        url = url_for('static', filename='/js/plugins/waypoint/jquery.waypoints.min.js')[1:].replace('//', '/')
        return open(url.replace('/', '\\')).read()

    @application.route('/js/plugins/swiper/js/swiper.min.js')
    def url_2():
        url = url_for('static', filename='/js/plugins/swiper/js/swiper.min.js')[1:].replace('//', '/')
        return open(url.replace('/', '\\')).read()

    @application.route('/js/plugins/ajaxchimp/jquery.ajaxchimp.min.js')
    def url_3():
        url = url_for('static', filename='/js/plugins/ajaxchimp/jquery.ajaxchimp.min.js')[1:].replace('//', '/')
        return open(url.replace('/', '\\')).read()

    @application.route('/open_user_tests/js/plugins/matchHeight/jquery.matchHeight.min.js')
    @application.route('/open_user_tests/<int:user_id>/js/plugins/matchHeight/jquery.matchHeight.min.js')
    @application.route('/third_test/js/plugins/matchHeight/jquery.matchHeight.min.js')
    @application.route('/third_test/<int:user_id>/js/plugins/matchHeight/jquery.matchHeight.min.js')
    @application.route('/third_test/<int:user_id>/<int:test_id>/js/plugins/matchHeight/jquery.matchHeight.min.js')
    @application.route('/test_site/js/plugins/matchHeight/jquery.matchHeight.min.js')
    @application.route('/my_tests/js/plugins/matchHeight/jquery.matchHeight.min.js')
    @application.route('/js/plugins/matchHeight/jquery.matchHeight.min.js')
    def url_4(user_id=0, test_id=0):
        url = url_for('static', filename='/js/plugins/matchHeight/jquery.matchHeight.min.js')[1:].replace('//', '/')
        return open(url.replace('/', '\\')).read()

    @application.route('/third_test/js/plugins/waypoint/sticky.min.js')
    @application.route('/third_test/<int:user_id>/js/plugins/waypoint/sticky.min.js')
    @application.route('/third_test/<int:user_id>/<int:test_id>/js/plugins/waypoint/sticky.min.js')
    @application.route('/open_user_tests/js/plugins/waypoint/sticky.min.js')
    @application.route('/open_user_tests/<int:user_id>/js/plugins/waypoint/sticky.min.js')
    @application.route('/test_site/js/plugins/waypoint/sticky.min.js')
    @application.route('/my_tests/js/plugins/waypoint/sticky.min.js')
    @application.route('/js/plugins/waypoint/sticky.min.js')
    def url_5(user_id=0, test_id=0):
        url = url_for('static', filename='/js/plugins/waypoint/sticky.min.js')[1:].replace('//', '/')
        return open(url.replace('/', '\\')).read()

    @application.route('/third_test/js/plugins/scrollTo/jquery.scrollTo.min.js')
    @application.route('/third_test/<int:user_id>/js/plugins/scrollTo/jquery.scrollTo.min.js')
    @application.route('/third_test/<int:user_id>/<int:test_id>/js/plugins/scrollTo/jquery.scrollTo.min.js')
    @application.route('/open_user_tests/js/plugins/scrollTo/jquery.scrollTo.min.js')
    @application.route('/open_user_tests/<int:user_id>/js/plugins/scrollTo/jquery.scrollTo.min.js')
    @application.route('/test_site/js/plugins/scrollTo/jquery.scrollTo.min.js')
    @application.route('/my_tests/js/plugins/scrollTo/jquery.scrollTo.min.js')
    @application.route('/js/plugins/scrollTo/jquery.scrollTo.min.js')
    def url_6(user_id=0, test_id=0):
        url = url_for('static', filename='/js/plugins/scrollTo/jquery.scrollTo.min.js')[1:].replace('//', '/')
        return open(url.replace('/', '\\')).read()

    @application.route('/third_test/js/plugins/lpbuilderSelect/lpbuilderSelect.min.js')
    @application.route('/third_test/<int:user_id>/js/plugins/lpbuilderSelect/lpbuilderSelect.min.js')
    @application.route('/third_test/<int:user_id>/<int:test_id>/js/plugins/lpbuilderSelect/lpbuilderSelect.min.js')
    @application.route('/open_user_tests/js/plugins/lpbuilderSelect/lpbuilderSelect.min.js')
    @application.route('/open_user_tests/<int:user_id>/js/plugins/lpbuilderSelect/lpbuilderSelect.min.js')
    @application.route('/test_site/js/plugins/lpbuilderSelect/lpbuilderSelect.min.js')
    @application.route('/my_tests/js/plugins/lpbuilderSelect/lpbuilderSelect.min.js')
    @application.route('/js/plugins/lpbuilderSelect/lpbuilderSelect.min.js')
    def url_7(user_id=0, test_id=0):
        url = url_for('static', filename='/js/plugins/lpbuilderSelect/lpbuilderSelect.min.js')[1:].replace('//', '/')
        return open(url.replace('/', '\\')).read()

    @application.route('/third_test/js/plugins/isotope/isotope.pkgd.min.js')
    @application.route('/third_test/js/<int:user_id>/plugins/isotope/isotope.pkgd.min.js')
    @application.route('/third_test/js/<int:user_id>/<int:test_id>/plugins/isotope/isotope.pkgd.min.js')
    @application.route('/open_user_tests/js/plugins/isotope/isotope.pkgd.min.js')
    @application.route('/open_user_tests/<int:user_id>/js/plugins/isotope/isotope.pkgd.min.js')
    @application.route('/test_site/js/plugins/isotope/isotope.pkgd.min.js')
    @application.route('/my_tests/js/plugins/isotope/isotope.pkgd.min.js')
    @application.route('/js/plugins/isotope/isotope.pkgd.min.js')
    def url_8(user_id=0, test_id=0):
        url = url_for('static', filename='/js/plugins/isotope/isotope.pkgd.min.js')[1:].replace('//', '/')
        return open(url.replace('/', '\\')).read()
