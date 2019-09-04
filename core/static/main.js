const homePage = document.querySelector('#home');
const fileUpload = document.querySelector('#file-upload');
const newMapButton = document.querySelector('#new-map');
const dataFileInput = document.querySelector('.data-file-input');


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

                let mapDict = {
                    "name": name,
                    "file": dataFile
                }
                console.log(JSON.stringify(mapDict))
                console.log(formData)
                console.log(formData.has('name'))
                console.log(formData.entries())
                fetch(`/api/new_map/filename=${dataFile.name}`, {
                    method: 'POST',
                    headers: {
                        "Content-Disposition": `form-data;name=name; filename=${dataFile.name}`
                    },
                    body: formData
                }).then(res => res.text())
                .then(text => console.log(text))
                // .then(response => console.log('Success:', JSON.stringify(response)))
                // .catch(error => console.error('Error:', error));
            })
        }
    })
}
