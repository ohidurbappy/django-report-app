const reportBtn = document.getElementById('report-btn')
const img = document.getElementById('img')


// console.log(reportBtn)
// console.log(img)

if (img) {
    reportBtn.classList.remove('invisible')
}

const modalBody = document.getElementById('modal-body')


const reportForm = document.getElementById('report-form')
const reportName = document.getElementById('id_name')
const reportRemarks = document.getElementById('id_remarks')
const csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value

const alertBox = document.getElementById('alert-box')


const handleAlerts = (type, msg) => {
    alertBox.innerHTML = `
    <div class="alert alert-${type}" role="alert">
        ${msg}
    </div>
    `
}

reportBtn.addEventListener('click', () => {
    img.setAttribute('class', 'w-100')
    modalBody.prepend(img)

    reportForm.addEventListener('submit', (e) => {
        e.preventDefault()

        const formData = new FormData()
        formData.append('csrfmiddlewaretoken', csrfToken)
        formData.append('name', reportName.value)
        formData.append('remarks', reportRemarks.value)
        formData.append('image', img.src)
        $.ajax({
            type: 'POST',
            url: '/reports/save/',
            data: formData,
            success: function (response) {
                handleAlerts('success', "Report Created")
                reportForm.reset()
            },
            error: function (err) {
                handleAlerts('danger', "Opps! Something went wrong.")
            },
            processData: false,
            contentType: false
        })
    })

})



// console.log(csrfToken)



