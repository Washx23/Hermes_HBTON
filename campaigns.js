document.addEventListener('DOMContentLoaded', (event) => {
    document.getElementById('addCampaignBtn').addEventListener('click', function() {
        toggleFormVisibility();
    });

    document.getElementById('campaignFormElement').addEventListener('submit', function(event) {
        event.preventDefault();
        const isEditing = this.dataset.isEditing === 'true';
        const campaignData = {
            title: document.getElementById('title').value,
            description: document.getElementById('description').value,
            videoUrl: document.getElementById('videoUrl').value
        };
        if (isEditing) {
            updateCampaign(campaignData);
        } else {
            addCampaignToDOM(campaignData);
        }
        hideForm();
    });

    document.getElementById('dashboard').addEventListener('click', function() {
        window.location.href = './index.html';
    });

    document.getElementById('statistics').addEventListener('click', function() {
        window.location.href = './StatisticsPage.html';
    });

    document.getElementById('campaignsBtn').classList.add('active');
    hideForm();
});

function toggleFormVisibility() {
    const form = document.getElementById('campaignForm');
    form.classList.toggle('hidden');
    form.dataset.isEditing = 'false';
    resetForm();
}

function hideForm() {
    document.getElementById('campaignForm').classList.add('hidden');
}

function resetForm() {
    const form = document.getElementById('campaignFormElement');
    form.reset();
    form.dataset.isEditing = 'false';
    form.dataset.editingTitle = '';
}

function addCampaignToDOM(campaign) {
    const campaignList = document.getElementById('campaignList');
    const li = document.createElement('li');
    li.className = 'box';
    li.innerHTML = `
        <h3>${campaign.title}</h3>
        <p>${campaign.description}</p>
        <a href="${campaign.videoUrl}" target="_blank">Watch Video</a>
        <button onclick="editCampaign('${campaign.title.replace(/'/g, "\\'")}');">Edit</button>
        <button class="delete-button">Delete</button>
    `;
    campaignList.appendChild(li);

    li.querySelector('.delete-button').addEventListener('click', () => {
        deleteCampaign(li);
    });
}

function editCampaign(title) {
    const campaigns = document.querySelectorAll('#campaignList li');
    campaigns.forEach(campaign => {
        if (campaign.querySelector('h3').textContent === title) {
            document.getElementById('title').value = title;
            document.getElementById('description').value = campaign.querySelector('p').textContent;
            document.getElementById('videoUrl').value = campaign.querySelector('a').href;
            
            const campaignForm = document.getElementById('campaignFormElement');
            campaignForm.dataset.isEditing = 'true';
            campaignForm.dataset.editingTitle = title;

            document.getElementById('campaignForm').classList.remove('hidden');
        }
    });
}

function updateCampaign(newData) {
    const campaigns = document.querySelectorAll('#campaignList li');
    const campaignForm = document.getElementById('campaignFormElement');
    const editingTitle = campaignForm.dataset.editingTitle;

    campaigns.forEach(campaign => {
        if (campaign.querySelector('h3').textContent === editingTitle) {
            campaign.querySelector('h3').textContent = newData.title;
            campaign.querySelector('p').textContent = newData.description;
            campaign.querySelector('a').href = newData.videoUrl;

            // Update the edit button to pass the new title
            campaign.querySelector('button').setAttribute('onclick', `editCampaign('${newData.title.replace(/'/g, "\\'")}');`);
        }
    });

    campaignForm.dataset.isEditing = 'false';
    campaignForm.dataset.editingTitle = '';
}

function deleteCampaign(li) {
    li.remove();
}
