function launchiOSApp(url) {

     var appleAppStoreLink = 'https://itunes.apple.com/sg/app/dbs-paylah!/id878528688?mt=8';

     var now = new Date().valueOf();

     setTimeout(function () {

          if (new Date().valueOf() - now > 500) return;
     window.location = url;

     }, 100);

}