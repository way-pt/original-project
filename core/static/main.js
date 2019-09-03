const homePage = document.querySelector('#home');
const fileUpload = document.querySelector('#file-upload');
const newMapButton = document.querySelector('#new-map');
const dataFileInput = document.querySelector('.data-file-input');


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
                
            })
        }
    })
}
