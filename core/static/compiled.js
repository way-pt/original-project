(function(){function r(e,n,t){function o(i,f){if(!n[i]){if(!e[i]){var c="function"==typeof require&&require;if(!f&&c)return c(i,!0);if(u)return u(i,!0);var a=new Error("Cannot find module '"+i+"'");throw a.code="MODULE_NOT_FOUND",a}var p=n[i]={exports:{}};e[i][0].call(p.exports,function(r){var n=e[i][1][r];return o(n||r)},p,p.exports,r,e,n,t)}return n[i].exports}for(var u="function"==typeof require&&require,i=0;i<t.length;i++)o(t[i]);return o}return r})()({1:[function(require,module,exports){

function escapeHtml(unsafe) {
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

// pages
const content = document.querySelector('#content');
const homePage = document.querySelector('#home');
const fileUpload = document.querySelector('#file-upload');
const loadingNewMap = document.querySelector('#loading-new-map');

// components
const newMapButton = document.querySelector('#new-map');
const dataFileInput = document.querySelector('.data-file-input');
const showRecentButton = document.querySelector('#show-most-recent');
const saveMapModal = document.querySelector('#save-map-modal');

// component templates
function hide(element){
    let children = element.children;
    for (let child of children){
        child.style.display = 'none';
    }
    return;
}

function showGeneratedImage(url, name, username) {
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
                    <h5 class="map-name text-right border-bottom border-secondary">${name}&#9660;</h5>
                    <p class="map-user text-right">User: <strong>${username}</p>
                    <p class="map-date text-right"><small class="text-muted"></small></p>
                </div>
            </div>
        </div>
    </div>
    `
    return component;
}
function showSaveModal(){
    const component = document.createElement('div');
    component.innerHTML = `
    <div class="modal save-map-modal" tabindex="-1" role="dialog">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Save map</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <p>Would you like to save your map?</p>
            <input id="map-name-input" type="text" class="form-control" placeholder="map name..." aria-label="map name">
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
            <button type="button save-map-button" class="btn btn-primary" disabled>Save changes</button>
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
        // content.appendChild(showSaveModal());
        saveMapModal.modal({show: true});
    })
}


// function prompMapSave()





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
    dataFileInput.addEventListener('change', function () {
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
            })
                // .then(response => console.log('Success:', JSON.stringify(response)))
                // .catch(error => console.error('Error:', error));
        })
    })
    
}

},{}]},{},[1]);
