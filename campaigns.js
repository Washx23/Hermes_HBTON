document.addEventListener('DOMContentLoaded', (event) => {
    document.getElementById('addCampaignBtn').addEventListener('click', function() {
        document.getElementById('campaignForm').classList.remove('hidden');
    });

    document.getElementById('campaignFormElement').addEventListener('submit', submitCampaignForm);
});

function submitCampaignForm(event) {
    event.preventDefault();
    // Logic to handle the form submission
    // Add the new campaign to the campaignList
    // Hide the form again
    const title = document.getElementById('title').value;
    const description = document.getElementById('description').value;
    const videoUrl = document.getElementById('videoUrl').value;

    addCampaignToDOM(title, description, videoUrl);
    document.getElementById('campaignForm').classList.add('hidden');
}

function addCampaignToDOM(title, description, videoUrl) {
    const campaignList = document.getElementById('campaignList');
    const li = document.createElement('li');
    
    li.innerHTML = `
        <h3>${title}</h3>
        <p>${description}</p>
        <a href="${videoUrl}" target="_blank">Watch Video</a>
        <button onclick="editCampaign('${title}');">Edit</button>
        <button onclick="deleteCampaign('${title}');">Delete</button>
    `;
    
    campaignList.appendChild(li);
}

function editCampaign(title) {
    const campaigns = document.querySelectorAll('#campaignList li');
    campaigns.forEach(campaign => {
        if (campaign.querySelector('h3').textContent === title) {
            // Populate form with existing values
            document.getElementById('title').value = title;
            document.getElementById('description').value = campaign.querySelector('p').textContent;
            document.getElementById('videoUrl').value = campaign.querySelector('a').href;
            
            // Display the form
            document.getElementById('campaignForm').classList.remove('hidden');
        }
    });
}


function deleteCampaign(title) {
    const campaigns = document.querySelectorAll('#campaignList li');
    campaigns.forEach(campaign => {
        if (campaign.querySelector('h3').textContent === title) {
            campaign.remove();
        }
    });
}

document.querySelectorAll('header nav button').forEach(btn => {
    btn.addEventListener('click', function() {
        // Remove active class from all buttons
        document.querySelectorAll('header nav button').forEach(button => {
            button.classList.remove('active');
        });
        // Add active class to clicked button
        this.classList.add('active');

        // Optional: Show the related section only
        showSection(this.id);
    });
});

// Function to handle showing the correct section
function showSection(sectionId) {
    // Assuming you have sections with corresponding IDs
    // Hide all sections
    document.querySelectorAll('main > div').forEach(section => {
        section.classList.add('hidden');
    });
    // Show the clicked section
    document.querySelector(`#${sectionId}`).classList.remove('hidden');
}

// Set the campaigns button as active on page load
window.onload = () => {
    document.getElementById('campaignsBtn').classList.add('active');
}
