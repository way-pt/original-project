
function escapeHtml(unsafe) {
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

const $ = require('jquery');
require('bootstrap');
const ImageViewer = require('iv-viewer').default;
const Cookie = require('js-cookie');

// pages
const content = document.querySelector('#content');
const homePage = document.querySelector('#home');
const fileUpload = document.querySelector('#file-upload');
const loadingNewMap = document.querySelector('#loading-new-map');

// components
const newMapButton = document.querySelector('#new-map');
const dataFileInput = document.querySelector('.data-file-input');
const showRecentButton = document.querySelector('#show-most-recent');
const mapNameInput = document.querySelector('#map-name-input');
const mapNameInputField = document.querySelector('#map-name-input-field');
const mapNameSubmit = document.querySelector('.map-name-submit');
const saveModalButtons = document.querySelector('#save-modal-buttons');

// component templates
function hide(element){
    let children = element.children;
    for (let child of children){
        child.style.display = 'none';
    }
    return;
}

function showGeneratedImage(url, name, username, dataFileName, date) {
    name = name || `<small class="text-muted">Map name</small>`
    username = username || '';

    const component = document.createElement('div');
    component.innerHTML = `
    <div class="generated-image card mb-3" style="max-width: 700px;">
        <div class="row no-gutters">
            <div class="col-md-8">
                <img src="${url}" class="card-img" alt="${url}">
            </div>
            <div class="col-md-4 bg-dark">
                <div class="card-body text-light image-view-tree">
                    <h5 class="map-name text-right border-bottom border-secondary">${name}</h5>
                    <p class="map-user text-right">${username}</p>
                    <p class="map-date text-right border-bottom border-secondary"><small class="text-muted">${date}</small></p>
                    <p class="map-data-title text-left>Data files</p>
                    <p class="map-data text-right>${dataFileName}</p>
                </div>
            </div>
        </div>
    </div>
    `
    return component;
}




function showMostRecent() {
    loadingNewMap.style.display = 'block';
    fetch(`/api/recent_map/`).then(res => res.json())
    .then(function (data) {
        console.log(data);
        let name = data.map.name;
        let dataURL = data.map.data_url;
        let imageURL = data.map.image;
        let user = data.map.user;
        let date = data.map.date;
        let mapPK = data.map.pk;
        loadingNewMap.style.display = 'none';
        content.appendChild(showGeneratedImage(imageURL, name, user));
        $('#save-map-modal').modal('show');
    })
}


function promptMapSave(mapPK) {
    $('#save-map-modal').modal('show');
    mapNameInputField.addEventListener('input', function () {

        $('.map-name-submit').removeAttr('disabled');
        mapNameSubmit.addEventListener('click', function () {
            let userPK = copyUser;
            let name = mapNameInputField.value;
            let dict = {
                "pk": mapPK,
                "name": name,
                "user": userPK
            }
            console.log(JSON.stringify(dict));
            console.log(copyUser);
            $('#save-map-modal').modal('hide');
            let csrftoken = Cookie.get('csrftoken');
            fetch(`/api/save_map/`, {
                method: 'PATCH',
                headers: {
                    "Content-Type": `application/json`,
                    "X-CSRFToken": csrftoken
                },
                body: JSON.stringify(dict)
            }).then(res => res.text())
            .then(function (text) {
                console.log(text)
                // $(".generated-image").remove();
                // showGeneratedImage(data.map.image, data.map.name, data.map.user_username, data.map.data_file, data.map.date);
            })
        })
    })

   
}

$('#save-map-modal').on('shown.bs.modal', function () {
    $('#map-name-input-field').trigger('focus')
  })




if (document.querySelector('#loggedIn')) {
    var copyUser = document.querySelector('#loggedIn').dataset['username']
    var copyUsername = document.querySelector('#loggedIn').dataset['userstring']
    console.log(copyUser)
    console.log(copyUsername)
}
if (showRecentButton) {
    showRecentButton.addEventListener('click', function () {
        hide(content);
        showMostRecent();
    })
}

if (newMapButton && homePage) {
    
    newMapButton.addEventListener('click', function () {
        homePage.style.display = 'none';
        fileUpload.style.display = 'block';
    })
}

if (fileUpload) {
    const dataFileInput = document.querySelector('.data-file-input');
    dataFileInput.addEventListener('input', function () {
        let dataFile = dataFileInput.files[0];
        console.log(dataFile.name);
        const submitMapFormButton = document.querySelector('.submit-map-form');
        submitMapFormButton.disabled = false;
        submitMapFormButton.addEventListener('click', function () {
            var formData = new FormData();
            let dataFileURL = URL.createObjectURL(dataFile);
            formData.append('data', dataFile);

            fileUpload.style.display = 'none';
            loadingNewMap.style.display = 'block';
            fetch(`/api/new_map/filename=${encodeURIComponent(dataFile.name)}`, {
                method: 'POST',
                headers: {
                    "Content-Disposition": `form-data;name=name; filename=${dataFile.name}`
                },
                body: formData
            }).then(res => res.json())
            .then(function (data) {
                console.log(data);
                loadingNewMap.style.display = 'none';
                let imageURL = data.newMap.image;
                content.appendChild(showGeneratedImage(imageURL, null, copyUsername));
                promptMapSave(data.newMap.pk);
            })
                // .then(response => console.log('Success:', JSON.stringify(response)))
                // .catch(error => console.error('Error:', error));
        })
    })
    
}
