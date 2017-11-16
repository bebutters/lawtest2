a = r"""
<!DOCTYPE html>
<html>

<style>
.hide {
    display: none }
td {white-space:pre}
</style>

<div class="tab">
    <button class="tablinks" onclick="openCity(event, 'LawyerDiv')">Lawyer</button>
    <button class="tablinks" onclick="openCity(event, 'FirmDiv')">Firm</button>
</div>

<div id="LawyerDiv" class = "tabcontent">
    <form id="Lawyer">
        First Name: <input type="text" name="FirstName"><br>
        Last name: <input type="text" name="LastName"><br>
        Postcode: <input type="text" name="PostCode"><br>
        Language Spoken: <input type="text" name="Language"><br>
<!--        Specialty: <input type="text" name="Specialty"><br>-->
        <button type="button" onclick="GetLawyers()">Submit</button>
        <button type="button" onclick="Reset()">Reset</button>
        <button type="button" onclick="Clear()">Clear</button>
    </form>
</div>

<div id="FirmDiv" class = "tabcontent hide" display: none>
    <form id="Firm">
        Firm Name: <input type="text" name="Name"><br>
        Postcode: <input type="text" name="PostCode"><br>
        Language: <input type="text" name="Language"><br>
        <button type="button" onclick="GetFirms()">Submit</button>
        <button type="button" onclick="Reset()">Reset</button>
        <button type="button" onclick="Clear()">Clear</button>
    </form>
</div>

<div id = "results">
</div>

<script>
function Clear() {
    var elements = document.getElementById("Lawyer").elements
    for (var i = 0, element; element = elements[i++];) {
        element.value = "" }
    var elements = document.getElementById("Firm").elements
    for (var i = 0, element; element = elements[i++];) {
        element.value = "" } }

function Reset() {
    Clear()
    document.getElementById("results").innerHTML = "" }        

function openCity(evt, tabname) {
    var i, tabcontent, tablinks;

    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    document.getElementById("results").innerHTML = ""
    document.getElementById(tabname).style.display = "block";
}

function GetLawyers(){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function(){
        if (this.readyState == 4 && this.status == 200){
            var div = document.getElementById("results")
            data = JSON.parse(xhttp.responseText)
            try {
                data["error"].length
                div.innerHTML = "Could not complete the request. Please try refresh the page"
                return(true) }
            catch (e) {}
            if (data["data"].length) {
                var str = ""
                str += "<table>"
                str += `<tr>
                        <th>Name</th>
                        <th>Firm</th>
                        <th>Postcode</th>
                        <th>Languages</th>
                        </tr>`
                for (var object in data["data"]) {
                    object = data["data"][object]
                    str += "<tr>"
                    str += "<td>" + object["name"] + "</td>"
                    str += "<td>" + object["firm"] + "</td>"
                    str += "<td>" + object["postcode"] + "</td>"
                    str += "<td>"
                    for (var language in object["languages"]) {
                        language = object["languages"][language]
                        str += language + "\n" }
                    str += "</td>"
                    str += "</tr>" }
                str += "</table>"
                div.innerHTML = str
                if (data["flag"]) {
                    div.innerHTML += "<p>More than 20 results found. Refine search terms to see other results</p>"}}
            else {
                div.innerHTML = "No results found. Please try a different search."}}};
    xhttp.open("POST", "/Lawyer", true);
    var formdata = new FormData(document.getElementById('Lawyer'));
    xhttp.send(formdata);}

function GetFirms(){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function(){
        if (this.readyState == 4 && this.status == 200){
            var div = document.getElementById("results")
            data = JSON.parse(xhttp.responseText)
            try {
                data["error"].length
                div.innerHTML = "Could not complete the request. Please try refresh the page"
                return(true) }
            catch (e) {}
            if (data["data"].length) {
                var str = ""
                str += "<table>"
                str += `<tr>
                        <th>Firm</th>
                        <th>Postcode</th>
                        <th>Firm Languages</th>
                        </tr>`
                for (var object in data["data"]) {
                    object = data["data"][object]
                    str += "<tr>"
                    str += "<td>" + object["firm"] + "</td>"
                    str += "<td>" + object["postcode"] + "</td>"
                    str += "<td>"
                    for (var language in object["languages"]) {
                        language = object["languages"][language]
                        str += language + "\n" }
                    str += "</td>"
                    str += "</tr>" }
                str += "</table>"
                div.innerHTML = str
                if (data["flag"]) {
                    div.innerHTML += "<p>More than 20 results found. Refine search terms to see other results</p>"}}
            else{
                div.innerHTML = "No results found. Please try a different search."}}};
    xhttp.open("POST", "/Firm", true);
    var formdata = new FormData(document.getElementById('Firm'));
    xhttp.send(formdata);}

</script>

</html> 
"""
