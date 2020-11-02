var proxy = "" //"https://cors-anywhere.herokuapp.com/";

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
    xhttp.open("GET", proxy + `https://dblp.org/search/publ/api?q=author%3A${author.replaceAll(' ', '+')}%3A&format=json&h=1000`, true);
    xhttp.send();
}

function LoadPaper(doi, layers, infoCallback, citersCallback) {
    var paperInfo = new XMLHttpRequest();
    paperInfo.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            // Typical action to be performed when the document is ready:
            var respons = JSON.parse(paperInfo.responseText);
            if (!Array.isArray(respons)) return;
            if (respons.length == 0) return;
            infoCallback(doi, respons[0].title)
        }
    };
    paperInfo.open("GET", proxy + `https://opencitations.net/index/api/v1/metadata/${doi}`, true);
    paperInfo.send();

    if (layers != 0) {
        var citersInfo = new XMLHttpRequest();
        citersInfo.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                // Typical action to be performed when the document is ready:
                var respons = JSON.parse(citersInfo.responseText)
                var citers = respons.map(p => p.citing.substring(8, p.citing.length));
                citersCallback(doi, citers)
                citers.forEach(c => LoadPaper(c, layers - 1, infoCallback, citersCallback))
            }
        };
        citersInfo.open("GET", proxy + `https://opencitations.net/index/api/v1/citations/${doi}`, true);
        citersInfo.send();
    }
}