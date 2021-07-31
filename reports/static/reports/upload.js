// const myDropzone=document.getElementById('my-dropzone')

const csrfToken=document.getElementsByName('csrfmiddlewaretoken')[0].value 
const alertBox=document.getElementById('alert-box')

const handleAlerts = (type, msg) => {
    alertBox.innerHTML = `
    <div class="alert alert-${type}" role="alert">
        ${msg}
    </div>
    `
}

console.log(csrfToken)

Dropzone.autoDiscover=false

const myDropzone=new Dropzone('#my-dropzone',{
    url:'/reports/upload/',
    init: function(){
        this.on('sending',function(file,xhr,formData){
            console.log('sending')
            formData.append('csrfmiddlewaretoken',csrfToken)
        })
        this.on('success',function(file,response){
            console.log(response)
            const ex=response.ex 
            if (ex){
                handleAlerts('danger','File already exists!')
            }else{
                handleAlerts('success','Your file uploaded Successfully.')
            }

        })
    },
    maxFiles: 3,
    maxFilesize: 3,
    acceptedFiles:'.csv'
})