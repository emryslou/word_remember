(function(window){
    setTimeout(() => {
        chrome.storage.sync.get('cached', (res) => {
            document.querySelector('#cached').value = res.cached;
        });
    }, 1);
})(window);