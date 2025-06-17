addButton=document.getElementById('add')

function fcAjax() {
    var xhttp = new XMLHttpRequest()
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById("Ajax").innerHTML = this.responseText;
        }
    };
    xhttp.open("GET", "tipFrunzaList", true);
    xhttp.send();
}

fcAjax()
