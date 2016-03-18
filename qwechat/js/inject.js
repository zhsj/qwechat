window.Notification = function(title, opts) {
    if(typeof opts === 'undefined') { notify.showMsg(title); }
    else { notify.showMsg(title, opts.body, opts.icon); }
}
