'use strict';

window.Notification = function(title, opts) {
  if(typeof opts === 'undefined') { notify.showMsg(title); }
  else { notify.showMsg(title, opts.body, opts.icon); }
};


// https://github.com/geeeeeeeeek/electronic-wechat/blob/v1.1.1/src/inject-preload.js
// Licensed at MIT. Translated by Babel.js

var _typeof = typeof Symbol === "function" && typeof Symbol.iterator === "symbol" ? function (obj) { return typeof obj; } : function (obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol ? "symbol" : typeof obj; };

var lock = function lock(object, key, value) {
  return Object.defineProperty(object, key, {
    get: function get() {
      return value;
    },
    set: function set() {}
  });
};

var angular = window.angular = {};
var angularBootstrapReal = void 0;
Object.defineProperty(angular, 'bootstrap', {
  get: function get() {
    return angularBootstrapReal ? function (element, moduleNames) {
      var moduleName = 'webwxApp';
      if (moduleNames.indexOf(moduleName) >= 0) {
        var constants;
        angular.injector(['ng', 'Services']).invoke(['confFactory', function (confFactory) {
          return constants = confFactory;
        }]);
        angular.module(moduleName).config(['$httpProvider', function ($httpProvider) {
          $httpProvider.defaults.transformResponse.push(function (value) {
            if ((typeof value === 'undefined' ? 'undefined' : _typeof(value)) === 'object' && value !== null && value.AddMsgList instanceof Array) {
              value.AddMsgList.forEach(function (msg) {
                switch (msg.MsgType) {
                  case constants.MSGTYPE_EMOTICON:
                    lock(msg, 'MMDigest', '[Emoticon]');
                    lock(msg, 'MsgType', constants.MSGTYPE_EMOTICON);
                    if (msg.ImgWidth >= 120) {
                      lock(msg, 'MMImgStyle', { height: '120px', width: 'initial' });
                    }
                    break;
                  case constants.MSGTYPE_RECALLED:
                    lock(msg, 'MsgType', constants.MSGTYPE_SYS);
                    lock(msg, 'MMActualContent', '阻止了一次撤回');
                    lock(msg, 'MMDigest', '阻止了一次撤回');
                    break;
                }
              });
            }
            return value;
          });
        }]);
      }
      return angularBootstrapReal.apply(angular, arguments);
    } : angularBootstrapReal;
  },
  set: function set(real) {
    return angularBootstrapReal = real;
  }
});
