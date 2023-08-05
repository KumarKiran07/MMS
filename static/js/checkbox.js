const checkbox = document.getElementById('checkbox');
const textboxes = document.getElementsByClassName('textbox');
checkbox.addEventListener('click', function () {
    const isChecked = checkbox.checked;
    for (let i = 0; i < textboxes.length; i++) {
        textboxes[i].disabled = !isChecked;
    }
});