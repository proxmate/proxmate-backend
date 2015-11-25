(function () {
    "use strict";
    angular.module("proxmatemeApp", ["ngCookies", "ngResource", "ngSanitize", "ngRoute", "angular-carousel", "angularUtils.directives.dirDisqus"])

}).call(this), function () {
    "use strict";
    angular.module("proxmatemeApp").controller("MainCtrl", ["$scope", "$location", "dataFactory", "Page", function (a, b, c, d) {
        return d.startLoading("Download Page"), d.setSection("home"), d.finishLoading()
    }])
}.call(this), function () {
    "use strict";
    angular.module("proxmatemeApp").constant("config", {
        API_HOST: "http://api-staging.proxmate.me",
        DISQUS_SHORTNAME: "proxmate"
    })
}.call(this), function () {
    "use strict";
    angular.module("proxmatemeApp").factory("dataFactory", ["$http", "config", function (a, b) {
        var c;
        return c = 42, {
            someMethod: function () {
                return c
            }, getPackages: function (c) {
                return a.get("" + b.API_HOST + "/package/list.json").success(c)
            }, getPackage: function (c, d) {
                return a.get("" + b.API_HOST + "/package/" + c + ".json").success(d)
            }
        }
    }])
}.call(this), function () {
    "use strict";
    angular.module("proxmatemeApp").controller("PackagesCtrl", ["$scope", "$location", "dataFactory", "Page", function (a, b, c, d) {
        console.log( 100 )
        return d.startLoading("Packages"), d.setTitle("Browse available proxy packages"), d.setDescription("Check out and browse through the newest packages submitted to ProxMate and download what you like"), d.setSection("packages"), c.getPackages(function (b) {
            return a.packages = b, d.setTitle("package listing"), d.finishLoading()
        })
    }])
}.call(this), function () {
    "use strict";
    angular.module("proxmatemeApp").controller("DetailCtrl", ["$scope", "$route", "$routeParams", "dataFactory", "Page", "config", "$location", function (a, b, c, d, e, f, g) {
        return e.setSection("packages"), e.startLoading("Package Detail View"), d.getPackage(c.packageId, function (b) {
            return a.packageData = b, a.disqusUrl = "https://" + (g.host() + g.path()), a.disqusShortname = f.DISQUS_SHORTNAME, e.setTitle("" + b.name + " proxy package"), e.setDescription(b.description), e.setImage("https:" + b.bigIcon, !0), e.finishLoading()
        })
    }])
}.call(this), function () {
    "use strict";
    angular.module("proxmatemeApp").controller("AboutCtrl", ["$scope", "$location", "Page", function (a, b, c) {
        return c.startLoading("About Page"), c.setSection("about"), c.setTitle("About our project"), c.setDescription("Learn more about the behind the scenes of the ProxMate project and support us on github!"), c.finishLoading()
    }])
}.call(this), function () {
    "use strict";
    angular.module("proxmatemeApp").controller("SupportCtrl", ["$scope", "$location", "Page", "$sce", function (a, b, c, d) {
        return c.startLoading("Donation Page "), c.setSection("donate"), c.setTitle("Donate and ensure the future of the project"), c.setImage("images/heart-shape.png"), c.setDescription("Want to help the ProxMate project out a bit? Your donation is greatly appreciated!!"), a.donationSteps = [3, 8, 13, 21, 34, 55], a.pickedDonationstep = 3, a.isRecurring = !1, a.paypalButton = null, a.pickDonationstep = function (b) {
            return a.pickedDonationstep = b, a.createPaypalbutton()
        }, a.changeRecurring = function (b) {
            return a.isRecurring = b, a.createPaypalbutton()
        }, a.createPaypalbutton = function () {
            var b, c;
            return b = {
                amount: {value: a.pickedDonationstep},
                name: {value: "ProxMate donation"},
                currency_code: {value: "EUR"}
            }, c = "donate", a.isRecurring && (c = "subscribe", b.recurrence = {value: 1}, b.period = {value: "M"}, b.src = {value: 1}), a.paypalHtml = PAYPAL.apps.ButtonFactory.create("paypal@proxmate.me", b, c), a.paypalButton = d.trustAsHtml(a.paypalHtml.outerHTML), !0
        }, a.createPaypalbutton(), c.finishLoading()
    }])
}.call(this), function () {
    "use strict";
    angular.module("proxmatemeApp").factory("Page", ["$location", function (a) {
        var b, c, d, e, f, g, h, i, j;
        return j = "ProxMate -", g = "https://proxmate.me/", i = "" + j + " Download for Chrome, Opera and Firefox", b = "ProxMate is the worlds first proxy package manager that lives in your browser. Automatically install pre-defined proxy scripts, stay anonymous, mask your IP and more. All that, for free! Download now for Chrome, Firefox and Opera!", c = "https://" + a.host() + "/images/proxmate-logo-single.png", h = "home", e = "Loading", f = "Loading...", d = !1, {
            title: i,
            setTitle: function (a, b) {
                return b = b || !1, this.title = "" + j + " " + a, b ? this.title = a : void 0
            },
            description: b,
            setDescription: function (a) {
                return this.description = a
            },
            image: c,
            setImage: function (b, c) {
                return c = c || !1, this.image = "https://" + a.host() + "/" + b, c ? this.image = b : void 0
            },
            path: g,
            setPath: function (a) {
                return this.path = a
            },
            section: h,
            setSection: function (a) {
                return this.section = a.toLowerCase()
            },
            isLoading: d,
            loadingText: f,
            startLoading: function (d) {
                return this.loadingText = "" + e + " " + d + "...", this.isLoading = !0, this.description = b, this.image = c, this.title = i, this.path = "https://" + (a.host() + a.path())
            },
            finishLoading: function () {
                return this.isLoading = !1
            }
        }
    }])
}.call(this), function () {
    "use strict";
    angular.module("proxmatemeApp").controller("PageCtrl", ["$rootScope", "Analytics", "Page", function (a, b, c) {
        return a.Page = c
    }])
}.call(this), function () {
    "use strict";
    angular.module("proxmatemeApp").filter("nl2br", function () {
        return function (a) {
            return a ? a.replace(/\n/g, "<br/>") : void 0
        }
    })
}.call(this), function () {
    "use strict";
    angular.module("proxmatemeApp").service("Analytics", ["$rootScope", "$window", "$location", "$timeout", function (a, b, c, d) {
        var e;
        return e = function () {
            return d(function () {
                return b.ga("send", "pageview", {page: c.path()})
            }, 500)
        }, a.$on("$viewContentLoaded", e)
    }])
}.call(this);