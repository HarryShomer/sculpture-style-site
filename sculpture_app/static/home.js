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
                instantUpload: true,
                maxFiles: 1,
                maxFileSize: "5MB",   

                // Send uploaded image to server and add the response img
                server: {
                    process: {
                        url: '/upload',
                        method: 'POST',
                        onload: (response) => {
                            response = JSON.parse(response);
                            //highest_style_prob(response['max_style']);
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


            // Create the plot containing the probability of each class
            // Takes in a base64 string of img
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


            // Note which style has the highest probability for the image
            // Create little message
            function highest_style_prob(max_style) {
                if (!document.contains(document.getElementById("likely_style"))){
                    var par = document.createElement("p");
                    var node = document.createTextNode("The model believes that the most likely style" +
                                                       " of this sculpture is - " + max_style);
                    par.appendChild(node);
                    par.id = "likely_style";
                    document.getElementById("plot_div").appendChild(par);
                }
                
            }

        });







