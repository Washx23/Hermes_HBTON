document.addEventListener('DOMContentLoaded', function() {
  const form = document.getElementById('urlForm');
  const videoNameInput = document.getElementById('videoNameInput');
  const urlInput = document.getElementById('urlInput');
  const existingCampaignsContainer = document.getElementById('existingCampaigns');

  form.addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the default form submission
    
    const videoName = videoNameInput.value;
    const urlValue = urlInput.value;

    // Create a new campaign box for the video name and URL
    const campaignBox = document.createElement('div');
    campaignBox.classList.add('campaign-box');
    campaignBox.innerHTML = `<strong>${videoName}</strong><br><a href="${urlValue}" target="_blank">${urlValue}</a>`; // Use the video name and make the URL an anchor element
    
    // Append the new campaign box to the existing campaigns container
    existingCampaignsContainer.appendChild(campaignBox);

    // Clear the inputs for new entries
    videoNameInput.value = '';
    urlInput.value = '';
  });
});

  
  