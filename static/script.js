//script.js

const body = document.body;

        
function toggleDarkMode() {
    
    body.classList.toggle('dark-mode');

   
    const isDarkModeEnabled = body.classList.contains('dark-mode');
    localStorage.setItem('darkModeEnabled', isDarkModeEnabled);

   
    const icon = document.getElementById('dark-mode-icon');
    if (isDarkModeEnabled) {
        icon.classList.remove('fa-sun');
        icon.classList.add('fa-moon');
    } else {
        icon.classList.remove('fa-moon');
        icon.classList.add('fa-sun');
    }
}


const isDarkModeEnabled = localStorage.getItem('darkModeEnabled') === 'true';
if (isDarkModeEnabled) {
    body.classList.add('dark-mode');
    
    const icon = document.getElementById('dark-mode-icon');
    icon.classList.remove('fa-sun');
    icon.classList.add('fa-moon');
}






let blurActive = false;

function toggleBlur() {
    blurActive = !blurActive;

    if (blurActive) {
        document.body.classList.add('blur-bc');
    } else {
        document.body.classList.remove('blur-bc');
    }
}






const inputFields = document.querySelectorAll('input[type="text"], textarea');

inputFields.forEach((inputField) => {
    inputField.addEventListener('focus', () => {
    	toggleBlur();
    	showDiv();
    	showRadioDiv();
    	collapseTagsDiv();
        document.body.style.overflow = 'hidden';
        inputField.scrollIntoView({ behavior: 'smooth', block: 'center' });
    });

    inputField.addEventListener('blur', () => {
    	toggleBlur();
        document.body.style.overflow = 'auto';
    });
});


