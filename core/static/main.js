
// pages
const content = document.querySelector('#content');
const homePage = document.querySelector('#home');
const fileUpload = document.querySelector('#file-upload');
const loadingNewMap = document.querySelector('#loading-new-map');

// components
const newMapButton = document.querySelector('#new-map');
const dataFileInput = document.querySelector('.data-file-input');

// component templates
function showGeneratedImage(url, username) {
    username = username || '';

    const component = document.createElement('div');
    component.innerHTML = `
    <div class="generated-image card mb-3" style="max-width: 700px;">
        <div class="row no-gutters">
            <div class="col-md-8">
                <img src="${url}" class="card-img" alt="${url}">
            </div>
            <div class="col-md-4">
                <div class="card-body">
                    <h5 class="map-name"></h5>
                    <p class="map-user">User: <strong>${username}</p>
                    <p class="map-date"><small class="text-muted"></small></p>
                </div>
            </div>
        </div>
    </div>
    `
    return component;
}






if (document.querySelector('#loggedIn')) {
    var copyUser = document.querySelector('#loggedIn').dataset['username']
    var copyUsername = document.querySelector('#loggedIn').dataset['userstring']
    console.log(copyUser)
    console.log(copyUsername)
}



if (newMapButton && homePage) {
    
    newMapButton.addEventListener('click', function () {
        homePage.style.display = 'none';
        fileUpload.style.display = 'block';
    })
}

if (fileUpload) {
    const mapNameInput = document.querySelector('#map-name');
    const dataFileInput = document.querySelector('.data-file-input');
    dataFileInput.addEventListener('change', function () {
        let dataFile = dataFileInput.files[0];
        console.log(dataFile.name);
        const submitMapFormButton = document.querySelector('.submit-map-form');
        if (mapNameInput.value){
            submitMapFormButton.disabled = false;
            submitMapFormButton.addEventListener('click', function () {
                var formData = new FormData();
                let name = mapNameInput.value;
                let dataFileURL = URL.createObjectURL(dataFile);
                formData.append('name', name);
                formData.append('data', dataFile);

                fileUpload.style.display = 'none';
                loadingNewMap.style.display = 'block';
                fetch(`/api/new_map/filename=${dataFile.name}`, {
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
                    content.appendChild(showGeneratedImage(imageURL, copyUsername));
                })
                // .then(response => console.log('Success:', JSON.stringify(response)))
                // .catch(error => console.error('Error:', error));
            })
        }
    })
}
