(function(window){
    function capture_word_info() {
        function ForeachMap(selector) {
            let result = [];
            document.querySelectorAll(selector).forEach((e) => {
                result.push(e.innerText.replace(/\n/g, '&nbsp;'))
            });
    
            return result
        }
    
        let cur_date = function() {
            let now = new Date;
            return now.getFullYear() + '-' + 
                (now.getMonth() + 1).toString().padStart(2, '0') + '-' + 
                (now.getDate()).toString().padStart(2, '0')
        };
        let word_info = {
            'date': cur_date(),
            'word': document.querySelector('.di-title > .headword').innerText,
            'href': window.location.href,
            'pron': document.querySelector('.pos-header > span.uk > .pron').innerText,
            'explain_en': ForeachMap('.sense-body >.def-block.ddef_block > .ddef_h'),
            'explain_zh': ForeachMap('.sense-body >.def-block.ddef_block > .def-body > .trans'),
        }
        
        return word_info
    }
    
    function copyTextToClipboard(text) {
        let newPromise = new Promise((resolve, rejected) => {
            var textarea = document.createElement('textarea');
            textarea.value = text;
            document.body.appendChild(textarea);
            textarea.select();
            document.execCommand('copy');
            document.body.removeChild(textarea);
            resolve()
        });
        
        newPromise.then(() => {
            chrome.storage.sync.set({cached: text}, () => {
                alert('解析完成，可直接粘贴使用');
                console.log('解析完成，可直接粘贴使用');
            });
        }).catch(e => {
            alert('保存失败，请在上方内容中复制解析结果，查找【请复制下面内容:】，并复制后面的文本');
            document.querySelector('div[data-iaw="container"]').append(`请复制下面内容: ${text}`);
        })
    }
    
    function parse() {
        let word_info = capture_word_info();
        let word = `[${word_info.word}](${word_info.href})`;
        let word_en = '&square; ' + word_info.explain_en.join('<br/>&square; ');
        let word_zh = '&square; ' + word_info.explain_zh.join('<br/>&square; ');
        let text = `|${word_info.date}|${word}|${word_info.pron}|${word_zh}|${word_en}|`
        copyTextToClipboard(text);
    }
    
    function inject_element() {
        let button = document.createElement('button');
        button.addEventListener('click', (e) => {
            let raw_text = e.target.innerText;
            e.target.disabled = true;
            new Promise((resolve, rejected) => {
                e.target.innerText = '解析中...';
                setTimeout(() => {
                    parse();
                    e.target.innerText = '解析完成';
                    resolve();
                }, 1000);
            }).then(() => {
                setTimeout(() => {
                    e.target.innerText = raw_text;
                    e.target.disabled = false;
                }, 1000);
            });
        });
        button.innerText = '解析';
        document.querySelector('.di-title>span.headword').parentNode.append(button)
    }
    
    inject_element()
})(window);
