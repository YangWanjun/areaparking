var isSubscribed = false;
var pushButton = null;
window.addEventListener("load", function() {
    pushButton = document.querySelector('.js-push-button');
    if (pushButton == null) {
        return;
    }
    pushButton.addEventListener("click", function() {
        subscribeUser();
    });

    if ('serviceWorker' in navigator && 'PushManager' in window) {
        // 指定したスクリプトをServiceWorkerとしてインストール
        navigator.serviceWorker.register("/static/js/sw.js").then(function(swReg) {
            console.log('Service Worker is registered', swReg);

            swRegistration = swReg;
            swRegistration.pushManager.getSubscription()
            .then(function(subscription) {
                isSubscribed = !(subscription === null);
                if (isSubscribed) {
                    console.log('User IS subscribed.');
                } else {
                    console.log('User is NOT subscribed.');
                }
                updateBtn(subscription);
            })
        }).catch(function(error) {
            console.error('Service Worker Error', error);
        });
    } else {
        console.warn('Push messaging is not supported');
    }
}, false);

function subscribeUser() {
//    var applicationServerPublicKey = "BAvstILXqJgYl_9_KTNwExG7Z9KcuEfXiBvSxKYqQnvFW9fNy2eFh5nqsNW0oPYFGg9c4sNqBVu5OkEN5YiWMWs";
//    applicationServerKey = urlB64ToUint8Array(applicationServerPublicKey);
    swRegistration.pushManager.subscribe({userVisibleOnly: true})
    .then(function(subscription) {
        console.log('User is subscribed.');
        updateSubscriptionOnServer(subscription);
        updateBtn(subscription);
        isSubscribed = true;
    })
    .catch(function(err) {
        console.log('Failed to subscribe the user: ', err);
    });
}

function updateSubscriptionOnServer(subscription) {
    // Send subscription to application server
    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    data = {'subscription': JSON.stringify(subscription)}
    $.post('/whiteboard/update_subscription', data, function(){
    }).done(function(response){
        //alert('success!')
    }).fail(function(response){
        //alert('error!')
    })
}

function updateBtn(subscription) {
    if (Notification.permission === 'denied') {
        pushButton.textContent = 'Push Messaging Blocked.';
        pushButton.disabled = true;
        // updateSubscriptionOnServer(null);
        return;
    }
    if (isSubscribed) {
        pushButton.textContent = 'Disable Push Messaging';
        var reg_id = subscription.endpoint.split("/").pop();
        console.log("reg_id: " + reg_id);
        // var rawKey = subscription.getKey ? subscription.getKey('p256dh') : '';
        // var key = rawKey ? Base64EncodeUrl(btoa(String.fromCharCode.apply(null, new Uint8Array(rawKey)))) : '';
        // var rawAuthSecret = subscription.getKey ? subscription.getKey('auth') : '';
        // var authSecret = rawAuthSecret ? Base64EncodeUrl(btoa(String.fromCharCode.apply(null, new Uint8Array(rawAuthSecret)))) : '';
        // console.log("Key: " + key);
        // console.log("AuthSecret: " + authSecret);
        // console.log('subscription:' + JSON.stringify(subscription));
        pushButton.disabled = true;
    } else {
        pushButton.textContent = 'Enable Push Messaging';
        pushButton.disabled = false;
        setTimeout(function(){pushButton.click()}, 5000);
    }
}

function Base64EncodeUrl(str){
    return str.replace(/\+/g, '-').replace(/\//g, '_').replace(/\=+$/, '');
}

function Base64DecodeUrl(str){
    str = (str + '===').slice(0, str.length + (str.length % 4));
    return str.replace(/-/g, '+').replace(/_/g, '/');
}

function urlB64ToUint8Array(base64String) {
  const padding = '='.repeat((4 - base64String.length % 4) % 4);
  const base64 = (base64String + padding)
    .replace(/\-/g, '+')
    .replace(/_/g, '/');

  const rawData = window.atob(base64);
  const outputArray = new Uint8Array(rawData.length);

  for (let i = 0; i < rawData.length; ++i) {
    outputArray[i] = rawData.charCodeAt(i);
  }
  return outputArray;
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
