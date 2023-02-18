var count = new Set();
var countCiters = new Set();
var total = new Set();

var cancelToken = false;

var localStorage = window.localStorage;

var cachedInfo = JSON.parse(localStorage.getItem('cachedInfo'));
if (cachedInfo == null) {
    cachedInfo = {}
}
var cachedCiters = JSON.parse(localStorage.getItem('cachedCiters'));
if (cachedCiters == null) {
    cachedCiters = {}
}

Array.prototype.uniqueText = function() {
    var arr = [];
    for (var i = 0; i < this.length; i++) {
        if (!arr.map(a => a.text).includes(this[i].text)) {
            arr.push(this[i]);
        }
    }
    return arr;
}

function GetPapersFromAuthor(author, selectElement) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            // Typical action to be performed when the document is ready:
            var respons = JSON.parse(xhttp.responseText)
            var hits = respons.result.hits.hit.filter(hit => 'doi' in hit.info);
            var options = hits.map(hit => {
                var option = document.createElement("option");
                option.text = hit.info.title.toLowerCase();
                option.value = hit.info.doi;
                return option
            });
            options = options.uniqueText();
            selectElement.innerHTML = ''
            options.forEach(option => {
                selectElement.appendChild(option)
            });
        }
    };
    xhttp.open("GET", `https://kristoffer-strube.dk/API/Citations/AuthorsCiters/${author}`, true);
    xhttp.send();
}

function union(setA, setB) {
    let _union = new Set(setA)
    for (let elem of setB) {
        _union.add(elem)
    }
    return _union
}

function LoadPaper(doi, layers, infoCallback, citersCallback) {
    if (cancelToken) { return; }
    if (layers != 0) {
        if (!countCiters.has(doi)) {
            if (cachedCiters[doi] != undefined) {
                returnCiters(cachedCiters[doi])
            } else {
                var citersInfo = new XMLHttpRequest();
                citersInfo.onreadystatechange = function() {
                    if (this.readyState == 4 && this.status == 200) {
                        if (cancelToken) { citersInfo.onreadystatechange = undefined; return; }
                        var respons = JSON.parse(citersInfo.responseText);
                        cachedCiters[doi] = respons;
                        localStorage.setItem('cachedCiters', JSON.stringify(cachedCiters));
                        returnCiters(respons)
                    }
                };
                citersInfo.open("POST", `https://kristoffer-strube.dk/API/Citations/Citers`, true);
                citersInfo.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
                citersInfo.send(`doi=${doi}`);
            }

            function returnCiters(respons) {
                var citers = respons.map(p => p.citing.substring(8, p.citing.length));
                citersCallback(doi, citers)
                if (layers - 1 != 0) {
                    total = union(total, citers);
                    document.getElementById('total').innerHTML = total.size;

                    countCiters.add(doi)
                    citers.forEach(c => {
                        setTimeout(() => {
                            LoadPaper(c, layers - 1, infoCallback, citersCallback);
                        }, Math.floor(Math.random() * 100 * citers.length));
                    });
                }
            }
        }
    }

    if (cancelToken) { return; }
    if (!count.has(doi)) {
        if (cachedInfo[doi] != undefined) {
            returnInfo(cachedInfo[doi])
        } else {
            var paperInfo = new XMLHttpRequest();
            paperInfo.onreadystatechange = function() {
                if (cancelToken) { paperInfo.onreadystatechange = undefined; return; }
                if (this.readyState == 4 && this.status == 200) {
                    var respons = JSON.parse(paperInfo.responseText)[0];
                    if (respons != undefined) {
                        respons.author = respons.author.replaceAll(/ \[.*?\]/g,'');
                    }
                    else {
                        console.log(JSON.parse(paperInfo.responseText))
                    }
                    cachedInfo[doi] = respons;
                    localStorage.setItem('cachedInfo', JSON.stringify(cachedInfo));
                    returnInfo(respons);
                }
            };
            paperInfo.open("POST", `https://kristoffer-strube.dk/API/Citations/Info`, true);
            paperInfo.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
            paperInfo.send(`doi=${doi}`);
        }

        function returnInfo(respons) {
            if (!Array.isArray(respons)) return;
            if (respons.length == 0) return;
            infoCallback(doi, respons[0].title, respons[0].source_title, respons[0].author, respons[0].year)
            count.add(doi)
            document.getElementById('count').innerHTML = count.size;
        }
    }
}

function getParameterByName(name, url = window.location.href) {
    name = name.replace(/[\[\]]/g, '\\$&');
    var regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)'),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, ' '));
}