let taggedParam;
 document.addEventListener('DOMContentLoaded', function() {
        const tagForm = document.getElementById('tag-form');
        const tagResults = document.getElementById('tag-results');

        tagForm.addEventListener('submit', function(event) {
            event.preventDefault(); 

           
            const formData = new FormData(tagForm);

            
            fetch('/get_tags', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(tags => {
            	taggedParam = tags.join(';');
            	clearResults();
            	collapseDiv();
            	collapseRadioDiv();
            	showTagsDiv();
            	showRel();
            	stopLoadingAnimation();
            	fetchAndDisplayResults(currentPage, taggedParam);
               
                tagResults.innerHTML = '';
                if (tags.length === 0) {
                	hideRel();
                	const ms = showMessageToUser();
                	const msg = document.createElement('h4');
                	msg.textContent = ms;
                	tagResults.appendChild(msg);
                	
                }
                tags.forEach(tag => {
                    const tagElement = document.createElement('a');
                    tagElement.className = 'btn btn-light';
                    tagElement.classList.add('tags');
                    tagElement.href = `https://stackoverflow.com/questions/tagged/${tag}`;
                    tagElement.textContent = tag;
                    tagResults.appendChild(tagElement);
                });
            })
            .catch(error => {
            	clearResults();
            	collapseDiv();
            	collapseRadioDiv();
            	showTagsDiv();
            	stopLoadingAnimation();
            	tagResults.innerHTML = '';
            	hideRel();
            	const msg = document.createElement('h4');
        	msg.textContent = "Some Error Occurred. Check your connection or try again.";
        	tagResults.appendChild(msg);
                console.error('Error:', error);
                
            });
        });
    });


const funnyMessages = [
    "Our crystal ball needs a vacation. Your question stumped it!",
    "Oops, we ran out of magic ink for our prediction quill!",
    "Looks like we need a cup of coffee to predict this one!",
    "This question is so mysterious, even Sherlock Holmes is baffled!",
    "Our prediction machine is on strike. Can we interest you in a joke instead?",
    "Your question is like a riddle wrapped in an enigma!",
    "Our prediction elves are napping. Try waking them up with another question!",
    "Hmm, our psychic parrot says it's too early to tell!",
    "Your question is as elusive as Bigfoot!",
    "We need more tea leaves to predict this one. Care for a virtual cup of tea?"
];

const rela = document.getElementById('rela');
function hideRel(){
	rela.style.display = "none";
}
function showRel(){
	rela.style.display = "block";
}


function showMessageToUser() {
    const randomMessage = funnyMessages[Math.floor(Math.random() * funnyMessages.length)];
    return "Could not predict. "+randomMessage;
}



let currentPage = 1;
const resultsPerPage = 5;
const resultsDiv = document.getElementById('results'); 
const loadMoreButton = document.getElementById('load-more-button'); 

function clearResults() {
    while (resultsDiv.firstChild) {
        resultsDiv.removeChild(resultsDiv.firstChild);
    }
}

function fetchAndDisplayResults(page, taggedParam) {
    
    
    const apiURL = `https://api.stackexchange.com/2.3/questions?tagged=${encodeURIComponent(taggedParam)}&site=stackoverflow&page=${page}`;

    fetch(apiURL)
        .then(response => response.json())
        .then(data => {
            data.items.slice(0, resultsPerPage).forEach(item => {
                const title = item.title;
                const link = item.link;
	
		
		const bigDiv = document.createElement('div');
		bigDiv.classList.add('bigDiv');
		
                const titleElement = document.createElement('div');
                titleElement.classList.add('li-title');
                const parser = new DOMParser();
                const decodedText = parser.parseFromString(title, 'text/html').body.textContent;

                titleElement.textContent = decodedText;

                const linkElement = document.createElement('a');
                linkElement.classList.add('btn');
                linkElement.classList.add('btn-light');
                linkElement.href = link;
                linkElement.textContent = 'Read more';

		bigDiv.appendChild(titleElement);
                bigDiv.appendChild(linkElement);		
		
		resultsDiv.appendChild(bigDiv);
                
            });

		
            if (data.has_more) {
                currentPage++;
                loadMoreButton.style.display = 'block'; 
            } else {
                
                loadMoreButton.style.display = 'none';
            }
        })
        .catch(error => console.error('Error:', error));
}


function loadMoreResults() {
    fetchAndDisplayResults(currentPage, taggedParam); 
}


loadMoreButton.addEventListener('click', loadMoreResults);

fetchAndDisplayResults(currentPage);



function collapseDiv() {
        // Collapse the content after clicking the button
        var collapseElement = document.getElementById('collapseExample');
        var bsCollapse = new bootstrap.Collapse(collapseElement, { toggle: false });
        bsCollapse.hide();
    }
    
function showDiv() {
    // Show the collapsed content
    var collapseElement = document.getElementById('collapseExample');
    var bsCollapse = new bootstrap.Collapse(collapseElement, { toggle: false });
    bsCollapse.show();
}

function collapseTagsDiv() {
	var collapseElement = document.getElementById('tags');
    	var bsCollapse = new bootstrap.Collapse(collapseElement, { toggle: false });
    	bsCollapse.hide();

}

function showTagsDiv() {
	var collapseElement = document.getElementById('tags');
    	var bsCollapse = new bootstrap.Collapse(collapseElement, { toggle: false });
    	bsCollapse.show();

}

function collapseRadioDiv() {
	var collapseElement = document.getElementById('radio');
    	var bsCollapse = new bootstrap.Collapse(collapseElement, { toggle: false });
    	bsCollapse.hide();

}

function showRadioDiv() {
	var collapseElement = document.getElementById('radio');
    	var bsCollapse = new bootstrap.Collapse(collapseElement, { toggle: false });
    	bsCollapse.show();

}






let loadingInProgress = false;
const animationContainer = document.getElementById('animation-container');
const animationElement = document.getElementById('animation');

function startLoadingAnimation() {
    if (!loadingInProgress) {
        loadingInProgress = true;
        animationContainer.style.display = 'inline-block';
        animationElement.classList.add('animate-dots-bars-5');
        
    }
}

function stopLoadingAnimation() {
    if (loadingInProgress) {
        loadingInProgress = false;
       animationElement.classList.remove('animate-dots-bars-5');
       animationContainer.style.display = 'none';
    }
}




document.getElementById('predict-button').addEventListener('click', function () {
    
    
    var inputValue = document.getElementById("ip").value;
    if (inputValue.trim() !== "") {
   
    startLoadingAnimation();
    }

});


function changeTextSize(delta) {
    
    const elements = document.querySelectorAll('[style*="font-size"], h1, h2, h3, h4, h5, h6');
    
    
    elements.forEach(element => {
        let currentSize = parseFloat(element.style.fontSize || getComputedStyle(element).fontSize);
        currentSize += delta; // Increase or decrease font size by the given delta
        element.style.fontSize = currentSize + 'px';
    });

    
    const placeholders = document.querySelectorAll('input[placeholder]');
    
    
    placeholders.forEach(input => {
        let currentSize = parseFloat(getComputedStyle(input).fontSize);
        currentSize += delta; // Increase or decrease font size by the given delta
        input.style.fontSize = currentSize + 'px';
    });

   
    const radioLabels = document.querySelectorAll('label[for^="radio"]');
    
  
    radioLabels.forEach(label => {
        let currentSize = parseFloat(getComputedStyle(label).fontSize);
        currentSize += delta; 
        label.style.fontSize = currentSize + 'px';
    });
}

function increaseTextSize() {
    changeTextSize(2); 
}


function decreaseTextSize() {
    changeTextSize(-2); 
}


document.getElementById('increase-text').addEventListener('click', increaseTextSize);
document.getElementById('decrease-text').addEventListener('click', decreaseTextSize);



function changeForm() {
  var platformSelect = document.getElementById("platform-select");
  var stackoverflowForm = document.getElementById("stackoverflow-form");
  var quoraForm = document.getElementById("quora-form");

  if (platformSelect.value === "stackoverflow") {
    stackoverflowForm.style.display = "block";
    quoraForm.style.display = "none";
  } else if (platformSelect.value === "quora") {
    stackoverflowForm.style.display = "none";
    quoraForm.style.display = "block";
  }
}

function submitQuoraForm() {
    const quoraForm = document.getElementById('quora-form1');
    const formData = new FormData(quoraForm);

    fetch('/process_quora_form', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        const tagResults = document.getElementById('tag-results1');
        tagResults.innerHTML = '';

        if (data.length === 0) {
            
            const message = showMessageToUser();
            const msgElement = document.createElement('h4');
            msgElement.textContent = message;
            tagResults.appendChild(msgElement);
        } else {
            data.forEach(tag => {
            	
                const tagElement = document.createElement('span');
                tagElement.className = 'tags';
                tagElement.textContent = tag;
                
                tagResults.appendChild(tagElement);
            });
        }
        
    })
    .catch(error => {
        console.error('Error:', error);
        
    });
}


