jQuery.noConflict();
        jQuery(document).ready(function($){

            //So Load Button doesn't stay depressed
            $(".btn").mouseup(function(){
                $(this).blur();
            });


            // Register the 2 filepond plugins
            FilePond.registerPlugin(
                FilePondPluginImagePreview,
                FilePondPluginFileValidateSize,
            );


            // create a FilePond instance at the input element location
            const inputElement = document.querySelector('input[type="file"]');
            const pond = FilePond.create(inputElement);
            FilePond.setOptions({
                allowMultiple: false,
                instantUpload: false,
                maxFiles: 1,
                maxFileSize: "5MB",   

                // Send uploaded image to server and add the response img
                server: {
                    process: {
                        url: '/upload',
                        method: 'POST',
                        onload: (response) => {
                            response = JSON.parse(response);
                            create_plot(response['plot_img']);
                        }
                    },
                    revert: null  // Stop sending DELETE to server after undo/remove
                },

                // Remove the plot img when want to uplaod new sculpture
                onremovefile: (file) => {
                    if(document.contains(document.getElementById("plot_img"))) {
                        elem = document.getElementById("plot_img")
                        elem.parentNode.removeChild(elem);  
                    }
                },                
            });


            function create_plot(plot_img) {
                if (!document.contains(document.getElementById("plot_img"))){
                    var img = document.createElement("img");
                    img.id = "plot_img";
                    img.style.width = '550px';
                    img.style.height = '413px';
                    document.getElementById("plot_div").appendChild(img);
                }
                
                // Display image
                $("#plot_img").attr("src", "data:image/png;base64," + plot_img);
            }

            /*
            // Create the sculpture_img if it doesn't exist
            // Otherwise just get element
            function get_img() {
                // We'll need to create if it doesn't exist
                if (document.contains(document.getElementById("sculpture_img"))) {
                    // If already exists need to remove plot_img if exists
                    if(document.contains(document.getElementById("plot_img"))) {
                        elem = document.getElementById("plot_img");
                        elem.parentNode.removeChild(elem);  
                    }

                    var img = document.getElementById("sculpture_img");
                } else {
                    var img = document.createElement("img");
                    img.id = "sculpture_img";
                    img.style.width = '250px';
                    img.style.height = '350px';
                    document.getElementById("sculpture_div").appendChild(img);
                }

                return img;
            }


            // Change the image when you choose a file
            $("#fileButton").change(function(e) {
                for (var i = 0; i < e.originalEvent.srcElement.files.length; i++) {
                    var file = e.originalEvent.srcElement.files[i];

                    img = get_img();
                    img.src = URL.createObjectURL(file);
                }
            });



            // Create the plot_img and display
            function create_plot(response) {
                if (!document.contains(document.getElementById("plot_img"))){
                    var img = document.createElement("img");
                    img.id = "plot_img";
                    img.style.width = '600px';
                    img.style.height = '450px';
                    //img.style.paddingLeft = "50px";
                    img.style.position = "relative";
                    img.style.left = "100px";
                    document.getElementById("sculpture_div").appendChild(img);
                }
                
                // Display image
                $("#plot_img").attr("src", "data:image/png;base64," + response['plot_img'])
            }

            
            // Submit the pic when click the form and receive the results plot
            $('#file-form').on('submit',(function(e) {
                e.preventDefault();
                var formData = new FormData(this);

                $.ajax({
                    type:'POST',
                    url: $(this).attr('action'),
                    data:formData,
                    cache:false,
                    contentType: false,
                    processData: false,
                    success: function(response){
                        create_plot(response);
                    },
                    error: function(response){
                        console.log("error");
                    }
                });
            }));
            */

        });







