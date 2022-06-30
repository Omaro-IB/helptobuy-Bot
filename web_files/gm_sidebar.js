var SERVMETRIC_CDN_URL = 'https://websurveys2.govmetric.com/';
var SERVMETRIC_VERSION = '202011112031';

try {
    var servmetric_snippet = document.createElement('script');
    servmetric_snippet.setAttribute('src', SERVMETRIC_CDN_URL + 'js/client/gm_intro.js?v=' + SERVMETRIC_VERSION);
    document.getElementsByTagName("head")[0].appendChild(servmetric_snippet);
} catch (e) { }

